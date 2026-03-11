---
name: list-vasanas
description: Show available Vasanas in the library
---

# List Vasanas Command

List all available Vasanas in `skills/library/`.

## Output Format:

For each Vasana found, show:

```
## [Vasana Name]
**Description:** [From frontmatter description field]
**Location:** skills/library/[name]/SKILL.md

---
```

## After listing:

Suggest next actions:
- `/create-vasana [name]` to create a new one
- `/test-vasana [name]` to test one
- Read any Vasana file to see full pattern description
