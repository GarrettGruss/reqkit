# trace.md

The trace function is the primary feature of reqkit - the ability to perform a deep recursive trace amongst the code base to asses compliance or drift against a requirement.

## Workflow

- user calls `rq trace --root <rq_id>|<filename> --type <rq_types> --category <rq_categories> --scope<dir>`
- if no scope is specified, tracer walks upwards to the .git dir, assume this is root of the project
- Tracer recursively walks the project, constructing a dictonary of `{<parent_id>:List[<rq_obj>]}`
> note: both `<rq_trace>` and `<rq_req>` should inherit from the base `<rq_obj>` class
> note: set an internal recursion limit in the ENV
- tracer walks the root document and constructs a list of origin elements. If an element does not satisfy the optional category or type filter, do not add it
- sort the origin elements list
- loop through the elements and map them to trace dictonary, constructing a trace object - need to define this as a dataclass
- Call the report function to dump the trace object to text
- print to stdio