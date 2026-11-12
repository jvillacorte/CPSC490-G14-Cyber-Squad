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
python -m venv ../../cyber-sandbox-venv
```

On Debian/Ubuntu, install the Qt runtime libraries before installing Python
dependencies:

```bash
sudo apt-get install libegl1 libgl1
```

The environment lives outside the repository so repository checks do not scan
it. Activate it with `source ../../cyber-sandbox-venv/bin/activate` on
macOS/Linux or `..\..\cyber-sandbox-venv\Scripts\activate` in Windows Command
Prompt (`..\..\cyber-sandbox-venv\Scripts\Activate.ps1` in PowerShell), then run:

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

## Optional local AI spike

This separate command-line experiment uses a local [Ollama](https://ollama.com/)
server; it does not change the offline GUI or load generated data into the
simulation. Install Ollama, start its local server, and download a model, for
example `ollama pull llama3.2`. Model downloads require internet access and
local storage; performance depends on your hardware. With the prototype's
Python environment active, run:

```bash
python generate_scenario.py --model llama3.2
```

The command sends a fictional-scenario prompt and the current minimal Pydantic
JSON schema to `http://127.0.0.1:11434/api/chat`. It prints the validated
scenario as JSON, or reports an error to standard error and exits nonzero if
the server is unavailable, the response is malformed, or validation fails.
It waits up to 180 seconds for the request. No API key is needed for the
default local server. Generated content is untrusted data, never executed.

The spike uses only `title`, `description`, and simulated text files; it is
not the full scenario schema or an AI-backed GUI. Its tests use simulated
responses and do not need Ollama. On Windows, a team member ran the command
with Ollama 0.40.16 and `llama3.2`; it returned a scenario accepted by the
minimal schema. This single run does not establish output quality, consistency,
or performance. The output included a `.pdf` path with text contents, though
binary-file handling is not implemented. This local experiment does not
complete the NRP.ai endpoint requirement in #79.

## Current limits

The sample schema covers only a title, description, and text files. It is not
the full scenario schema, and the GUI does not implement AI generation,
malware behavior, deleting or creating directories, a process manager, network
viewer, objective evaluation, or reports. Action history is held in memory
only. Host isolation for future malware behaviors still needs its own tests;
the included file-operation check covers only this slice.

The [sample scenario](scenario/sample.py) illustrates the supported structure:
nonempty `title` and `description` strings and a nonempty `files` array. Each
file has a unique, absolute normalized virtual `path` and a string `contents`.
Unexpected fields and invalid paths are rejected before the state is replaced.
