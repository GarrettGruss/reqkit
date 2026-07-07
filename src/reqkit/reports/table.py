"""Report generator to create a `RICH` table."""

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd
from rich.table import Table

from reqkit.types import ReqkitBase


def _body_last(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with columns reordered so 'body' is last, if present."""
    if "body" not in df.columns:
        return df
    return df[[c for c in df.columns if c != "body"] + ["body"]]


@dataclass
class TableConfig:
    title: Optional[str] = None
    style: Optional[str] = None
    header_style: str = "bold"
    show_lines: bool = False
    body_lines: Optional[int] = None

class ReqkitTable:
    """Wraps a Rich Table for a list of ReqkitBase objects."""

    def __init__(self, objs: List[ReqkitBase]) -> None:
        self._df = pd.DataFrame([obj.model_dump() for obj in objs])
        self._config = TableConfig()

    def set_config(self, config: TableConfig) -> "ReqkitTable":
        """Apply a TableConfig to this table."""
        self._config = config
        return self

    def generate(self) -> Table:
        """Build and return the configured Rich Table."""
        df = _body_last(self._df)
        if "body" in df.columns:
            df["body"] = df["body"].str.strip()
            if self._config.body_lines is not None:
                df["body"] = df["body"].str.split("\n").str[: self._config.body_lines].str.join("\n")

        table = Table(
            title=self._config.title,
            style=self._config.style,
            header_style=self._config.header_style,
            show_lines=self._config.show_lines,
        )

        for col in df.columns:
            table.add_column(col)

        for row in df.itertuples(index=False):
            table.add_row(*[str(v) for v in row])

        return table
