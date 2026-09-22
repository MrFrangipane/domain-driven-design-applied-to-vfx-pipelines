# Further considerations

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
