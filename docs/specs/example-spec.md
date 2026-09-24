# Specification — Account management

> Epic: #1 · Stories: #2, #3
> Owner: 〈name〉 · Sprint: 1 · Status: draft

*This is a worked example of what a specification document should look like:
it names its issues above (gate G2), every requirement traces to a story, and
the acceptance criteria are checkable by someone who did not write them.
Replace it with your own — keep the shape.*

## Scope

**In scope.** Registering an account with a campus email address, signing in
with email and password, issuing a session that expires, and signing out.

**Out of scope** (say this explicitly, or the assistant will helpfully build
it): password reset, third-party sign-in, two-factor authentication,
role-based permissions. These are candidates for CPSC 491, not for the
prototype.

## Functional requirements

Written in EARS form — "when 〈trigger〉, the system shall 〈response〉" — because
each one then becomes a test almost verbatim.

| ID | Requirement | Story |
|---|---|---|
| FR-1 | When a visitor submits a valid campus email and a password of at least 12 characters, the system shall create an account and issue a session. | #2 |
| FR-2 | When a visitor submits an email that already has an account, the system shall reject the request without revealing that the address is registered. | #2 |
| FR-3 | When a member submits credentials that match a stored account, the system shall issue an opaque session token. | #3 |
| FR-4 | When a member submits credentials that do not match, the system shall reject the attempt with a message identical to FR-2's, so an attacker cannot enumerate accounts. | #3 |
| FR-5 | When a session token is older than 24 hours, the system shall treat it as invalid. | #3 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | Passwords are stored only as salted hashes, never in plaintext or reversible form. | The prototype will be read by the sponsor and the instructor. |
| NFR-2 | Failure responses for unknown-account and wrong-password are byte-identical. | Distinguishing them leaks which addresses are registered (see FR-4). |
| NFR-3 | Sign-in responds in under 500 ms on the demo dataset. | The Week-8 check is a live demo. |

## Acceptance criteria (epic level)

- [ ] A member can register, sign in, and sign out through the served
      interface — by tapping, not by calling functions in a console.
- [ ] FR-1 … FR-5 each have a test that fails if the behaviour is removed.
- [ ] No plaintext password appears anywhere in the repository or its history.
- [ ] `python .github/scripts/check_repo.py` is green and the prototype's
      tests pass.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Does the sponsor require campus SSO instead of local accounts? | 〈name〉 | Sprint 2 planning |
| Is a 24-hour session acceptable, or does the sponsor mandate shorter? | 〈name〉 | before FR-5 is implemented |

*Open questions belong in the document, not in someone's memory. An
assistant asked to "finish the spec" will invent answers to these — that is
exactly the fabrication the review gate is looking for.*
