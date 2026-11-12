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

## Network activity viewer (Objective 1.5, #28)

This section details the requirements for the network activity viewer. It
defines what a simulated connection contains, which protocols and states the
simulation supports, and what the viewer shows when a connection is selected.
All connections are records in the in-memory simulation state; none
correspond to real connections on the host computer (FR-13, NFR-3).

### Connection fields

Each simulated connection is a NETWORK_CONNECTION record (Figure 4,
docs/design/data-model.md). The connection list shows five columns, chosen
because they are the fields an analyst reads first when looking for
suspicious traffic: where a connection comes from, where it goes, and whether
it is still active (AC2).

| Column | Field | Example |
|---|---|---|
| Source IP | source_ip | 10.0.0.15 |
| Source port | source_port | 49712 |
| Destination IP | dest_ip | 203.0.113.42 |
| Destination port | dest_port | 4444 |
| Status | connection_state | ESTABLISHED |

When the user selects a connection, the viewer shows its detail fields (AC3):

| Detail | Field | Why it matters |
|---|---|---|
| Protocol | protocol | Distinguishes TCP sessions from UDP or ICMP traffic |
| Connection ID | conn_id | Identifies the connection in the action log and after-action report |
| Direction | derived from source and destination | Outbound connections to unknown hosts are a common sign of command-and-control |
| Owning process | process_id → PROCESS_RECORD | Links the connection to the process manager (#26) so the user can trace it to its cause |

### Protocols and states

The simulation supports three protocols: TCP, UDP and ICMP. These cover the
traffic a beginner is expected to recognize, including the outbound TCP
connections typical of a Trojan's command-and-control channel.

A connection is in one of four states. LISTENING, ESTABLISHED and TIME_WAIT
mirror what a real operating system reports. CLOSED is added so that an
incident-response containment action (#31) has a visible result.

| State | Meaning in the simulation |
|---|---|
| LISTENING | A simulated process is waiting for inbound connections on a port |
| ESTABLISHED | Two endpoints are actively exchanging simulated traffic |
| TIME_WAIT | The connection has ended and is waiting to be cleaned up |
| CLOSED | The connection was terminated, for example by a containment action |

### Detailed requirements

FR-11, FR-12 and FR-13 state what the viewer must do at the level of the
whole training environment. The requirements below break each one into
behaviors that can be implemented and tested separately in CPSC 491. Each is
written in the form "when <trigger>, the system shall <response>" and traces
to its parent requirement and to an acceptance criterion of #28.

**Displaying connections (FR-11).** The viewer's first job is to show the
student every connection the scenario contains, in a form that can be scanned
quickly. The list therefore shows the five columns defined above for every
connection, including closed ones, so that the student can see how the
network state changed during the incident rather than only what is active
now. Selecting a connection opens its details without leaving the list, which
keeps the student's place while investigating.

| ID | Requirement | Traces to |
|---|---|---|
| FR-11.1 | When the user opens the network activity viewer during an active scenario, the system shall display one row for every simulated connection in the scenario, in every state. | FR-11, AC1 |
| FR-11.2 | When a connection row is displayed, the system shall show its source IP, source port, destination IP, destination port and connection status. | FR-11, AC2 |
| FR-11.3 | When the user selects a connection, the system shall display its protocol, connection ID, direction, and owning process (or "none" if no process owns it), while keeping the list visible. | FR-11, AC3 |
| FR-11.4 | When the user selects a connection that has an owning process, the system shall allow the user to open that process in the process manager. | FR-11, AC3, #26 |
| FR-11.5 | When no scenario is active, the system shall show an empty viewer with a message that no scenario is loaded. | FR-11, FR-22 |

**Updating connections (FR-12).** Network activity changes while the student
investigates: scenarios start with connections already open, simulated
malware opens new ones, and the student's own containment actions close
them. The viewer must reflect every change as it happens, so the student
never acts on stale information. Connections are never removed from the
list; a closed connection stays visible with the CLOSED status, so the
student can see what was contained.

| ID | Requirement | Traces to |
|---|---|---|
| FR-12.1 | When a simulated connection is created, the system shall add it to the displayed list without the user reopening the viewer. | FR-12, AC4 |
| FR-12.2 | When a simulated connection changes state, the system shall update its status in the list and, if it is selected, in the details panel. | FR-12, AC4 |
| FR-12.3 | When a connection changes, the system shall make the changed row distinguishable from unchanged rows until the user selects it. | FR-12, AC4 |
| FR-12.4 | When the user closes a connection through an incident-response containment action, the system shall set its state to CLOSED and record the action in the action log. | FR-12, FR-21, #31, #38 |
| FR-12.5 | When an action targets a connection that is already CLOSED or does not exist, the system shall reject the action and leave every connection unchanged. | FR-12, FR-21 |

**Malware-generated connections (FR-12).** The connections that matter most
for training are the ones simulated malware creates. The malware behavior
engine (#29) does not draw anything itself; it sends a network event to the
simulation state, and the viewer displays the result like any other
connection. Keeping this as one path means the viewer behaves the same for
scripted scenarios and AI-generated ones.

| ID | Requirement | Traces to |
|---|---|---|
| FR-12.6 | When a simulated malware behavior generates network activity, the malware behavior engine shall send a network event (create a connection or change its state) to the simulation state, and the system shall display the resulting connection. | FR-12, FR-14, AC5, #29 |
| FR-12.7 | When a malware behavior creates a connection, the system shall record the owning simulated process so that the connection can be traced to it. | FR-12, AC3, AC5 |

**Host isolation (FR-13).** The viewer imitates a real network tool, which
makes it the place where reaching for the real network would be easiest by
mistake. These requirements state exactly what it must never do, so the
isolation tests for #30 have something concrete to check.

| ID | Requirement | Traces to |
|---|---|---|
| FR-13.1 | When the viewer displays or updates connections, the system shall read them only from the in-memory simulation state. | FR-13, NFR-1, AC6 |
| FR-13.2 | The network viewer and the simulation's network state shall not read host network connections, interfaces, routing tables or socket information. | FR-13, NFR-3, AC6 |
| FR-13.3 | When the user closes a simulated connection, the system shall not open, close or change any host network connection or configuration. | FR-13, NFR-3, AC6 |
| FR-13.4 | The isolation test suite shall include a test that fails if the network viewer or simulation network state uses a host networking library or system call. | FR-13, #30, AC6 |

### Acceptance criteria

The network activity viewer is complete when every criterion below is met.
Each one is copied from story #28 without rewording, followed by a concrete
check that someone who did not write the requirement can perform, and the
verification method planned for implementation in CPSC 491. Automated tests
run in CI without a display; manual checks are performed from a clean clone
by following the prototype README.

| # | Acceptance criterion (from #28) | How to check it | Planned verification |
|---|---|---|---|
| AC1 | When the user opens the network activity viewer, the system shall display a list of simulated network connections. | Load a fixture scenario with five connections in different states, open the viewer, and confirm five rows appear, including any CLOSED connection (FR-11.1). | Automated test: `test_ac1_lists_all_scenario_connections` |
| AC2 | When a connection is displayed, the system shall include its source IP address, destination IP address, source and destination ports, and connection status. | For one fixture connection, compare each of the five columns against the fixture's values (FR-11.2). | Automated test: `test_ac2_row_shows_required_columns` |
| AC3 | When the user selects a simulated connection, the system shall display additional information associated with that connection. | Select a connection with an owning process and confirm the details show its protocol, connection ID, direction and owning process; select one without an owning process and confirm it shows "none" (FR-11.3). | Automated test: `test_ac3_selection_shows_detail_fields`; manual check of the details panel layout |
| AC4 | When a simulated network connection is created or changes status, the system shall update the displayed connection information. | With the viewer open, add a connection to the simulation state and confirm a new row appears; change a connection to CLOSED and confirm its row and, if selected, its details update without reopening the viewer (FR-12.1, FR-12.2). | Automated test: `test_ac4_updates_on_create_and_state_change` |
| AC5 | When a simulated malware behavior generates network activity, the system shall display the associated simulated connection. | Trigger the Trojan behavior from the malware behavior engine (#29) and confirm its outbound connection appears with the Trojan's process as the owning process (FR-12.6, FR-12.7). | Automated test: `test_ac5_malware_connection_displayed` (requires #29) |
| AC6 | When the user views network activity, the system shall display only simulated connections rather than accessing or modifying the host operating system's network connections. | Confirm every displayed connection exists in the scenario fixture and nothing else appears; confirm the network viewer and network state use no host networking library or system call; close a simulated connection and confirm no host connection changed (FR-13.1–FR-13.4). | Automated tests: `test_ac6_displays_only_simulated_connections` and `test_ac6_no_host_network_access`; included in the #30 isolation suite |

AC1 to AC4 and AC6 can be verified using the network viewer and a scenario
fixture alone. AC5 depends on the malware behavior engine (#29) sending the
network event defined in FR-12.6; until that engine exists, the criterion can
only be checked with a scripted event, which does not count as meeting it.

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | All Goal 1 simulation state, including files, processes, logs, network activity, malware state, and objectives, shall remain in memory within the application process. | Enforces the agreed safety boundary for the initial prototype. |
| NFR-2 | Malware behaviors shall be represented as controlled simulation-state transitions and shall not execute host binaries, scripts, or external malware payloads. | Prevents unsafe execution while still enabling incident-response practice. |
| NFR-3 | The system shall not access or modify host-system files, processes, or network configurations while users, simulated malware, or incident-response controls interact with the training environment. | Ensures that the training environment cannot affect the user's computer. |
| NFR-4 | Resetting or restarting a scenario shall restore the in-memory simulation to its defined initial state without requiring access to host-system resources. | Allows students to repeat scenarios safely and consistently. |

## Acceptance criteria (epic level)

- [ ] A user can launch the application and access the simulated file explorer,
      process manager, system log viewer, and network activity viewer without
      closing or restarting the application.

- [ ] A user can inspect, create, navigate, and delete simulated files, and
      each operation updates the in-memory virtual file system and its
      corresponding interface.

- [ ] A user can inspect and terminate simulated processes, and invalid
      termination attempts are rejected without affecting other simulated
      processes.

- [ ] A user can view timestamped simulated system events, including events
      generated by simulated malware and incident-response actions.

- [ ] A user can view simulated network connections containing source address,
      destination address, port information, and connection status.

- [ ] The system supports both a simulated Trojan and simulated ransomware,
      with distinguishable effects on the in-memory simulation state.

- [ ] Simulated malware changes appear in the appropriate desktop components and
      generate investigation-relevant simulated log entries.

- [ ] A user can identify, contain, remove, and recover from supported simulated
      malware threats.

- [ ] A user can start, complete, restart, and reset training scenarios.

- [ ] Invalid actions are rejected without unintentionally modifying the
      simulation state.

- [ ] Separate tests verify that the Trojan does not modify host-system files,
      processes, or network configurations.

- [ ] Separate tests verify that the ransomware does not modify host-system
      files, processes, or network configurations.

- [ ] Every functional requirement in this specification has a corresponding
      test or documented verification method before the Goal 1 implementation
      is considered complete.

- [ ] The architecture documentation identifies the simulation trust boundary
      and explains how simulated malware is restricted to in-memory application
      state.

- [ ] `python .github/scripts/check_repo.py` is green and the prototype tests
      pass.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| What specific effects should the simulated Trojan produce? | jvillacorte | Before implementation of #29 |
| What specific simulated files should ransomware affect? | jvillacorte | Before implementation of #29 |
| Which simulated files should be restorable during ransomware recovery? | jvillacorte | Before implementation of #31 |
| Which process fields must be displayed beyond name, PID, and status? | jvillacorte | Before implementation of #26 |
| Which network fields and simulated protocols must be supported? **Decided:** see "Network activity viewer" above — five list columns, four detail fields, TCP/UDP/ICMP, and four states. | jvillacorte | Before implementation of #28 |
| What exact actions count as identification, containment, removal, and recovery? | jvillacorte | Before implementation of #31 |
| What makes a scenario complete: all objectives completed, a manual completion action, or both? **Decided:** both — the scenario completes when all objectives are met or the user chooses to finish ([architecture.md §6](../design/architecture.md)). | jvillacorte | Before implementation of #32 |
| Should the Trojan activate immediately when a scenario starts, or after a simulated user action? | jvillacorte | Before implementation of #29 |
| What evidence will be collected to prove that host files, processes, and network configurations were not modified? | jvillacorte | Before implementation of #30 |
| What response should the application provide if the simulation enters an invalid state? | jvillacorte | Before integration testing |
