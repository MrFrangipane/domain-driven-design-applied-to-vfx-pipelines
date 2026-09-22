## Relationship to `pipeline_path`

`archiver` uses `pipeline_path` as an upstream domain library.

That means `pipeline_path` owns a separate but related domain: **pipeline path identity**.

Its job is to understand studio path conventions and turn paths into meaningful production concepts, such as:

- project;
- sequence;
- shot;
- asset;
- task;
- version;
- work type;
- version family;
- file extension.

`archiver` does not duplicate those concepts or re-parse paths manually. Instead, it asks `pipeline_path` to parse a discovered file path. If the path matches a known pipeline template, `pipeline_path` returns a parsed domain object. If the path does not match, `archiver` skips it.

This creates a clean domain relationship:

```plain text
filesystem path
  -> pipeline_path domain
  -> parsed production identity
  -> archiver domain
  -> archive candidate
  -> archive decision
  -> archive plan
```

### Upstream domain ownership

`pipeline_path` is upstream because it defines the source language for path meaning.

For example, the question:

> What production file does this path represent?

belongs to `pipeline_path`.

It knows whether a path describes:

- a shot or an asset;
- a work file or publish file;
- a specific task;
- a specific version;
- a member of a version family.

The archiver should not answer those questions itself. If it did, the same path rules would be copied into multiple tools, and every tool would need to change when the studio path convention changes.

Instead, `pipeline_path` provides a stable interpretation of the path, and `archiver` builds its own behavior on top of that interpretation.

### Archiver domain ownership

`archiver` owns a different domain: **archive planning**.

Its questions are:

- Is this parsed file an archive candidate?
- Which archive rules apply to it?
- Should the file be archived?
- Why or why not?
- What archive destination should be planned?
- What should the final archive plan contain?

Those questions belong to the archiver, not to `pipeline_path`.

For example, `pipeline_path` may say:

> This file is a work file for version `v012` of a lighting task.

The archiver may then say:

> Work files can be considered for archiving, but the latest two versions in each version family should be protected.

The first statement is path-domain knowledge. The second statement is archive-domain knowledge.

### How `pipeline_path` domain objects are used

The archiver wraps parsed path information in its own domain object: an archive candidate.

An archive candidate combines:

- the original source path from the filesystem;
- the parsed production identity from `pipeline_path`.

That candidate then becomes the input to archive rules.

This is important because archive rules can speak in production terms instead of string manipulation terms.

For example, a rule can ask:

- Is this candidate a work file?
- What version is it?
- Which version family does it belong to?
- Is it one of the latest versions in that family?

Without `pipeline_path`, the archiver would need to infer those answers by splitting strings, matching folder names, and formatting version labels itself. That would blur the boundary between path parsing and archive planning.

### Shared language without shared responsibility

The two packages share some vocabulary, but they do not have the same responsibility.

`pipeline_path` vocabulary:

- `Project`;
- `Shot`;
- `Asset`;
- `Task`;
- `Version`;
- `WorkType`;
- `ParsedPath`;
- `VersionFamilyKey`.

`archiver` vocabulary:

- `ArchiveCandidate`;
- `ArchiveMark`;
- `ArchiveDecision`;
- `ResolvedArchiveDecision`;
- `ArchivePlanItem`;
- `ArchivePlan`;
- archive rules;
- archive path builders.

The archiver uses `pipeline_path` concepts as input, but it does not own their validation or construction rules.

For example:

- version number formatting belongs to `pipeline_path`;
- deciding whether an old work version should be archived belongs to `archiver`;
- identifying a path as a publish path belongs to `pipeline_path`;
- deciding that publish files should not be archived belongs to `archiver`.

### Why this boundary matters

This boundary keeps both domains easier to change.

If the studio changes path templates, that change should mostly affect `pipeline_path`.

If the studio changes archive policy, such as keeping three versions instead of two, that change should affect `archiver`.

The result is a dependency direction like this:

```plain text
archiver -> pipeline_path
```

`archiver` depends on `pipeline_path` because it needs interpreted path data.

`pipeline_path` does not depend on `archiver` because path parsing should be useful to many tools, not just the archiver.

The same upstream library could also be used by:

- a publishing tool;
- a file browser;
- a loader;
- a validation tool;
- a DCC integration;
- another command-line utility.

Each downstream tool can build its own domain behavior using the same path-domain objects.

### DDD interpretation

In DDD terms, `pipeline_path` and `archiver` are separate bounded contexts.

`pipeline_path` is the bounded context for path identity and path rules.

`archiver` is the bounded context for archive policy and archive planning.

The parsed path object acts as the handoff between the two contexts. It translates a raw technical input, a filesystem path, into production language that the archiver can safely use.

This keeps the archiver focused on archive decisions instead of low-level parsing details.
