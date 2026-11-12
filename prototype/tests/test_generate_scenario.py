import io
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError, URLError

import pytest

import generate_scenario
from scenario.models import Scenario
from scenario.sample import SAMPLE_SCENARIO


def response_with_content(content):
    return io.BytesIO(json.dumps({"message": {"content": content}}).encode())


def test_generation_requests_schema_and_returns_validated_json(monkeypatch, capsys):
    def fake_urlopen(request, timeout):
        payload = json.loads(request.data)
        assert request.full_url == generate_scenario.OLLAMA_URL
        assert timeout == generate_scenario.TIMEOUT_SECONDS
        assert payload["model"] == "example-model"
        assert payload["format"] == Scenario.model_json_schema()
        assert payload["stream"] is False
        return response_with_content(json.dumps(SAMPLE_SCENARIO))

    monkeypatch.setattr(generate_scenario, "urlopen", fake_urlopen)

    assert generate_scenario.main(["--model", "example-model"]) == 0
    output = capsys.readouterr()
    assert json.loads(output.out) == SAMPLE_SCENARIO
    assert output.err == ""


def test_local_http_request_validates_response(monkeypatch, capsys):
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers["Content-Length"])
            self.server.payload = json.loads(self.rfile.read(length))
            body = json.dumps({"message": {"content": json.dumps(SAMPLE_SCENARIO)}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        monkeypatch.setattr(
            generate_scenario, "OLLAMA_URL", f"http://127.0.0.1:{server.server_port}/api/chat"
        )
        assert generate_scenario.main(["--model", "example-model"]) == 0
        assert server.payload["format"] == Scenario.model_json_schema()
        assert json.loads(capsys.readouterr().out) == SAMPLE_SCENARIO
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.mark.parametrize(
    "response",
    [
        b"not JSON",
        b'{"message": {}}',
        json.dumps({"message": {"content": "not JSON"}}).encode(),
        json.dumps({"message": {"content": '{"title": "Incomplete"}'}}).encode(),
    ],
)
def test_invalid_responses_are_rejected(monkeypatch, capsys, response):
    monkeypatch.setattr(generate_scenario, "urlopen", lambda *args, **kwargs: io.BytesIO(response))

    assert generate_scenario.main(["--model", "example-model"]) == 1
    output = capsys.readouterr()
    assert not output.out
    assert "rejected" in output.err


@pytest.mark.parametrize(
    "error",
    [
        URLError("unavailable"),
        TimeoutError(),
        HTTPError(generate_scenario.OLLAMA_URL, 404, "not found", {}, None),
    ],
)
def test_service_errors_are_reported(monkeypatch, capsys, error):
    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(generate_scenario, "urlopen", fail)

    assert generate_scenario.main(["--model", "missing-model"]) == 1
    output = capsys.readouterr()
    assert not output.out
    assert "failed" in output.err
