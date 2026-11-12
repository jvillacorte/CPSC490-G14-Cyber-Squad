import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pydantic import ValidationError

from scenario.models import Scenario


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
TIMEOUT_SECONDS = 180
PROMPT = (
    "Create a fictional beginner cybersecurity investigation scenario. "
    "Return only a JSON object matching the supplied schema. "
    "Use simulated text files under /home/student/Downloads. "
    "Do not include executable code, commands, or real malware."
)


def generate_scenario(model: str) -> Scenario:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "format": Scenario.model_json_schema(),
        "stream": False,
    }
    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        envelope = json.load(response)
    if not isinstance(envelope, dict) or not isinstance(envelope.get("message"), dict):
        raise ValueError("Ollama response has no message object")
    content = envelope["message"].get("content")
    if not isinstance(content, str) or not content:
        raise ValueError("Ollama response has no scenario content")
    return Scenario.model_validate_json(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate and validate a scenario using a local Ollama model."
    )
    parser.add_argument("--model", required=True, help="Name of an installed Ollama model")
    args = parser.parse_args(argv)
    if not args.model.strip():
        parser.error("--model must not be empty")

    try:
        scenario = generate_scenario(args.model)
    except HTTPError as error:
        print(
            f"Ollama request failed (HTTP {error.code}); check the server and model.",
            file=sys.stderr,
        )
        return 1
    except (URLError, TimeoutError, OSError):
        print("Ollama request failed or timed out; check the local server.", file=sys.stderr)
        return 1
    except (ValueError, UnicodeDecodeError, ValidationError):
        print("Ollama returned malformed or invalid scenario data; rejected.", file=sys.stderr)
        return 1
    print(scenario.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
