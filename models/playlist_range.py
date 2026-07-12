"""Playlist range domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaylistRange:
    """One-based inclusive playlist range.

    Attributes:
        start_index: First playlist item to process.
        end_index: Last playlist item to process.
    """

    start_index: int
    end_index: int

    def __post_init__(self) -> None:
        """Validate the range."""
        if self.start_index < 1:
            raise ValueError("Playlist start index must be at least 1.")
        if self.end_index < self.start_index:
            raise ValueError("Playlist end index must be greater than or equal to start index.")

    @property
    def item_count(self) -> int:
        """Return the number of requested playlist items."""
        return self.end_index - self.start_index + 1

    @classmethod
    def from_start_and_limit(cls, start_index: int, max_items: int) -> "PlaylistRange":
        """Create a playlist range from a start index and item count.

        Args:
            start_index: First playlist item to process.
            max_items: Number of playlist items to process.

        Returns:
            Valid playlist range.
        """
        if max_items < 1:
            raise ValueError("Playlist range limit must be at least 1.")
        return cls(start_index=start_index, end_index=start_index + max_items - 1)

    @classmethod
    def from_optional_end(
        cls,
        start_index: int,
        end_index: int | None,
        max_items: int,
    ) -> "PlaylistRange":
        """Create a range from optional end index and fallback limit.

        Args:
            start_index: First playlist item to process.
            end_index: Optional explicit last playlist item.
            max_items: Fallback item count when end index is not provided.

        Returns:
            Valid playlist range.
        """
        if end_index is None:
            return cls.from_start_and_limit(start_index, max_items)
        return cls(start_index=start_index, end_index=end_index)

    def next_range(self, max_items: int) -> "PlaylistRange":
        """Return the next adjacent range using the configured item count.

        Args:
            max_items: Number of playlist items to process next.

        Returns:
            Next adjacent range.
        """
        return self.from_start_and_limit(self.end_index + 1, max_items)

    def label(self) -> str:
        """Return a user-facing range label."""
        return f"{self.start_index}-{self.end_index}"
