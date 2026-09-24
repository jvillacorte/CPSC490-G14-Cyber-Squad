"""Prototype v0 — the thinnest end-to-end slice that proves the risky part.

This example implements the login check behind story #3 and task #5: valid
credentials get a session token, everything else is rejected. It is
deliberately tiny — a prototype exists to answer one question, not to be the
product.

**Replace this file with your own prototype.** Keep the shape: a small
module, a test per acceptance criterion, and run instructions in README.md
that work on a machine that has never seen your project.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets

# Demo credential store. A real system stores a salted hash per user in a
# database and never keeps plaintext — see docs/design/example-design.md.
_DEMO_USERS = {"member@csu.fullerton.edu": "correct-horse-battery-staple"}

_SESSION_SECRET = secrets.token_bytes(32)


class AuthError(Exception):
    """Raised when credentials are not accepted."""


def issue_session(email: str, password: str) -> str:
    """Return an opaque session token for valid credentials.

    Raises AuthError for an unknown email or a wrong password.
    """
    if not email or not password:
        raise AuthError("email and password are required")
    expected = _DEMO_USERS.get(email.strip().lower())
    if expected is None or not hmac.compare_digest(expected, password):
        # Same error either way: distinguishing them tells an attacker which
        # addresses are registered.
        raise AuthError("invalid email or password")
    return hmac.new(_SESSION_SECRET, email.encode(), hashlib.sha256).hexdigest()


if __name__ == "__main__":  # pragma: no cover - manual smoke run
    token = issue_session("member@csu.fullerton.edu", "correct-horse-battery-staple")
    print(f"session issued: {token[:16]}...")
