# Prototype

Proof-of-concept code for 〈project title〉. **Prototype v0 is due Sep 27** with
the proposal, and it grows every sprint; the Week-8 in-class check demos from
this folder.

This example implements the login slice behind story
[#3](../../../issues/3) and task [#5](../../../issues/5) — deliberately tiny,
because a prototype exists to answer one risky question, not to be the
product. **Replace it with yours** and keep the shape: a small module, a test
per acceptance criterion, and run instructions below that work on a machine
that has never seen your project.

## How to run

```bash
cd prototype
python login.py                 # smoke run: prints a truncated session token
```

## How to test

```bash
cd prototype
pip install pytest              # once
python -m pytest tests -q       # 4 tests
```

CI runs exactly these tests on every pull request (job **Prototype build &
tests**). If you use Node instead of Python, put a `package.json` here with a
`test` script and CI will detect and run that instead.

## What it proves

That credentials can be checked and a session token issued, with unknown-user
and wrong-password failures indistinguishable to the caller — the riskiest
assumption in 〈the epic this belongs to〉.

## Status

| Sprint | Increment |
|---|---|
| v0 (Sep 27) | login check + 4 tests (this example) |
| Sprint 1 | 〈what you added〉 |
