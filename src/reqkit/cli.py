"""CLI for reqkit."""

import argparse
from reqkit.parser import parse_str
from reqkit.types import ReqkitRequirement
from pydantic import BaseModel, PositiveInt
from typing import Optional


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
            body="my requirement",
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

    args = parser.parse_args()
    args.func(args)
