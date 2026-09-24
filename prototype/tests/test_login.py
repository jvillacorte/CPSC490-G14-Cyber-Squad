"""Tests for prototype v0 — one test per acceptance criterion of task #5.

Written BEFORE the implementation and committed failing (the "red commit"),
per docs/aidlc/loop-engineering.md §4. Ask of every test: would this fail if
I reintroduced the bug? If not, it asserts nothing.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from login import AuthError, issue_session  # noqa: E402

VALID_EMAIL = "member@csu.fullerton.edu"
VALID_PASSWORD = "correct-horse-battery-staple"  # pragma: allowlist secret (test fixture)


def test_valid_credentials_issue_a_token():
    """Criterion: endpoint returns a session token for valid credentials."""
    token = issue_session(VALID_EMAIL, VALID_PASSWORD)
    assert isinstance(token, str)
    assert len(token) == 64  # sha256 hex digest


def test_wrong_password_is_rejected():
    """Criterion: the failure path rejects bad credentials."""
    with pytest.raises(AuthError):
        issue_session(VALID_EMAIL, "not-the-password")


def test_unknown_email_is_rejected_with_the_same_message():
    """Unknown and wrong-password must be indistinguishable to a caller."""
    with pytest.raises(AuthError) as unknown:
        issue_session("nobody@csu.fullerton.edu", VALID_PASSWORD)
    with pytest.raises(AuthError) as wrong:
        issue_session(VALID_EMAIL, "not-the-password")
    assert str(unknown.value) == str(wrong.value)


def test_missing_input_is_rejected():
    with pytest.raises(AuthError):
        issue_session("", "")
