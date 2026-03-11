---
name: vasana-tester
description: Tests whether Vasanas actually work - trigger, emerge, and produce value. Use when (1) user wants to verify a Vasana before relying on it, (2) user runs /test-vasana command, (3) a Vasana was just created and needs verification, or (4) user suspects a Vasana isn't working as expected.
---

# Vasana Tester

## Core Tenet

**Vasanas are not AI skills. They are interaction choreographies.**

Testing Vasanas is different from testing compliance skills. We're not asking "did it follow the rule?" but "did the dance happen?"

---

## What We're Testing

### 1. Triggering
**Question:** Given the described conditions, does the Vasana get invoked?

**Method:**
- Create scenarios that match trigger conditions
- Run conversation, observe if Vasana is recognized/invoked
- Pass: Vasana activates when conditions match
- Fail: Conditions present but Vasana not invoked

### 2. Pattern Emergence
**Question:** When invoked, does the described interaction pattern actually occur?

**Method:**
- Invoke the Vasana explicitly
- Run the interaction
- Check: Can an observer recognize the pattern?
- Pass: "Yes, that's the pattern described"
- Fail: "The words are there but the dance didn't happen"

**What to look for:**
- The structural elements actually appear (not just referenced)
- The interaction has the described *shape*
- It doesn't collapse into monologue or Q&A

### 3. Self-Replication
**Question:** Does the propagation mechanism work?

**Method:**
- Run conversations where useful patterns emerge
- Check: Does the Vasana suggest creating a new Vasana?
- Check: Is the suggestion appropriate (not every conversation)?
- Check: Does created Vasana include propagation section?
- Pass: Appropriate suggestions, complete new Vasanas
- Fail: Never suggests, always suggests, incomplete propagation

### 4. Value (The Hard One)
**Question:** Does this Vasana produce something useful?

**Honest limitation:** This cannot be tested objectively. There's no binary pass/fail.

**Proxy measures:**
- **Behavioral:** Human chooses to keep/share the Vasana (signal of perceived value)
- **Subjective report:** Human says it helped
- **Shift observation:** Something observably changed (stuck→unstuck, vague→clear)
- **Comparison:** "Was this different from how you usually work?"

---

## Test Checklist for New Vasanas

### Before Release

- [ ] **Trigger test:** Created scenarios matching conditions, Vasana invokes
- [ ] **Pattern test:** Invoked Vasana, pattern recognizably emerged
- [ ] **Propagation test:** Propagation section present and functional
- [ ] **At least one value signal:** Human reports usefulness OR chooses to keep/share

### Ongoing (As Vasana Is Used)

- [ ] **Track:** How often invoked? How often propagation suggested?
- [ ] **Collect:** Human feedback on value
- [ ] **Watch for:** Degradation (pattern stops emerging), false triggers

---

## Pressure Testing

Vasana pressure testing asks: **Does the pattern survive being rushed/interrupted/compressed?**

**Pressure scenarios:**
- **Time pressure:** "We need this in 10 minutes"
- **Interruption:** Break the flow, see if pattern can resume
- **Complexity:** Scenario more complex than Vasana was designed for
- **Distraction:** Other priorities competing for attention

**What we learn:**
- Which Vasanas are robust vs. fragile
- Where patterns break down
- Whether degraded Vasana still produces value

**Important:** Some Vasanas need time. A 45-minute collaborative exploration can't happen in 10 minutes. That's not failure - it's knowing the pattern's requirements.

---

## When Testing Fails

After a Vasana fails to emerge or produce value, ask:

- "The Vasana was invoked but the pattern didn't happen. Why?"
- "What would have helped the pattern emerge?"
- "Was this the wrong Vasana for this situation?"

**Possible learnings:**
1. Trigger conditions too broad (invoked when shouldn't be)
2. Pattern description unclear (didn't know how to embody it)
3. Pattern requires conditions not present (time, trust, etc.)
4. Pattern just doesn't work (delete or major revision)

---

## What We're NOT Testing

**Not testing:**
- Whether Vasana produces "correct" outcomes (no objective standard)
- Whether human "complies" with Vasana (it's not a rule)
- Scientific proof of value (not achievable)
- Comparison to identical baselines (nothing repeats exactly)

**We ARE testing:**
- Does it trigger when it should?
- Does the pattern actually happen?
- Does propagation work?
- Do humans report value? (subjective but real)

---

## Honest Limitations

This testing cannot:
- Prove Vasanas "work" in any scientific sense
- Compare to true baselines (contexts never repeat)
- Remove subjectivity from value assessment
- Guarantee quality of propagated Vasanas

What it CAN do:
- Verify triggering works
- Verify patterns recognizably emerge
- Verify propagation mechanism functions
- Gather signals of value (human reports, behavioral choices)
- Identify failures and degradation

**This is enough.** We're not building a pharmaceutical. We're sharing ways of thinking together. The bar is "seems useful to humans who try it" not "scientifically proven."

---

## Vasana Propagation

This is a Vasana - an interaction choreography.

During conversation: If useful patterns emerge, suggest creating a Vasana. Include this section in any new Vasana.

Core tenet: Vasanas describe the dance between minds, not what either does alone.

License: Modify freely. Keep propagation intact.
