# The outer world

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

Today they can be hard-coded. Tomorrow they can be loaded from a database. The domain objects and use case should not
need to be rewritten just because the storage mechanism changed.

Example template:

```text
/show/{project}/sequences/{sequence}/shots/{shot}/{task}/publish/{version}/{name}_{version}.{extension}
```

The template is technical configuration. The production meaning belongs to the domain objects and the use case.

## Public API

The package also exposes a simpler public API for other tools.

This API is useful because external tools do not need to know about use cases, template classes, or internal folders.

They only need to create a `LibraryPath` instance and call methods for the operation they want to perform.

A tool can use the default VFX templates:

```python
from library_path import LibraryPath

library_path = LibraryPath.default()
```

Or it can create an instance from explicit templates:

```python
from library_path import LibraryPath
from library_path.infrastructure.path_templates import PathTemplates

library_path = LibraryPath.from_templates(
    PathTemplates.a_way_to_create_templates(),
)
```

### Building

Instead of forcing a Maya tool, browser, or archiver to know the internal package structure, it can call a method on the
public API object:

```python
from library_path import LibraryPath

library_path = LibraryPath.default()

path = library_path.build_shot_path(
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
show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/dragon_sq010_sh020_lighting_v012.abc
```

There is also an asset path method:

```python
from library_path import LibraryPath

library_path = LibraryPath.default()

path = library_path.build_asset_path(
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

### Parsing

The public API can also parse a known library path back into domain data:

```python
from library_path import LibraryPath

library_path = LibraryPath.default()

parsed = library_path.parse_path(
    "show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/"
    "dragon_sq010_sh020_lighting_v012.abc"
)

print(parsed.project.code)
print(parsed.entity.code)
print(parsed.task.name)
print(parsed.version.label)
print(parsed.work_type.value)
print(parsed.extension)
```

Example output:

```text
dragon
sh020
lighting
v012
publish
abc
```

The returned value is a `ParsedPath`.

`ParsedPath` is a small aggregate-style object: it keeps the parsed project, entity, task, version, work type, and
extension together as one result, instead of returning a loose dictionary of strings.