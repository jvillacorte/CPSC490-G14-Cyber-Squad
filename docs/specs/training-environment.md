# Specification — Training environment

> Epic: #22 · Stories: #24, #25, #26, #27, #28, #29, #30, #31, #32
> Owner: jvillacorte · Sprint: 2 · Status: draft

## Scope

**In scope.** Goal 1 requirements for a PySide6 simulated desktop that supports
virtual files, simulated processes, simulated system logs, simulated network
activity, simulated malware behaviors, incident-response controls, and scenario
lifecycle controls.

**Architecture decision.** The initial prototype shall use an entirely
in-memory simulation for the virtual file system, simulated processes, system
logs, network activity, malware state, and scenario objectives. The application
must not execute real malware or modify host files, host processes, or host
network configuration.

**Out of scope.** Any behavior that executes real malware or performs direct
host-system file, process, or network configuration changes.

## Functional requirements

| ID | Requirement | Objective trace |
|---|---|---|
| FR-1 | When the application is launched, the system shall display a simulated desktop interface containing a file explorer, process manager, system log viewer, and network activity viewer. | #24 |
| FR-2 | When the user selects the file explorer, process manager, system log viewer, or network activity viewer, the system shall display the selected component and allow switching components without closing or restarting the application. | #24 |
| FR-3 | When the user opens the virtual file system, the system shall display simulated files and directories, allow directory navigation, and allow file inspection (contents and file information). | #25 |
| FR-4 | When the user creates or deletes a simulated file, the system shall update the selected virtual directory and file explorer state accordingly. | #25 |
| FR-5 | When the user performs virtual file operations, the system shall not create, modify, or delete corresponding host operating-system files. | #25 |
| FR-6 | When the user opens the process manager, the system shall display running simulated processes with name, PID, and status, and shall display additional process details when selected. | #26 |
| FR-7 | When the user terminates a simulated process, the system shall update process status and running-process state; if the process is no longer running, the system shall reject the action without affecting other simulated processes. | #26 |
| FR-8 | When process actions are performed in the simulation, the system shall not terminate or modify host operating-system processes. | #26 |
| FR-9 | When the user opens the system log viewer, the system shall display simulated events in chronological order, with timestamp, event type, description, and selectable event details. | #27 |
| FR-10 | When simulated malware or user actions create new events, the system shall append corresponding simulated log entries and update the log viewer. | #27, #29, #31 |
| FR-11 | When the user opens the network activity viewer, the system shall display simulated connections including source and destination addresses, source and destination ports, connection status, and selectable connection details. | #28 |
| FR-12 | When a simulated connection is created or changes status, including malware-generated activity, the system shall update displayed simulated network information. | #28, #29 |
| FR-13 | When users view network activity, the system shall display only simulated connections and shall not access or modify host operating-system network connections. | #28 |
| FR-14 | When a malware scenario starts, the system shall activate the scenario malware behavior and modify only simulated files, processes, and network activity in internal simulation state. | #29 |
| FR-15 | The system shall implement at least two distinct simulated malware behaviors: Trojan and ransomware, each with distinguishable effects represented as simulated state changes only. | #29 |
| FR-16 | Trojan behavior shall be modeled as simulated state changes (for example: creation/modification of simulated files, simulated suspicious process activity, and simulated outbound connection events) and shall generate corresponding simulated logs. | #29 |
| FR-17 | Ransomware behavior shall be modeled as simulated state changes (for example: simulated file encryption/renaming indicators, simulated ransom-note artifacts, simulated process/network events) and shall generate corresponding simulated logs. | #29 |
| FR-18 | When isolation tests are executed, the test suite shall run separate host-isolation test cases for Trojan and ransomware behaviors and verify no host-file, host-process, or host-network-configuration modifications. | #30 |
| FR-19 | When any isolation test detects unauthorized host modification, the test shall fail and report the detected violation; when isolation tests complete, results shall show pass/fail per malware behavior. | #30 |
| FR-20 | When the user performs incident-response actions, the system shall support identifying potential threats, containing selected threats per scenario rules, removing selected simulated malicious files/processes, and recovering supported affected simulated components. | #31 |
| FR-21 | When incident-response actions are valid, the system shall update relevant simulated files, processes, logs, and network activity; when invalid or unsupported, the system shall reject the action without unintended simulation-state changes or host-resource modification. | #31 |
| FR-22 | When the user starts a scenario, the system shall initialize predefined simulated files, processes, logs, and network activity, maintain active scenario state during investigation, and prevent scenario actions when no active scenario exists. | #32 |
| FR-23 | When the user completes, restarts, or resets a scenario, the system shall mark completion status, reload original scenario configuration for restart, clear active state for reset, and avoid host file/process/network modifications. | #32 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | All Goal 1 simulation state (files, processes, logs, network activity, malware state, objectives) shall remain in memory within the application process. | Enforces the agreed safety boundary for the initial prototype. |
| NFR-2 | Malware behaviors shall be represented as controlled simulation-state transitions and shall not execute host binaries, scripts, or external malware payloads. | Prevents unsafe execution while still enabling incident-response practice. |
| NFR-3 | Functional requirements in this document shall be traceable to Goal 1 objective issues #24–#32. | Preserves objective intent and supports review against proposal §2. |

## Acceptance criteria (epic level)

- [ ] FR-1 through FR-23 trace to one or more of #24, #25, #26, #27, #28, #29, #30, #31, and #32.
- [ ] The specification states the in-memory-only architecture decision and the host-safety prohibition (no real malware execution, no host file/process/network modification).
- [ ] Trojan and ransomware simulated behaviors are both specified as simulated state changes only.
- [ ] Host-isolation test requirements are specified separately for Trojan and ransomware behaviors.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Which exact simulated fields should be mandatory for process-detail and connection-detail views in Sprint 2 UI prototypes? | jvillacorte | Before implementation of #24, #26, #28 |
