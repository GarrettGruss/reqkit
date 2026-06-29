from dataclasses import dataclass
from typing import Optional


@dataclass
class ReqkitBase:
    """Reqkit base class."""

    rq_type: Optional[str]
    category: Optional[str]
    parent_id: Optional[str]
    parent_rel: Optional[str]

    def __str__(self):
        return (
            "<rq-element" + f' type="{self.rq_type}"'
            if self.rq_type
            else "" + f' category="{self.category}"'
            if self.category
            else "" + f' parent_id="{self.parent_id}"'
            if self.parent_id
            else "" + f' parent_rel="{self.parent_rel}"'
            if self.parent_rel
            else "" + "></rq-element>"
        )


@dataclass
class ReqkitRequirement(ReqkitBase):
    """Reqkit requirement class."""

    id: str

    def __str__(self):
        return (
            "<rq-req" + f' id="{self.id}"' + f' type="{self.rq_type}"'
            if self.rq_type
            else "" + f' category="{self.category}"'
            if self.category
            else "" + f' parent_id="{self.parent_id}"'
            if self.parent_id
            else "" + f' parent_rel="{self.parent_rel}"'
            if self.parent_rel
            else "" + "></rq-req>"
        )


@dataclass
class ReqkitTrace(ReqkitBase):
    """Reqkit trace class."""

    def __str__(self):
        return (
            "<rq-trace" + f' type="{self.rq_type}"'
            if self.rq_type
            else "" + f' category="{self.category}"'
            if self.category
            else "" + f' parent_id="{self.parent_id}"'
            if self.parent_id
            else "" + f' parent_rel="{self.parent_rel}"'
            if self.parent_rel
            else "" + "></rq-trace>"
        )
