"""Constructs a list of reqkit objects into a hash map, and reports on it."""

from typing import Dict, List, Optional

from reqkit.types import ReqkitBase, ReqkitRequirement, ReqkitTrace

_COMPLIANT_RELATIONS = {"satisfy", "verify"}


class Tracer:
    """Builds a `{parent_id: [reqkit objects]}` hash map from a flat list of
    reqkit objects, and reports on requirement compliance."""

    def build_map(self, objs: List[ReqkitBase]) -> Dict[Optional[str], List[ReqkitBase]]:
        trace_map: Dict[Optional[str], List[ReqkitBase]] = {}
        for obj in objs:
            trace_map.setdefault(obj.parent_id, []).append(obj)
        return trace_map

    def construct_report(self, trace_map: Dict[Optional[str], List[ReqkitBase]]) -> str:
        """Render a compliance report by mapping over a hash map built by build_map.

        Each requirement is reported as non-compliant (no traces),
        partially-compliant (traces exist, but none satisfy/verify it), or
        compliant (at least one satisfy/verify trace). Traces that aren't
        attached to any requirement are counted separately as orphaned.
        """

        def report_lines(requirement: ReqkitRequirement, depth: int = 0) -> List[str]:
            children = trace_map.get(requirement.id, [])
            traces = [c for c in children if isinstance(c, ReqkitTrace)]
            sub_requirements = [c for c in children if isinstance(c, ReqkitRequirement)]

            relations = {t.parent_rel for t in traces if t.parent_rel}
            if not traces:
                status = "non-compliant"
            elif relations & _COMPLIANT_RELATIONS:
                status = "compliant"
            else:
                status = "partially-compliant"

            indent = "  " * depth
            lines = [f"{indent}{requirement} — {status} ({len(traces)} trace(s))"]
            lines += [f"{indent}  - {t}" for t in traces]
            lines += [
                line
                for sub_lines in map(lambda r: report_lines(r, depth + 1), sub_requirements)
                for line in sub_lines
            ]
            return lines

        all_objs = [obj for objs_ in trace_map.values() for obj in objs_]
        requirement_ids = {o.id for o in all_objs if isinstance(o, ReqkitRequirement)}

        # a requirement is top-level if it has no parent, or its parent_id
        # doesn't resolve to a known requirement (dangling reference)
        top_level = [
            o
            for o in all_objs
            if isinstance(o, ReqkitRequirement) and o.parent_id not in requirement_ids
        ]
        lines = [line for section in map(report_lines, top_level) for line in section]

        orphaned_traces = [
            o
            for o in all_objs
            if isinstance(o, ReqkitTrace) and o.parent_id not in requirement_ids
        ]

        lines.append("")
        lines.append(f"Total requirements: {len(requirement_ids)}")
        lines.append(f"Total traces: {sum(isinstance(o, ReqkitTrace) for o in all_objs)}")
        lines.append(f"Orphaned traces: {len(orphaned_traces)}")

        return "\n".join(lines)
