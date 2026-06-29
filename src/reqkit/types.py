from secrets import token_hex
from typing import Optional
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field, field_validator
from reqkit.config import Config


def _generate_id(length: int = 6, strategy: str = "hex") -> str:
    if strategy == "hex":
        return token_hex(length // 2)
    raise NotImplementedError(
        f"strategy ${strategy} is not supported for generating reqkit ids"
    )


class ReqkitBase(BaseModel):
    """Reqkit base class."""

    subtype: Optional[str] = None
    category: Optional[str] = None
    parent_id: Optional[str] = None # for v2, convert the parent_id into a list of ids
    parent_rel: Optional[str] = None
    body: Optional[str] = None

    @field_validator("subtype")
    @classmethod
    def validate_subtype(cls, subtype: Optional[str]) -> Optional[str]:
        if subtype is None or subtype in Config.allowed_requirement_types:
            return subtype
        raise ValueError(
            f"${subtype} is not an allowed requirement subtype."
            + f" Allowed requirement subtypes: {Config.allowed_requirement_types}"
        )

    @field_validator("parent_rel")
    @classmethod
    def validate_parent_rel(cls, parent_rel: Optional[str]) -> Optional[str]:
        if parent_rel is None or parent_rel in Config.allowed_relationship_types:
            return parent_rel
        raise ValueError(
            f"${parent_rel} is not an allowed relationship type."
            + f" Allowed relationship types: {Config.allowed_relationship_types}"
        )

    def _to_xml(self, tag: str) -> ET.Element:
        elem = ET.Element(tag, attrib=self.model_dump(exclude={"body"}, exclude_none=True))
        if self.body:
            elem.text = self.body
        return elem

    def __str__(self):
        return ET.tostring(self._to_xml("rq-element"), encoding="unicode")


class ReqkitRequirement(ReqkitBase):
    """Reqkit requirement class."""

    id: str = Field(
        default_factory=lambda: _generate_id(strategy=Config.generate_id_strategy)
    )

    def __str__(self):
        return ET.tostring(self._to_xml("rq-req"), encoding="unicode")


class ReqkitTrace(ReqkitBase):
    """Reqkit trace class."""
