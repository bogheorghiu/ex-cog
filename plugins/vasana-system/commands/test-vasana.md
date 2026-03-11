---
name: test-vasana
description: Run tests on a Vasana
arguments:
  - name: name
    required: false
    description: Name of the Vasana to test (optional - will list available if not provided)
---

# Test Vasana Command

Use the `vasana-tester` skill to test a Vasana.

## If name provided:
Run tests on the Vasana at `skills/library/$ARGUMENTS.name/SKILL.md`

## If no name:
List available Vasanas in `skills/library/` and ask which one to test.

## Test Process:
1. **Trigger test:** Do conditions match what invokes this Vasana?
2. **Pattern emergence test:** When invoked, does the dance happen?
3. **Propagation test:** Is the propagation section present and correct?
4. **Value assessment:** Gather any available signals of usefulness

## Output:
- Pass/fail for each testable aspect
- Honest notes on what can't be objectively tested
- Recommendations for improvement if issues found
