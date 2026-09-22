# Archiver

`archiver` is the second concrete example in this repository.

It shows a small DDD-style command-line application that scans a folder, parses files with `pipeline_path`, evaluates archive rules, and produces an **archive plan**.

The current implementation only builds and prints the plan. It does not move, copy, delete, or mutate files on disk.

## Folder structure

```plain text
archiver/
  application/
    __init__.py
    build_archive_plan.py

  cli/
    __init__.py
    main.py

  planning/
    __init__.py
    entities.py
    path_builders.py
    ports.py

  rules/
    __init__.py
    archive_policy.py
    archive_rules.py
    decision_resolver.py
    entities.py
    ports.py

  scanning/
    __init__.py
    filesystem.py
    ports.py

__init__.py
```

### Note regarding DDD and folder structures

Unlike `pipeline_path`, `archiver` is organized by workflow area instead of by technical layer.

This is intentional.

`pipeline_path` is small enough that domain/application/infrastructure folders are easy to see. 
Archiver has several related subdomains: scanning, rules, and planning. Each folder contains the entities, ports,
and implementations that belong to that area.

The same dependency rule still applies:
- CLI is outside.
- Filesystem scanning is infrastructure-like.
- Archive rules and planning objects are core application/domain concepts.
- The use case coordinates the workflow.

## Core idea

The workflow is:

1. The CLI receives a root folder.
2. The scanning use case walks all files under that folder.
3. Each file is parsed using `pipeline_path`.
4. Files that do not match known pipeline path templates are skipped.
5. Parsed files become archive candidates.
6. Archive rules mark candidates as archivable or not archivable.
7. The decision resolver combines rule results into final decisions.
8. Archivable candidates are converted into archive plan items.
9. The plan is printed as JSON.

The output contains:

- `count`: number of files planned for archiving;
- `items`: planned archive actions;
- `source_path`: original file path;
- `archive_path`: planned destination path;
- `reasons`: rule explanations that contributed to the decision.

## Running the example

From the `example-projects/archiver` folder:

```bash
uv run archiver <root-folder-to-scan>
```

Example:

```bash
uv run archiver ./example-files
```

The command prints JSON similar to:

```json
{
  "count": 1,
  "items": [
    {
      "source_path": "show/dragon/sequences/sq010/shots/sh020/lighting/work/v001/file.ma",
      "archive_path": "archives/show/dragon/sequences/sq010/shots/sh020/lighting/work/v001/file.ma",
      "reasons": [
        "Is of Work type",
        "One of the latest 2 versions in its version family."
      ]
    }
  ]
}
```

## Current archive policy

The default CLI wiring uses these rules:

### `ArchiveWorkFilesRule`

This is a **single-candidate** rule.

It marks candidates as archivable only when their parsed `pipeline_path` work type is `WorkType.WORK`.

Non-work files are marked as `DO_NOT_ARCHIVE`.

### `KeepLastVersionsRule`

This is a **collection** rule.

It groups candidates by their `VersionFamilyKey` and marks candidates according to version order.

The current CLI configuration keeps `2` versions per version family.

### Conflict resolution

Rules express intent, but they do not directly perform archive actions.

`ArchiveDecisionResolver` combines all rule decisions using this strategy:

- a candidate is archived only if at least one rule marks it `ARCHIVABLE`;
- a candidate is not archived if any rule marks it `DO_NOT_ARCHIVE`;
- `DO_NOT_ARCHIVE` wins over `ARCHIVABLE`.

If the final decision is to archive a candidate, the resolver asks an archive path builder to create the planned destination path.

## Package responsibilities

```plain text
application/
  Application use case that coordinates scanning files, evaluating rules,
  resolving archive decisions, and building the archive plan.

cli/
  Command-line entry point and dependency wiring.

scanning/
  File discovery interfaces and filesystem implementation.

rules/
  Archive candidate objects, rule interfaces, rule implementations,
  archive policy, and decision resolution.

planning/
  Archive plan objects and archive destination path building.
```

## More on Domain Driven Design

For further information about the Domain Driven Design approach used in this project, see:

### [DDD Mapping](docs/ddd-mapping.md)

A [document](docs/ddd-mapping.md) that maps the Archiver's classes to the DDD concepts.

### [Relationship to `pipeline_path`](docs/relationship-to-pipeline-path.md)

A [document](docs/relationship-to-pipeline-path.md) that explains the relationship between the `pipeline_path` and the Archiver.
