"""mint.py is a factory helper for constructing a new reqkit object."""

from dataclasses import dataclass
from secrets import token_hex
from reqkit.types import ReqkitRequirement, ReqkitBase
from reqkit.config import Config
from typing import Optional


@dataclass
class reqkitObjectFactory:
    """Factory class for creating reqkit objects."""

    def mint_many(self, qty: int, rq_type: str, **kwargs):
        return [self.mint(rq_type, **kwargs) for _ in range(qty)]

    def mint(self, rq_type: str, **kwargs) -> ReqkitBase:
        if rq_type in {"requirement", "req"}:
            return self._mint_requirement(**kwargs)
        elif rq_type == "trace":
            raise NotImplementedError("Minting is not supported for traces")
        raise TypeError(f"Unspported mint type {rq_type}")

    def _mint_requirement(
        self, subtype: Optional[str], category: Optional[str], parent_id: Optional[str], parent_rel: Optional[str]
    ) -> list[ReqkitRequirement]:
        return ReqkitRequirement(
            subtype=validate_requirement_type(subtype) or None,
            category=validate_category(category) or None,
            parent_id=validate_parent_id(parent_id) or None,
            parent_rel=validate_relationship_type(parent_rel) or None,
        )


# Helpers


def generate_id(length=6, strategy="hex") -> str:
    if strategy == "hex":
        return token_hex(length // 2)
    raise NotImplementedError(
        f"strategy ${strategy} is not supported for generating reqkit ids"
    )


def validate_requirement_type(subtype: str) -> str:
    if subtype in Config.allowed_requirement_types:
        return subtype
    raise TypeError(
        f"${subtype} is not an allowed requirement type."
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
        + f" Allowed relationship types: {Config.allowed_requirement_types}"
    )
