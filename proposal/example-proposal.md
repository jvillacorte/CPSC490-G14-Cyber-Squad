# Project Proposal — Secure Member Portal (EXAMPLE)

**Department of Computer Science**
**CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project**

**Group 00 — Example Team** · Sponsor: independent
Authors: Doe, Jane (jdoe-example), Roe, Richard (rroe-example)
Repository: https://github.com/kyoungshin/CPSC490
Date: October 11, 2026

> **Worked example** of `proposal/proposal.md` written for the Word export.
> Its issue references point at this repository's example issues #1–#7.
> Convert it with:
>
>     pandoc proposal/example-proposal.md -o proposal/example-proposal.docx --reference-doc=proposal/reference.docx --lua-filter=proposal/to-word.lua --resource-path=proposal
>
> Quote blocks like this one are guidance and never reach the Word file.

---

## 0. Abstract

Small clubs keep their member records in shared spreadsheets that anyone with
the link can edit. This project builds a member portal with secure accounts,
proves the riskiest part — session handling — in a prototype by the end of
Sprint 2, and documents the design that CPSC 491 will build on.

## 1. Introduction

Volunteer-run clubs rarely have anyone whose job is security, yet they hold
names, emails and payment notes for hundreds of members. A portal with real
accounts removes the shared-link problem without asking volunteers to run a
server.

### 1.1 Related Work

Hosted membership tools exist but charge per member and lock the data in
their own format; open-source portals assume an administrator who patches
the server [1].

### 1.2 Problem Statements

Shared spreadsheets give every member write access to every record, and
nothing records who changed what.

## 2. Goals and Objectives

Each goal is tracked as an epic and each objective as a user story; every one
is cited by its issue reference.

**Goal 1: Secure account management** [[epic:#1]](https://github.com/kyoungshin/CPSC490/issues/1 "Goal 1: Secure account management")

Objective 1.1: Implement member registration and login with hashed
credentials and session expiry. [[story:#2]](https://github.com/kyoungshin/CPSC490/issues/2 "Objective 1.1: Implement member registration and login")

Objective 1.2: Demonstrate the login round-trip in a runnable prototype at the
end-of-Sprint-2 demo. [[story:#3]](https://github.com/kyoungshin/CPSC490/issues/3 "Objective 1.2: Demonstrate the login round-trip")

Objective 1.3: Document the authentication architecture and data model for
CPSC 491. [[story:#4]](https://github.com/kyoungshin/CPSC490/issues/4 "Objective 1.3: Document the authentication architecture")

## 3. Proposed Approaches

We will build the login round-trip first, because session handling is the
design choice most likely to force a rewrite if it is wrong, and every other
feature depends on it. A hosted identity provider was considered and rejected:
it would hide exactly the part the project has to prove. The implementation
stack is detailed in §4.

## 4. Required Environment, Resources, and Planned Activities

### Environment and resources

The prototype runs on Node.js 22 with PostgreSQL 16 in Docker, so every team
member runs the same stack locally. Standing up that stack, with a health
check the demo can call, is the first piece of work. [[task:#5]](https://github.com/kyoungshin/CPSC490/issues/5 "Task 1.2.1: Stand up the prototype login endpoint")

### Specification and design documents

The account-management specification, `docs/specs/account-management.md`,
defines what the login endpoint accepts and rejects, including the input
rules that stop malformed requests before they reach the database. [[feature:#6]](https://github.com/kyoungshin/CPSC490/issues/6 "Feature 1.2.a: Login endpoint with session issuance")

The authentication design, `docs/design/architecture.md`, chooses a salted
digest for stored passwords so that no plain-text credential is ever stored
or logged. [[sub-task:#7]](https://github.com/kyoungshin/CPSC490/issues/7 "Sub-task 1.2.1.a: Hash and verify passwords")

### Diagrams

Figure 1 shows the login round-trip the prototype demonstrates: the browser
sends credentials, the login API checks them against the salted hash in
PostgreSQL, and a session cookie comes back.

![Figure 1. Login round-trip architecture. [[feature:#6]](https://github.com/kyoungshin/CPSC490/issues/6)](example-architecture.png){width=6in}

### Planned activities

The login endpoint is planned for Sprint 2: it issues a session on a
successful login, and its hashing step lands first so the demo never handles
a plain-text password. [[feature:#6]](https://github.com/kyoungshin/CPSC490/issues/6) [[sub-task:#7]](https://github.com/kyoungshin/CPSC490/issues/7)

## 5. Project Outcomes

When the project is finished, a club officer can invite members, each member
signs in with their own account, and every change to a record is attributed.
The deliverables are the team repository, the prototype in `prototype/`, and
the final report; the prototype demonstrates the login round-trip.

## 6. Project Timeline

The spring plan builds the objectives in §2 in order: accounts first, then
records, then the audit trail.

## 7. AI Usage

No AI tool drafted the prose of this proposal.

## 8. References

[1] OWASP Foundation. Password Storage Cheat Sheet.
https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html,
accessed Oct 8, 2026.
