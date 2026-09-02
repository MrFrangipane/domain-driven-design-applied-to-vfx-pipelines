# Application use cases

The main use cases of this package are:

> Build a path.

and:

> Parse a known path.

The application layer coordinates these operations.

It does not represent a production concept itself. Instead, it answers workflow questions:

> Given valid production data, which path should be produced?

and:

> Given a path that matches our templates, what production data does it describe?

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

The use case coordinates the operation, but it does not need to know about Maya, Houdini, Qt, ShotGrid, Ftrack, Kitsu,
databases, or real files on disk.

That separation is the main architectural lesson.
