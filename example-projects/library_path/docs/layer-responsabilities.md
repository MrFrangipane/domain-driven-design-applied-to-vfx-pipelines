# Layer responsibilities

This package follows a simple layered structure:

```text
library_path/
├── domain/
├── application/
├── infrastructure/
└── api.py
```

## Domain layer

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

The domain layer should not depend on Maya, Houdini, Qt, a database, a web framework, or a specific filesystem 
implementation.

## Application layer

The application layer contains use cases.

In this package, the main use case is building a path.

The application layer coordinates the workflow:

1. receive valid domain objects;
2. ask for the correct template;
3. prepare template values;
4. render the final path.

It should contain orchestration logic, not low-level UI or database code.

## Infrastructure layer

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

## API module

The API module is a small public entry point.

It lets external tools use the package without depending on its internal structure.

This is useful when the library is consumed by many different tools:

- a publishing tool;
- a file browser;
- a loader;
- an archiver;
- a command-line utility;
- a DCC integration.
