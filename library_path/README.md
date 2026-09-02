# Library Path

`library_path` is the first concrete example in this repository.

It shows how a small VFX pipeline library can be organized using the first ideas of Domain-Driven Design, or DDD.

The goal of this package is simple:

> Build valid filesystem paths for shots and assets.

For example, given a project, shot, task, version, work type, and file extension, the library can produce a path such as:
```
text
/show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc
```
This is intentionally a small example. The point is not to build a complete studio path system, but to show how DDD concepts can help keep even simple pipeline code easier to understand, test, and change.

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

DDD encourages us to move the important production concepts and rules into a clear domain model, instead of hiding them inside UI code, string formatting code, or filesystem scripts.

## What this example demonstrates

This package demonstrates a few DDD ideas:

- **Domain concepts** such as project, shot, asset, task, version, and work type.
- **Value Objects** that validate their own data.
- **Application use cases** that coordinate one meaningful action.
- **Infrastructure details** such as path templates.
- **A public API** that hides the internal organization of the package from other tools.

The example is deliberately simple, but the structure is close to what you could use in a larger pipeline codebase.

## The domain language

In this package, the language of the domain is the language of VFX production:

- A **Project** has a code, such as `dragon`.
- A **Sequence** has a code, such as `sq010`.
- A **Shot** belongs to a sequence and has a shot code, such as `sh020`.
- An **Asset** has an asset type and a name, such as `character/dragon`.
- A **Task** describes the department or work area, such as `modeling`, `rigging`, `animation`, or `lighting`.
- A **Version** represents a numbered version and is formatted as `v001`, `v002`, `v003`, and so on.
- A **Work Type** describes whether the path is for work-in-progress data or published data.

These words are not just variable names. They are part of the shared vocabulary of the pipeline.

That shared vocabulary is what DDD calls the **Ubiquitous Language**.

## Domain objects

The domain objects describe the production concepts.

Examples include:

```python
Project(code="dragon")
Sequence(code="sq010")
Shot(sequence=Sequence(code="sq010"), code="sh020")
Task(name="lighting")
Version(number=12)
```

These objects are small, but they already express useful rules.

For example:

- a project code cannot be empty;
- a shot code cannot contain invalid characters;
- a version number must be greater than or equal to `1`;
- a version number knows how to format itself as a label like `v012`.

This is an important DDD idea:

> Production rules should live close to the production concepts they belong to.

The version formatting rule should not be copied into every publishing tool, browser, or command-line script. It belongs to the `Version` concept.

## Value Objects

Most objects in this package are best understood as **Value Objects**.

A Value Object is defined by its values, not by a long-lived identity.

For example, this version:

```python
Version(number=12)
```

does not represent a database row or a tracked production entity. It represents the value `12`, with the domain rule that it is displayed as `v012`.

The same is true for:

```python
Project(code="dragon")
Task(name="lighting")
Sequence(code="sq010")
```

They are small, immutable descriptions of valid production data.

This is useful because Value Objects can protect the rest of the system from invalid data. If a `Version` exists, the rest of the code can trust that its number is valid.

## Entities

In a larger production system, concepts like `Shot`, `Asset`, and `Publish` are often **Entities**.

An Entity has an identity that stays the same over time, even when other details change.

For example, shot `dragon/sq010/sh020` is still the same shot if:

- its frame range changes;
- its status changes;
- its assigned artist changes;
- its latest publish changes.

In this small package, `Shot` and `Asset` are lightweight objects used to build paths. In a larger system, they might become richer Entities connected to tracking data, tasks, publishes, dependencies, or review status.

The important lesson is that the code already uses production concepts instead of passing anonymous dictionaries or loose strings everywhere.

Compare this:

```python
shot = Shot(
    sequence=Sequence(code="sq010"),
    code="sh020",
)
```

with this:

```python
shot = {
    "seq": "sq010",
    "shot_name": "sh020",
}
```

The first version is more explicit. It says what the data means.

## Application use case

The main use case of this package is:

> Build a path.

The application layer coordinates that operation.

It does not represent a production concept itself. Instead, it answers a workflow question:

> Given valid production data, which path should be produced?

A use case is useful because it gives the rest of the software one clear operation to call.

For example:

```python
from library_path.application.build_path import BuildPathUseCase
from library_path.domain.entities import Project, Sequence, Shot, Task, Version, WorkType
from library_path.infrastructure.path_templates import PathTemplates


build_path = BuildPathUseCase(
    templates=PathTemplates.default_vfx_templates(),
)

path = build_path.execute(
    project=Project(code="dragon"),
    entity=Shot(
        sequence=Sequence(code="sq010"),
        code="sh020",
    ),
    task=Task(name="lighting"),
    version=Version(number=12),
    work_type=WorkType.PUBLISH,
    extension="abc",
)

print(path.as_posix())
```

This produces:

```text
/show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc
```

