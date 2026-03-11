---
name: record-vasana
description: Record a new Vasana from observed interaction pattern (renamed from create-vasana to emphasize capturing emergent patterns, not creating from scratch)
arguments:
  - name: name
    required: false
    description: Name for the new Vasana (optional - will prompt if not provided)
---

# Record Vasana Command

**Renamed from `/create-vasana`**: Emphasizes that Vasanas are **recorded** (like music), not created theoretically.


Use the `vasana-creator` skill to record a new Vasana.

## If name provided:
Create a Vasana named `$ARGUMENTS.name` based on the current conversation or a pattern the user describes.

## If no name:
Ask the user to describe the interaction pattern they want to capture, then suggest an appropriate name.

## Process:
1. Identify the pattern (what interaction produced value?)
2. Name it (active, descriptive)
3. Describe the pattern (conditions, moves, what makes it work)
4. Add testing notes
5. Include propagation section (REQUIRED)
6. Save to `skills/library/[name]/SKILL.md`

## Output:
- Show the created Vasana
- Remind user to test it before relying on it
- Suggest `/test-vasana [name]` as next step
