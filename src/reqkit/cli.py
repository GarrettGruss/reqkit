"""CLI for reqkit."""

import argparse
from pathlib import Path
from reqkit.parser import parse_str
from reqkit.tracer import Tracer
from reqkit.types import ReqkitBase, ReqkitRequirement
from pydantic import BaseModel, PositiveInt
from typing import List, Optional


class MintInterface(BaseModel):
    qty: PositiveInt
    subtype: Optional[str] = None
    category: Optional[str] = None
    parent_id: Optional[str] = None
    parent_rel: Optional[str] = None


def _cmd_mint(args: argparse.Namespace) -> None:
    # validate args
    params = MintInterface(
        qty=args.qty,
        subtype=args.subtype,
        category=args.category,
        parent_id=args.parent_id,
        parent_rel=args.parent_rel,
    )
    objs = [
        ReqkitRequirement(
            subtype=params.subtype,
            category=params.category,
            parent_id=params.parent_id,
            parent_rel=params.parent_rel,
            body=" ",
        )
        for _ in range(int(params.qty))
    ]

    for obj in objs:
        print(str(obj))


def _cmd_parse(args: argparse.Namespace) -> None:
    with open(args.file) as f:
        objs = parse_str(f.read())

    for obj in objs:
        print(str(obj))


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


def _cmd_trace(args: argparse.Namespace) -> None:
    objs = _recursive_parse(args.source)
    if args.target:
        objs += _recursive_parse(args.target)

    tracer = Tracer()
    trace_map = tracer.build_map(objs)
    print(
        tracer.construct_report(
            trace_map,
            include_requirement_body=args.verbosity != "minimal",
            include_trace_body=args.verbosity == "full",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold and manage requirement traces"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    mint_parser = subparsers.add_parser(
        "mint", help="Mint a new requirement with an ID"
    )
    mint_parser.add_argument("--subtype")
    mint_parser.add_argument("--category")
    mint_parser.add_argument("--parent_id")
    mint_parser.add_argument("--parent_rel")
    mint_parser.add_argument("--qty", type=int, default=1)
    mint_parser.set_defaults(func=_cmd_mint)

    parse_parser = subparsers.add_parser(
        "parse", help="Parse rq- tags out of a file"
    )
    parse_parser.add_argument("file")
    parse_parser.set_defaults(func=_cmd_parse)

    trace_parser = subparsers.add_parser(
        "trace", help="Recursively trace requirements against code"
    )
    trace_parser.add_argument(
        "--source", required=True, help="File or directory to recursively parse for requirements"
    )
    trace_parser.add_argument(
        "--target", help="File or directory to recursively parse for traces"
    )
    verbosity_group = trace_parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "--full",
        action="store_const",
        dest="verbosity",
        const="full",
        help="Include requirement and trace body text in the report",
    )
    verbosity_group.add_argument(
        "--partial",
        action="store_const",
        dest="verbosity",
        const="partial",
        help="Include requirement body text, omit trace body text (default)",
    )
    verbosity_group.add_argument(
        "--minimal",
        action="store_const",
        dest="verbosity",
        const="minimal",
        help="Omit requirement and trace body text",
    )
    trace_parser.set_defaults(func=_cmd_trace, verbosity="partial")

    args = parser.parse_args()
    args.func(args)
