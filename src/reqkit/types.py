from secrets import token_hex
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from reqkit.config import Config
# import xml.etree.ElementTree as ET
# Change the __str__ method to use a default xml library


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
    parent_id: Optional[str] = None
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

    def __str__(self):
        return (
            "<rq-element"
            + (f' subtype="{self.subtype}"' if self.subtype else "")
            + (f' category="{self.category}"' if self.category else "")
            + (f' parent_id="{self.parent_id}"' if self.parent_id else "")
            + (f' parent_rel="{self.parent_rel}"' if self.parent_rel else "")
            + ">"
            + (self.body if self.body else "")
            + "</rq-element>"
        )


class ReqkitRequirement(ReqkitBase):
    """Reqkit requirement class."""

    id: str = Field(
        default_factory=lambda: _generate_id(strategy=Config.generate_id_strategy)
    )

    def __str__(self):
        return (
            "<rq-req"
            + (f' id="{self.id}')
            + (f' subtype="{self.subtype}"' if self.subtype else "")
            + (f' category="{self.category}"' if self.category else "")
            + (f' parent_id="{self.parent_id}"' if self.parent_id else "")
            + (f' parent_rel="{self.parent_rel}"' if self.parent_rel else "")
            + ">"
            + (self.body if self.body else "")
            + "</rq-req>"
        )


class ReqkitTrace(ReqkitBase):
    """Reqkit trace class."""

    def __str__(self):
        return (
            "<rq-element"
            + (f' subtype="{self.subtype}"' if self.subtype else "")
            + (f' category="{self.category}"' if self.category else "")
            + (f' parent_id="{self.parent_id}"' if self.parent_id else "")
            + (f' parent_rel="{self.parent_rel}"' if self.parent_rel else "")
            + ">"
            + (self.body if self.body else "")
            + "</rq-element>"
        )
