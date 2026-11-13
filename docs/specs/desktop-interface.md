# Specification — Desktop Interface

> Epic: #22 · Story: #24
> Owner: NguyenVGH · Status: draft
> Related specification: [training environment](training-environment.md)

## Intended interface

The simulated desktop is to contain a file explorer, process manager, system
log viewer, and network activity viewer. Users should be able to select each
view and switch between them without closing or restarting the application.
The views must represent simulated state, not the host computer's files,
processes, logs, or network activity. Story #24 contains the acceptance
criteria; the training-environment specification describes each capability.

## Current prototype

The maintained interface is implemented with PySide6 in
[`prototype/ui/window.py`](../../prototype/ui/window.py), consistent with
the [architecture](../design/architecture.md). An earlier Tkinter sketch was
only a concept and is not the current implementation.

The start screen starts the sample scenario or loads a selected JSON file.
The scenario screen displays simulated files, supports directory navigation,
file inspection, creation and confirmed deletion, and returns to the start
screen. Starting or loading a scenario creates fresh in-memory state.
See the [prototype README](../../prototype/README.md) for setup and limits.

The process manager, system log viewer, network activity viewer, and switching
among those desktop components are not yet implemented. The current file view
does not by itself satisfy all of story #24.
