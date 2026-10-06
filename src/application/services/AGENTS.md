# Services guide

A service is a rule or step sequence that spans several entities or ports
and names a domain concept. See "Where logic goes" in
`application/AGENTS.md`.

- Describe it in one sentence without "and". If you cannot, split it.
- Do not name it after a use case. Avoid `Manager`, `Helper`, `Processor`.
- Not a service: a single dm or queries call, a rule over one entity, or
  steps extracted only to shorten a use case.
- One service → one file, grouped by domain.
- Inject dependencies as protected dataclass fields, like use cases.
