# Library Path

`library_path` is the first concrete example in this repository.

It shows how a small VFX pipeline library can be organized using the first ideas of Domain-Driven Design, or DDD.

The goal of this package is simple:

> Build valid filesystem paths for shots and assets, and parse known library paths back into production data.

For example, given a project, shot, task, version, work type, and file extension, the library can produce a path such
as:

```text
/show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc
```

This is intentionally a small example. The point is not to build a complete studio path system, but to show how DDD
concepts can help keep even simple pipeline code easier to understand, test, and change.

## Why path building is a good first example

Every VFX pipeline has path logic.

TDs and developers often need to answer questions like:

- Where should a Maya work file live?
- Where should a published Alembic cache be written?
- What does a valid shot name look like?
- How should versions be formatted?
- Is this an asset path or a shot path?
- Does the tool need a work path or a publish path?

It is easy for this logic to become scattered across many tools:

- Maya scripts;
- Houdini tools;
- Nuke gizmos;
- publishing tools;
- browser tools;
- archiving scripts;
- render farm submission code;
- asset manager integrations.

When path rules are duplicated everywhere, changing the naming convention becomes risky.

DDD encourages us to move the important production concepts and rules into a clear domain model, instead of hiding them
inside UI code, string formatting code, or filesystem scripts.

## What this example demonstrates

This package demonstrates a few DDD ideas:

- **Domain concepts** such as project, shot, asset, task, version, and work type.
- **Value Objects** that validate their own data.
- **Application use cases** that coordinate one meaningful action.
- **Infrastructure details** such as path templates.
- **A public API** that hides the internal organization of the package from other tools.
- **Round-tripping path data** by building paths from domain objects and parsing valid paths back into domain objects.

The example is deliberately simple, but the structure is close to what you could use in a larger pipeline codebase.

## The domain language

In this package, the language of the domain is the language of VFX production:

- A **Project** has a code, such as `dragon`.
- A **Sequence** has a code, such as `sq010`.
- A **Shot** belongs to a sequence and has a shot code, such as `sh020`.
- An **Asset** has an asset type and a name, such as asset type `character` and name `dragon`.
- A **Task** describes the department or work area, such as `modeling`, `rigging`, `animation`, or `lighting`.
- A **Version** represents a numbered version and is formatted as `v001`, `v002`, `v003`, and so on.
- A **Work Type** describes whether the path is for work-in-progress data or published data.

These words are not just variable names. They are part of the shared vocabulary of the pipeline.

That shared vocabulary is what DDD calls the **Ubiquitous Language**.

## Detailed explanations

The following pages explain the concepts in more detail.

**[Objects](docs/objects.md)**

- Domain Objects
- Value Objects
- Entities
- Aggregates

**[Application use cases](docs/application-use-cases.md)**

- Build a Path
- Parse a Path

**[Layer responsibilities](docs/layer-responsibilities.md)**

- Domain
- Application
- Infrastructure
- API

**[The outer world](docs/the-outer-world.md)**

- Infrastructure
- Public API

**[Further considerations](docs/further-considerations.md)**

- Why not just format strings directly?
- What to notice as a TD or developer
- Possible exercises
