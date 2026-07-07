"""CLI for reqkit."""

import click
from pathlib import Path
from typing import List

from reqkit.parser import parse_str
from reqkit.tracer import Tracer
from reqkit.types import ReqkitBase, ReqkitRequirement


@click.group()
def main() -> None:
    """Scaffold and manage requirement traces."""


@main.command()
@click.option("--subtype", default=None)
@click.option("--category", default=None)
@click.option("--parent_id", default=None)
@click.option("--parent_rel", default=None)
@click.option("--qty", default=1, type=click.IntRange(min=1))
def mint(
    subtype: str | None,
    category: str | None,
    parent_id: str | None,
    parent_rel: str | None,
    qty: int,
) -> None:
    """Mint a new requirement with an ID."""
    objs = [
        ReqkitRequirement(
            subtype=subtype,
            category=category,
            parent_id=parent_id,
            parent_rel=parent_rel,
            body=" ",
        )
        for _ in range(qty)
    ]
    for obj in objs:
        click.echo(str(obj))


@main.command()
@click.argument("file", type=click.Path(exists=True))
def parse(file: str) -> None:
    """Parse rq- tags out of a file."""
    with open(file) as f:
        objs = parse_str(f.read())
    for obj in objs:
        click.echo(str(obj))


def _recursive_parse(path: str) -> List[ReqkitBase]:
    """Parse a single file, or every file under a directory, into reqkit objects."""
    target = Path(path)
    files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]

    objs: List[ReqkitBase] = []
    for file in files:
        try:
            text = file.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        objs.extend(parse_str(text))

    return objs


@main.command()
@click.option("--source", required=True, help="File or directory to recursively parse for requirements")
@click.option("--target", default=None, help="File or directory to recursively parse for traces")
@click.option("--full", "verbosity", flag_value="full", help="Include requirement and trace body text in the report")
@click.option("--partial", "verbosity", flag_value="partial", default=True, help="Include requirement body text, omit trace body text (default)")
@click.option("--minimal", "verbosity", flag_value="minimal", help="Omit requirement and trace body text")
def trace(source: str, target: str | None, verbosity: str) -> None:
    """Recursively trace requirements against code."""
    objs = _recursive_parse(source)
    if target:
        objs += _recursive_parse(target)

    tracer = Tracer()
    trace_map = tracer.build_map(objs)
    click.echo(
        tracer.construct_report(
            trace_map,
            include_requirement_body=verbosity != "minimal",
            include_trace_body=verbosity == "full",
        )
    )
