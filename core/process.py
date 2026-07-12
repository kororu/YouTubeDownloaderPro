"""External process helpers."""

from __future__ import annotations

import os
import subprocess
from typing import Any

PROCESS_TERMINATION_TIMEOUT_SECONDS: float = 5.0


def hidden_process_kwargs() -> dict[str, Any]:
    """Return subprocess options that hide console windows on Windows.

    Returns:
        Keyword arguments compatible with subprocess.Popen.
    """
    if os.name != "nt":
        return {}

    startupinfo: subprocess.STARTUPINFO = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    return {
        "creationflags": subprocess.CREATE_NO_WINDOW,
        "startupinfo": startupinfo,
    }


def create_text_process(
    command: list[str],
    stdout: int | None = subprocess.PIPE,
    stderr: int | None = subprocess.PIPE,
    bufsize: int = -1,
) -> subprocess.Popen[str]:
    """Create a text-mode external process with hidden Windows startup.

    Args:
        command: Command arguments.
        stdout: stdout redirection mode.
        stderr: stderr redirection mode.
        bufsize: Buffering policy passed to subprocess.

    Returns:
        Started process.
    """
    return subprocess.Popen(
        command,
        stdout=stdout,
        stderr=stderr,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=bufsize,
        **hidden_process_kwargs(),
    )


def terminate_process(process: subprocess.Popen[str]) -> int:
    """Terminate a process and kill it if it does not exit promptly.

    Args:
        process: Active process.

    Returns:
        Process return code, or -1 when the process cannot be reaped.
    """
    if process.poll() is None:
        process.terminate()
    try:
        return process.wait(timeout=PROCESS_TERMINATION_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            return process.wait(timeout=PROCESS_TERMINATION_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return -1


def request_process_termination(process: subprocess.Popen[str]) -> None:
    """Ask a process to terminate without blocking the caller.

    Args:
        process: Active process.
    """
    if process.poll() is None:
        process.terminate()


def wait_for_process(process: subprocess.Popen[str]) -> int:
    """Wait for a process and kill it if it stays alive too long.

    Args:
        process: Active process.

    Returns:
        Process return code, or -1 when the process cannot be reaped.
    """
    try:
        return process.wait(timeout=PROCESS_TERMINATION_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            return process.wait(timeout=PROCESS_TERMINATION_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return -1
