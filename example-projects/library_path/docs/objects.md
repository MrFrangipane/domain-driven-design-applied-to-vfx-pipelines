# Objects

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

The package also includes `ParsedPath`, which represents the result of reading a known library path back into these
domain objects.

These objects are small, but they already express useful rules.

For example:

- a project code cannot be empty;
- a shot code cannot contain invalid characters;
- a version number must be greater than or equal to `1`;
- a version number knows how to format itself as a label like `v012`.

This is an important DDD idea:

> Production rules should live close to the production concepts they belong to.

The version formatting rule should not be copied into every publishing tool, browser, or command-line script. It 
belongs to the `Version` concept.

## Value Objects

Most objects in this package are best understood as **Value Objects**.

A Value Object is defined by its values, not by a long-lived identity.

For example, this version:

```python
Version(number=12)
```

does not represent a database row or a tracked production entity. It represents the value `12`, with the domain rule
that it is displayed as `v012`.

The same is true for:

```python
Project(code="dragon")
Task(name="lighting")
Sequence(code="sq010")
```

They are small, immutable descriptions of valid production data.

This is useful because Value Objects can protect the rest of the system from invalid data. If a `Version` exists,
the rest of the code can trust that its number is valid.

## Entities

In a larger production system, concepts like `Shot`, `Asset`, and `Publish` are often **Entities**.

An Entity has an identity that stays the same over time, even when other details change.

For example, shot `dragon/sq010/sh020` is still the same shot if:

- its frame range changes;
- its status changes;
- its assigned artist changes;
- its latest publish changes.

In this small package, `Shot` and `Asset` are lightweight objects used to build paths. In a larger system, they might
become richer Entities connected to tracking data, tasks, publishes, dependencies, or review status.

The important lesson is that the code already uses production concepts instead of passing anonymous dictionaries or 
loose strings everywhere.

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

## Aggregates

Another useful DDD idea is an **Aggregate**.

An Aggregate is a group of related domain objects that are treated as one meaningful whole.

In this package, `ParsedPath` is a small example:

```python
parsed = parse_path(
    "/show/dragon/sequences/sq010/shots/sh020/lighting/publish/v012/"
    "dragon_sq010_sh020_lighting_v012.abc"
)
```

The result contains the production data described by that path:

```python
parsed.project
parsed.entity
parsed.task
parsed.version
parsed.work_type
parsed.extension
```

Instead of returning a loose dictionary like this:

```python
{
    "project": "dragon",
    "sequence": "sq010",
    "shot": "sh020",
    "task": "lighting",
    "version": "v012",
    "work_type": "publish",
    "extension": "abc",
}
```

the package returns one object that keeps the related domain data together.

That object is useful because the rest of the tool can pass around one meaningful result:

```python
parsed.project.code
parsed.entity.code
parsed.task.name
parsed.version.label
```

For this small example, `ParsedPath` is not a complex business object. It does not talk to a database, save itself, or
manage a long lifecycle.

It simply shows the aggregate idea in a lightweight way:

> When several domain objects belong together for one operation, model that group explicitly.