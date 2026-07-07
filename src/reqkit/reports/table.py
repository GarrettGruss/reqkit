"""Report generator to create a `RICH` table."""

from dataclasses import dataclass, field
from typing import List, Optional

from rich.table import Table

from reqkit.types import ReqkitBase


_VALID_COLUMNS = {"type", "id", "subtype", "category", "parent_id", "parent_rel", "body"}

_DEFAULT_COLUMNS = ["type", "id", "subtype", "category", "parent_id", "parent_rel", "body"]


def extract_column(obj: ReqkitBase, column: str) -> str:
    """Return the string value of a named column for a reqkit object."""
    if column not in _VALID_COLUMNS:
        raise ValueError(f"Unknown column: {column!r}. Valid: {_VALID_COLUMNS}")
    value = obj.model_dump().get(column) or ""
    return value.strip() if column == "body" else value


@dataclass
class TableConfig:
    columns: List[str] = field(default_factory=lambda: list(_DEFAULT_COLUMNS))
    title: Optional[str] = None
    style: Optional[str] = None
    header_style: str = "bold"
    show_lines: bool = False

    def __post_init__(self) -> None:
        unknown = set(self.columns) - _VALID_COLUMNS
        if unknown:
            raise ValueError(f"Unknown column(s): {unknown}. Valid: {_VALID_COLUMNS}")


class ReqkitTable:
    """Wraps a Rich Table for a list of ReqkitBase objects."""

    def __init__(self, objs: List[ReqkitBase]) -> None:
        self._objs = objs
        self._config = TableConfig()

    def set_config(self, config: TableConfig) -> "ReqkitTable":
        """Apply a TableConfig to this table."""
        self._config = config
        return self

    def generate(self) -> Table:
        """Build and return the configured Rich Table."""
        table = Table(
            title=self._config.title,
            style=self._config.style,
            header_style=self._config.header_style,
            show_lines=self._config.show_lines,
        )

        for col in self._config.columns:
            table.add_column(col)

        for obj in self._objs:
            table.add_row(*[extract_column(obj, col) for col in self._config.columns])

        return table