The use case coordinates the operation, but it does not need to know about Maya, Houdini, Qt, ShotGrid, Ftrack, Kitsu, databases, or real files on disk.

That separation is the main architectural lesson.

## Infrastructure

The path templates are treated as infrastructure.

In this example, templates are stored in Python code.

In a real studio, they might come from:

- YAML files;
- JSON files;
- a database;
- ShotGrid;
- Ftrack;
- Kitsu;
- a central pipeline configuration package;
- environment-specific studio settings.

The important idea is that the rest of the application should not care where the templates come from.

Today they can be hard-coded. Tomorrow they can be loaded from a database. The domain objects and use case should not need to be rewritten just because the storage mechanism changed.

Example template:

```text
/show/{project}/sequences/{sequence}/shots/{shot}/{task}/publish/{version}/{name}_{version}.{extension}
```

The template is technical configuration. The production meaning belongs to the domain objects and the use case.

## Public API

The package also exposes a simpler public API for other tools.

Instead of forcing a Maya tool, browser, or archiver to know the internal package structure, it can call a simple function:

```python
from library_path import build_shot_path

path = build_shot_path(
    project="dragon",
    sequence="sq010",
    shot="sh020",
    task="lighting",
    version=12,
    work_type="publish",
    extension="abc",
)

print(path.as_posix())
```

This produces:

```text
/show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc
```

There is also an asset path helper:

```python
from library_path.api import build_asset_path

path = build_asset_path(
    project="dragon",
    asset_type="character",
    asset="wyvern",
    task="modeling",
    version=3,
    work_type="work",
    extension="ma",
)

print(path.as_posix())
```

Example output:

```text
/show/dragon/assets/character/wyvern/modeling/work/v003/dragon_character_wyvern_modeling_v003.ma
```

This API is useful because external tools do not need to know about use cases, template classes, or internal folders.

They only need to know what they want to do.

## Layer responsibilities

This package follows a simple layered structure:

```text
library_path/
├── domain/
├── application/
├── infrastructure/
└── api.py
```

### Domain layer

The domain layer contains the production concepts and rules.

This is where concepts like these belong:

- project;
- sequence;
- shot;
- asset;
- task;
- version;
- work type;
- validation errors.

The domain layer should not depend on Maya, Houdini, Qt, a database, a web framework, or a specific filesystem implementation.

### Application layer

The application layer contains use cases.

In this package, the main use case is building a path.

The application layer coordinates the workflow:

1. receive valid domain objects;
2. ask for the correct template;
3. prepare template values;
4. render the final path.

It should contain orchestration logic, not low-level UI or database code.

### Infrastructure layer

The infrastructure layer contains technical details.

In this package, path templates live here.

In a larger system, this layer might also contain:

- filesystem adapters;
- database repositories;
- ShotGrid clients;
- Ftrack clients;
- Kitsu clients;
- studio configuration loaders;
- environment variable readers.

Infrastructure is where the outside world is connected to the application.

### API module

The API module is a small public entry point.

It lets external tools use the package without depending on its internal structure.

This is useful when the library is consumed by many different tools:

- a publishing tool;
- a file browser;
- a loader;
- an archiver;
- a command-line utility;
- a DCC integration.

## Why not just format strings directly?

For a very small script, this might seem enough:

```python
path = f"/show/{project}/sequences/{sequence}/shots/{shot}/{task}/publish/v{version:03d}/{name}.abc"
```

That is fine for a quick one-off script.

But in production, this logic tends to grow:

- validation rules are added;
- more asset types appear;
- departments need different paths;
- work and publish paths diverge;
- shows require custom naming conventions;
- delivery paths differ from internal paths;
- tools need to support multiple studios or projects.

If every tool formats paths manually, the pipeline becomes hard to change.

The DDD-inspired structure gives the rules a clear home.

## What to notice as a TD or developer

When reading or extending this package, ask:

- Does this rule belong to the domain?
- Is this a use case, or just a technical detail?
- Am I passing meaningful objects, or loose strings and dictionaries?
- Could this code still work if the UI changed?
- Could this code still work if templates came from JSON instead of Python?
- Could this code be reused in Maya, Houdini, a CLI, and a web service?
- Is the production language visible in the code?

If the answer is yes, the design is moving in a useful direction.

## Possible exercises

To continue learning from this example, try adding one small feature at a time.

Possible exercises:

1. Add a new `WorkType`, such as `review` or `delivery`.
2. Add validation for file extensions.
3. Add support for sequence-level paths.
4. Load path templates from a JSON file.
5. Add show-specific path templates.
6. Add a use case that returns the folder path without the filename.
7. Add a use case that builds the next available version.
8. Add tests for invalid project names and invalid version numbers.
9. Add a CLI wrapper around the public API.
10. Use the same library from another package, such as a browser or archiver.

Each exercise should preserve the same principle:

> Keep production rules in the core, and keep technical details at the edges.
