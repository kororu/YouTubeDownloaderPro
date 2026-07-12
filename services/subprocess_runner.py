"""Subprocess execution foundation."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass

from core.exceptions import CommandExecutionError
from core.process import create_text_process


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Completed command result.

    Attributes:
        command: Executed command arguments.
        return_code: Process return code.
        stdout: Captured stdout.
        stderr: Captured stderr.
    """

    command: list[str]
    return_code: int
    stdout: str
    stderr: str


class SubprocessRunner:
    """Runs external commands through subprocess."""

    def run(self, command: list[str], timeout_seconds: int = 60) -> CommandResult:
        """Run a command and capture output.

        Args:
            command: Command arguments.
            timeout_seconds: Maximum execution time in seconds.

        Returns:
            Captured command result.

        Raises:
            CommandExecutionError: If the process fails or times out.
        """
        process: subprocess.Popen[str] | None = None
        try:
            process = create_text_process(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate(timeout=timeout_seconds)
        except FileNotFoundError as exc:
            raise CommandExecutionError(f"Command not found: {command[0]}") from exc
        except subprocess.TimeoutExpired as exc:
            if process is not None:
                process.kill()
                process.communicate()
            raise CommandExecutionError(f"Command timed out: {' '.join(command)}") from exc

        result: CommandResult = CommandResult(
            command=command,
            return_code=process.returncode,
            stdout=stdout,
            stderr=stderr,
        )
        if result.return_code != 0:
            message: str = result.stderr.strip() or "Command failed without stderr output."
            raise CommandExecutionError(message)
        return result
