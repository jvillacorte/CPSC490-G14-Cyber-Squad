# Prototype

Proof-of-concept code for Cyber-Squad Incident-Response Training Simulator. 

This example implements the Simulated Desktop
[#3](../../../issues/32) — deliberately tiny,
because a prototype exists to answer one risky question, not to be the
product. Create a simple PySide interface that (once implemented) allows
a user to start a malware training simulation.

## How to run

```bash
cd prototype
python start_simulation.py                 # smoke run: prints a truncated session token
```

## How to test

```bash
cd prototype
pip install pytest              # once
python -m pytest tests -q       # 4 tests
```

CI runs exactly these tests on every pull request (job **Prototype build &
tests**).

## What it proves

That a menu for starting, configuring, and monitoring a simulated desktop environment can
be created sanely.

## Status

| Sprint | Increment |
|---|---|
| Sprint 2 (v0) | Outline wireframe for main menu |
