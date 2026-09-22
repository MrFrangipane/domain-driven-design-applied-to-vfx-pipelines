# Domain-Driven Design Applied to VFX Pipelines

This repository demonstrates how Domain-Driven Design, or DDD, can be applied to VFX pipeline tools.

The README introduces the main ideas and vocabulary. The actual example is in the code, where you can see how production 
concepts are separated from UI, filesystem, and external service concerns.

## How to read this repository

You do not need to fully understand DDD before reading the code.

The important idea is to look for separation between:

- production concepts and rules;
- use cases;
- user interfaces;
- technical details such as filesystems, databases, DCC APIs, render farms, or asset trackers.

The code examples show how these parts can be organized so that production rules do not get buried inside UI or 
infrastructure code.

## Contents

The repository is organized as follows:

```text
domain-driven-design-applied-to-vfx-pipelines/
├── demo-folder-structure/  a demo folder structure for a project
│   └── ...
├── docs/
│   └── quick-summary.md    a quick introduction to DDD
├── example-projects/
│   ├── pipeline_path/       a first example of basic DDD principles
│   ├── archiver/           dive more into ports and adapters
│   └── browser/            ...
└── README.md               this file
```

### 0. [Quick summary: Domain-Driven Design](docs/quick-summary.md)

[A document](docs/quick-summary.md) that suggests a team workflow and introduces the following concepts:

- Domain-Driven Design
- Ubiquitous Language
- Entities and Value Objects
- Aggregates
- Bounded Contexts
- Application, domain, infrastructure, and presentation layers

### 1. [First example: A Path Library](example-projects/pipeline_path/)

[A Python library](example-projects/pipeline_path/) that teaches the basic layered package shape:
- `domain/`
- `application/`
- `infrastructure/`
- `api.py`

This example is intentionally small. It uses pipeline paths as a familiar production concept to show how DDD separates
the meaning of the work from the technical details of string formatting and parsing.

In DDD terms, `pipeline_path` is a first bounded context: it defines the language of projects, shots, assets, tasks,
versions, and work types. The goal is not just to build paths, but to make those production concepts explicit in 
the code.

### 2. [Second example: A CLI Archiver](example-projects/archiver/)

[A Python project](example-projects/archiver/) that teaches a slightly more feature-oriented/domain-oriented 
application shape:
- `application/`
- `scanning/`
- `rules/`
- `planning/`
- `cli/`

This example builds on the path library and shows a larger workflow. The archiver is not mainly about moving files; 
it is about deciding which production files are safe or meaningful to archive.

In DDD terms, the archiver introduces another bounded context with its own language: archive candidates, archive rules,
decisions, policies, and archive plans. It shows how an application can coordinate domain rules without hiding those
rules inside command-line, filesystem, or JSON-output code.

### 3. [Third example: A GUI Asset Browser](example-projects/browser/)

[A Python project](example-projects/browser/) that contains code examples that demonstrates ...

### 4. [A demo folder structure](demo-folder-structure/)

[A folder](demo-folder-structure/) and a [README.md](demo-folder-structure/README.md) that shows a demo folder 
structure for a project. That structure is used by the examples in this repository.
