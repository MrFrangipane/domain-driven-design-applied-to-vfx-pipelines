## DDD mapping

This example is intentionally small, but it maps to DDD concepts in a practical way.

### Domain concepts

The main domain concepts are:

- `ArchiveCandidate`;
- `ArchiveDecision`;
- `ResolvedArchiveDecision`;
- `ArchiveMark`;
- `ArchivePlan`;
- `ArchivePlanItem`.

These objects describe the language of the archiving problem directly. The code does not pass around anonymous dictionaries such as `{"path": ..., "parsed": ..., "archive": true}`. Instead, it gives names to the production concepts being handled.

### Value Objects

Most objects in this example behave like Value Objects.

Examples:

- `ArchiveCandidate`;
- `ArchiveDecision`;
- `ResolvedArchiveDecision`;
- `ArchivePlanItem`;
- `ArchivePlan`.

They are small immutable dataclasses that are defined by their data rather than by a long-lived identity.

For example, an `ArchivePlanItem` is the value:

- source path;
- archive path;
- reasons.

If those values are the same, the plan item represents the same planned action.

### Domain rules

Archive rules live in the `rules` package.

Examples:

- `ArchiveWorkFilesRule`;
- `KeepLastVersionsRule`;
- `ArchiveDecisionResolver`;
- `ArchiveRulePolicy`.

These classes contain the business meaning of archiving:

- only work files are candidates for archiving;
- versions are evaluated in families;
- recent versions can be protected;
- conflicting decisions are resolved consistently.

The important DDD idea is that these rules are represented explicitly in the domain language instead of being hidden inside CLI code or filesystem code.

### Application use case

`BuildArchivePlanUseCase` is the main application use case.

It coordinates the workflow:

1. scan files;
2. parse paths;
3. create archive candidates;
4. evaluate archive policy;
5. build an archive plan.

The use case does not contain the detailed archive rules itself. It delegates those decisions to the rule policy.

It also does not implement low-level filesystem traversal itself. It depends on a scanner.

### Ports

Ports describe what the application needs without tying the core workflow to one technical implementation.

Current ports include:

- scanner behavior in `scanning/ports.py`;
- archive path builder behavior in `planning/ports.py`;
- rule interfaces in `rules/ports.py`.

This keeps the core code easy to change. For example, a different scanner, archive path strategy, or rule implementation can be introduced without rewriting the use case.

### Infrastructure

`FilesystemScanner` is an infrastructure adapter.

It knows how to walk files on disk. The use case only needs something that can provide file paths.

`DefaultArchivePathBuilder` is also an adapter-like implementation. It applies the current destination path strategy by placing planned archive paths under the configured archive root.

### CLI as delivery mechanism

The `cli` package is the delivery mechanism.

It is responsible for:

- parsing command-line arguments;
- wiring concrete implementations together;
- running the use case;
- printing JSON.

The CLI does not contain the archive policy itself. It assembles the policy and hands control to the application use case.
