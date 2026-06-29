from dataclasses import dataclass
from typing import Optional
# import xml.etree.ElementTree as ET
# Change the __str__ method to use a default xml library

@dataclass
class ReqkitBase:
    """Reqkit base class."""

    subtype: Optional[str]
    category: Optional[str]
    parent_id: Optional[str]
    parent_rel: Optional[str]
    body: Optional[str]

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


@dataclass
class ReqkitRequirement(ReqkitBase):
    """Reqkit requirement class."""

    id: str

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


@dataclass
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
