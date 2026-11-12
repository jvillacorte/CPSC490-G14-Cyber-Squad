# Cyber Sandbox prototype

This offline proof of concept opens a PySide6 start menu and validates one
predefined scenario with Pydantic. Start the scenario, select a simulated file
to inspect its contents, navigate into virtual directories, create a simulated
text file, and confirm deletion to remove it from the in-memory state. Return
to the start screen and start again to restore the sample. Simulated paths are
data; these actions do not operate on host files.

## Setup and run

From a clean clone, using Python 3.10–3.13:

```bash
cd prototype
python -m venv .venv
```

On Debian/Ubuntu, install the Qt runtime libraries before installing Python
dependencies:

```bash
sudo apt-get install libegl1 libgl1
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux or
`.venv\Scripts\activate` in Windows Command Prompt
(`.venv/Scripts/Activate.ps1` in PowerShell), then run:

```bash
python -m pip install -r requirements.txt
python start_simulation.py
```

The application needs a graphical desktop. It does not need an API key or
network connection. `.env.example` records that no configuration is needed yet.
PySide6 is constrained to the 6.8 series, which supports these Python versions.

## Tests

With the same environment active:

```bash
python -m pip install pytest
python -m pytest -q
```

The UI tests use Qt's offscreen platform, so they also run without a display.

## Current limits

The sample schema covers only a title, description, and text files. It is not
the full scenario schema, and this slice does not implement AI generation,
malware behavior, deleting or creating directories, a process manager, network
viewer, objective evaluation, or reports. Action history is held in memory
only. Host isolation for future malware behaviors still needs its own tests;
the included file-operation check covers only this slice.

The [sample scenario](scenario/sample.py) illustrates the supported structure:
nonempty `title` and `description` strings and a nonempty `files` array. Each
file has a unique, absolute normalized virtual `path` and a string `contents`.
Unexpected fields and invalid paths are rejected before the state is replaced.
