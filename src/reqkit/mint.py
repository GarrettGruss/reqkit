"""mint.py is a factory helper for constructing a new reqkit object."""

from secrets import token_hex
from reqkit.types import ReqkitRequirement
from reqkit.config import Config
from typing import Optional


def mint_requirements(
    qty: int,
    rq_type: Optional[str],
    category: Optional[str],
    parent_id: Optional[str],
    parent_rel: Optional[str],
) -> list[ReqkitRequirement]:
    return [
        mint_requirement(rq_type, category, parent_id, parent_rel) for _ in range(qty)
    ]


def mint_requirement(
    rq_type: Optional[str],
    category: Optional[str],
    parent_id: Optional[str],
    parent_rel: Optional[str],
) -> ReqkitRequirement:
    return ReqkitRequirement(
        rq_type=validate_requirement_type(rq_type) if rq_type is not None else "req",
        category=validate_category(category) if category is not None else None,
        parent_id=validate_parent_id(parent_id) if parent_id is not None else None,
        parent_rel=validate_relationship_type(parent_rel) if parent_rel is not None else None,
        id=generate_id(),
    )


# Helpers
def generate_id(length=6, strategy="hex") -> str:
    if strategy == "hex":
        return token_hex(length // 2)
    raise NotImplementedError(
        f"strategy ${strategy} is not supported for generating reqkit ids"
    )


def validate_requirement_type(rq_type: str) -> str:
    if rq_type in Config.allowed_requirement_types:
        return rq_type
    raise TypeError(
        f"${rq_type} is not an allowed requirement type."
        + f" Allowed requirement types: {Config.allowed_requirement_types}"
    )


def validate_category(category: str) -> str:
    # placeholder for now
    return str


def validate_parent_id(parent_id: str) -> str:
    # placeholder for now, but show perform an optional lookup
    # to detect if the id is associated to any object before creating
    return str


def validate_relationship_type(parent_rel: str) -> str:
    if parent_rel in Config.allowed_relationship_types:
        return parent_rel
    raise TypeError(
        f"${parent_rel} is not an allowed relationship type."
        + f" Allowed relationship types: {Config.allowed_relationship_types}"
    )
