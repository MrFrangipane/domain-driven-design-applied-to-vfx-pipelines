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
├── docs/
│   └── quick-summary.md    a quick introduction to DDD
├── example-projects/
│   ├── library_path/       a first example of basic DDD principles
│   ├── archiver/           dive more into ports and adapters
│   └── browser/            ...
└── README.md               this file
```

### [Quick summary: Domain-Driven Design](docs/quick-summary.md)

[A document](docs/quick-summary.md) that introduces the following concepts:

- Domain-Driven Design
- Ubiquitous Language
- Entities and Value Objects
- Aggregates
- Bounded Contexts
- Application, domain, infrastructure, and presentation layers

### [First example: A Path Library](example-projects/library_path/)

[A Python project](example-projects/library_path/) that contains code examples that demonstrates how to separate production
concepts and rules from UI, filesystem, and external service concerns.

The examples are organized to show how these parts can be separated, ensuring that production rules do not get buried
inside UI or infrastructure code.

### [Second example: A CLI tool for archiving](example-projects/archiver/)

[A Python project](example-projects/archiver/) that contains code examples that demonstrates ...
