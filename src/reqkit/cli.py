"""CLI for reqkit."""

import argparse
from reqkit.mint import reqkitObjectFactory


def _cmd_mint(args: argparse.Namespace) -> None:
    breakpoint()
    objs = reqkitObjectFactory().mint_many(
        int(args.qty), args.type,
        category=args.category, parent_id=args.parent_id, parent_rel=args.parent_rel,
    )

    print(f"Minted {len(objs)} {objs[0]['rq_type']}(s)")
    for obj in objs:
        print("\n" + str(obj))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold and manage requirement traces"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    mint_parser = subparsers.add_parser(
        "mint", help="Mint a new reqkit object with an ID"
    )
    mint_parser.add_argument("--type", default="req")
    mint_parser.add_argument("--category")
    mint_parser.add_argument("--parent_id")
    mint_parser.add_argument("--parent_rel")
    mint_parser.add_argument("--qty", type=int, default=1)
    mint_parser.set_defaults(func=_cmd_mint)

    args = parser.parse_args()
    args.func(args)
