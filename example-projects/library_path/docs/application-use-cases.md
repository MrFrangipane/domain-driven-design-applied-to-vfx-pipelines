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

## Building a path

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

## Parsing a path

The opposite operation is parsing a known path back into production data:

```python
from library_path.application.parse_path import ParsePathUseCase
from library_path.infrastructure.path_templates import PathTemplates
from library_path.infrastructure.template_path_parser import TemplatePathParser


templates = PathTemplates.default_vfx_templates()

parse_path = ParsePathUseCase(
    parser=TemplatePathParser(templates=templates),
)

parsed_path = parse_path.execute(
    "/show/dragon/sequences/sq010/shots/sh020/"
    "lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc"
)

print(parsed_path.project.code)
print(parsed_path.entity.sequence.code)
print(parsed_path.entity.code)
print(parsed_path.task.name)
print(parsed_path.version.label)
print(parsed_path.work_type.value)
print(parsed_path.extension)
```

This produces:

```text
dragon
sq010
sh020
lighting
v012
publish
abc
```

The parser first matches the path against the configured templates.  
Then the use case turns the captured values into domain objects such as `Project`, `Shot`, `Task`, and `Version`.

The same use case also works for asset paths:

```python
parsed_path = parse_path.execute(
    "/show/dragon/assets/character/wyvern/"
    "model/work/v003/dragon_character_wyvern_model_v003.ma"
)

print(parsed_path.project.code)
print(parsed_path.entity.asset_type)
print(parsed_path.entity.name)
print(parsed_path.task.name)
print(parsed_path.version.label)
print(parsed_path.work_type.value)
print(parsed_path.extension)
```

This produces:

```text
dragon
character
wyvern
model
v003
work
ma
```

The use case coordinates the operation, but it does not need to know about Maya, Houdini, Qt, ShotGrid, Ftrack, Kitsu,
databases, or real files on disk.

That separation is the main architectural lesson.
