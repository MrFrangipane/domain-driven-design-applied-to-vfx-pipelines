# Archiver

`archiver` is the second concrete example in this repository.

It shows a clean DDD-style starting point for the **CLI archiver**. It uses `library_path` to parse each discovered file, applies archive rules, and produces an **archive plan** without moving files yet.

Folder structure:

```plain text
archiver/
  analysis/
    __init__.py
    use_cases.py
    infrastructure/
      __init__.py
      filesystem.py

  archive/
    __init__.py
    use_cases.py
    entities.py

  rules/
    __init__.py
    entities.py
    ports.py
    archive_rules.py
    policies.py

  cli/
    __init__.py
    main.py

  __init__.py
```

## Core idea

The workflow is:

1. CLI receives a root folder.
2. Analysis walks all files under that folder.
3. Each file is parsed using `library_path`.
4. Rules decide whether the file should be archived.
5. A plan is produced.
6. The plan is printed as JSON.
