# Specification — AI-assisted scenarios and feedback

> Epic: #23 · Stories: #33, #34, #35, #36, #37, #38, #39, #40, #41
> Owner: jvillacorte · Sprint: 2 · Status: draft

*Task: Create Requirements List for Goal 2 (#47). Requirement from the issue:
"Convert our objectives into list of functional requirements". Each requirement
traces to an objective in proposal §2.*

## Scope

**In scope.** AI-assisted mechanics for configuring, generating, validating,
loading, and evaluating cybersecurity training scenarios (Goal 2, epic #23):

- scenario configuration interface (#33);
- structured scenario schema (#34);
- NRP.ai / LLM integration (#35);
- Pydantic validation, with valid and invalid test expectations (#36);
- scenario loader into simulated desktop elements (#37);
- chronological action logging with per-attempt history (#38);
- AI-assisted after-action report (#39);
- optional contextual hint system (#40);
- scenario variability testing (#41).

AI-generated content is treated as structured data only. It is never executed
as Python code, shell commands, malware, or direct operating-system operations.

**Out of scope.** The internal implementation of the simulated desktop, virtual
file system, simulated processes, system logs, and simulated network activity
(Goal 1, `docs/specs/training-environment.md`); unrestricted AI-generated code
execution; autonomous incident response; automatic modification of the
simulated environment based solely on a hint or AI response.

## Functional requirements

Written in EARS form — "when <trigger>, the system shall <response>".

| ID | Requirement | Objective |
|---|---|---|
| FR-1 | When the user opens the scenario configuration interface, the system shall display options for malware type, difficulty level, and attack path. | #33 |
| FR-2 | When the user selects a difficulty level, the system shall allow selection of easy, medium, or hard. | #33 |
| FR-3 | When the user selects a malware type, the system shall display the available supported malware categories. | #33 |
| FR-4 | When the user selects an attack path, the system shall record the selected attack path. | #33 |
| FR-5 | When the user confirms a scenario configuration, the system shall collect the selected parameters for scenario generation. | #33 |
| FR-6 | When required scenario parameters are missing or unsupported, the system shall prevent scenario generation and display an appropriate message. | #33 |
| FR-7 | When a scenario is represented using the defined schema, it shall include structures for simulated files, processes, system logs, network activity, and incident-response objectives. | #34 |
| FR-8 | When simulated file data is represented in the scenario schema, the schema shall define the required file properties. | #34 |
| FR-9 | When simulated process data is represented in the scenario schema, the schema shall define the required process properties. | #34 |
| FR-10 | When system log data is represented in the scenario schema, the schema shall include timestamps, event types, and event descriptions. | #34 |
| FR-11 | When network activity is represented in the scenario schema, the schema shall include source and destination addresses, ports, and connection status. | #34 |
| FR-12 | When incident-response objectives are represented in the scenario schema, the schema shall describe the expected user actions or conditions for scenario completion. | #34 |
| FR-13 | When the scenario schema is documented, the documentation shall include at least one structurally valid example scenario. | #34 |
| FR-14 | When the user submits a valid scenario configuration, the system shall send the selected parameters to the configured LLM service through the NRP.ai integration. | #35 |
| FR-15 | When the LLM receives scenario parameters, the system shall request structured cybersecurity scenario data according to the predefined generation guidelines. | #35 |
| FR-16 | When the LLM successfully generates a response, the system shall receive structured scenario data for validation. | #35 |
| FR-17 | When the LLM service is unavailable or returns an error, the system shall display an appropriate error message without crashing the application. | #35 |
| FR-18 | When the LLM returns scenario data, the system shall pass the data to the validation component before loading it into the simulation. | #35, #36 |
| FR-19 | When generated scenario data matches the defined schema and constraints, the Pydantic validation component shall accept the data for scenario loading. | #36 |
| FR-20 | When required scenario fields are missing, the Pydantic validation component shall reject the generated data. | #36 |
| FR-21 | When scenario fields contain invalid data types, the Pydantic validation component shall reject the generated data. | #36 |
| FR-22 | When scenario fields contain unsupported values, the Pydantic validation component shall reject the generated data. | #36 |
| FR-23 | When scenario data violates predefined constraints, the validation component shall reject the data and report the validation errors. | #36 |
| FR-24 | When scenario validation fails, the system shall prevent the invalid scenario from being loaded into the simulated environment. | #36, #37 |
| FR-25 | When validation tests are executed, the system shall correctly accept at least three valid test scenarios and reject at least three invalid test scenarios. | #36 |
| FR-26 | When a validated scenario is loaded, the system shall initialize the simulated file system using the scenario's file data. | #37 |
| FR-27 | When a validated scenario is loaded, the system shall populate the simulated process manager using the scenario's process data. | #37 |
| FR-28 | When a validated scenario is loaded, the system shall populate the system log viewer using the scenario's defined events. | #37 |
| FR-29 | When a validated scenario is loaded, the system shall populate the network activity viewer using the scenario's defined connections. | #37 |
| FR-30 | When a validated scenario is loaded, the system shall initialize the incident-response objectives associated with that scenario. | #37 |
| FR-31 | When invalid or unvalidated scenario data is provided, the system shall reject the loading request. | #37 |
| FR-32 | When a scenario is successfully loaded, the system shall allow users to interact with its simulated elements. | #37 |
| FR-33 | When a user performs an investigation action, the system shall record the action in the active scenario history. | #38 |
| FR-34 | When a user performs an incident-response action, the system shall record the action in the active scenario history. | #38 |
| FR-35 | When an action is recorded, the system shall include a timestamp, action type, and relevant simulated target. | #38 |
| FR-36 | When multiple actions are recorded, the system shall maintain their chronological order. | #38 |
| FR-37 | When a scenario is completed, the system shall make the recorded action history available for after-action reporting. | #38, #39 |
| FR-38 | When a new scenario attempt begins, the system shall maintain a separate action history for that attempt. | #38 |
| FR-39 | When a training scenario is completed, the system shall allow the user to generate an after-action report. | #39 |
| FR-40 | When an after-action report is generated, the system shall include a summary of the simulated malware incident. | #39 |
| FR-41 | When an after-action report is generated, the system shall summarize the user's recorded investigation and incident-response actions. | #39 |
| FR-42 | When user actions are evaluated, the system shall compare them against the scenario's defined incident-response objectives. | #39 |
| FR-43 | When a user misses or incorrectly performs a required response action, the after-action report shall identify the issue and provide an explanation. | #39 |
| FR-44 | When an after-action report is generated, the system shall provide recommendations for alternative or improved incident-response procedures. | #39 |
| FR-45 | When the LLM generates feedback, the system shall use the active scenario information and recorded user actions as the basis for its evaluation. | #39 |
| FR-46 | When a training scenario is active, the system shall provide an option for the user to request a hint. | #40 |
| FR-47 | When the user requests a hint, the system shall generate guidance based on the current scenario and available investigation information. | #40 |
| FR-48 | When a hint is generated, the system shall display it within the application interface. | #40 |
| FR-49 | When a hint is requested, the system shall not automatically complete incident-response objectives or modify the simulated environment. | #40 |
| FR-50 | When the user requests a hint, the system shall provide guidance relevant to the active scenario rather than unrelated cybersecurity information. | #40 |
| FR-51 | When no scenario is active, the system shall prevent scenario-specific hint requests. | #40 |
| FR-52 | When identical input parameters are submitted three times, the system shall generate three structurally valid scenarios. | #41 |
| FR-53 | When the three scenarios generated from identical parameters are compared, the system shall identify distinguishable differences in scenario content, such as files, processes, logs, network activity, or incident-response objectives. | #41 |
| FR-54 | When three additional scenarios are generated using different input parameters, the system shall produce valid scenarios reflecting their respective configurations. | #41 |
| FR-55 | When each generated scenario is tested, the system shall verify that it passes the defined Pydantic validation requirements. | #41, #36 |
| FR-56 | When scenario variability testing is completed, the test results shall document the input parameters, validation results, and observed differences for all six scenarios. | #41 |
| FR-57 | When a generated scenario fails validation, the test shall record the failure rather than counting the scenario as a successful result. | #41 |

## Non-functional requirements

| ID | Requirement | Why it matters here |
|---|---|---|
| NFR-1 | AI-generated scenario responses shall be treated as structured data and shall not be executed as Python code, shell commands, malware, or host-system operations. | Prevents untrusted AI output from becoming executable behavior. |
| NFR-2 | Scenario data shall pass Pydantic validation before it is loaded into the simulated environment. | Prevents malformed or unsupported data from corrupting the simulation. |
| NFR-3 | The system shall reject invalid scenario data without partially loading it into the simulated environment. | Keeps the simulation state consistent and predictable. |
| NFR-4 | The system shall not expose API credentials, authentication tokens, or other secrets through the user interface, scenario data, action logs, generated reports, or version control. | Protects external-service credentials and user data. |
| NFR-5 | The system shall fail safe on LLM errors, unavailable services, malformed responses, and validation failures: it shall not crash, shall keep any active scenario unchanged, and shall let the user retry. | Provides a recoverable experience when an external service fails. |
| NFR-6 | Action history shall preserve the chronological order of actions for each scenario attempt. | Accurate ordering is necessary for after-action evaluation. |
| NFR-7 | AI-generated hints and after-action reports shall be based only on the active scenario and recorded user actions provided to the feedback component. | Keeps feedback relevant to the student's actual exercise. |
| NFR-8 | AI-generated hints shall not directly alter scenario state, complete objectives, or perform incident-response actions. | Ensures the student remains responsible for investigating and responding. |
| NFR-9 | The scenario schema, validation rules, and example scenario shall be documented and version-controlled with the project. | Makes generated data reproducible, reviewable, and maintainable. |
| NFR-10 | The system shall produce a clear validation result for every scenario submitted to the validation component. | Makes accepted and rejected scenarios traceable during testing. |

## Acceptance criteria (epic level)

- [ ] A user can configure a scenario by selecting a supported malware type, an
      easy, medium, or hard difficulty level, and an attack path; missing or
      unsupported values prevent generation with a visible message. (#33)
- [ ] A documented scenario schema defines simulated files, processes, logs,
      network activity, and incident-response objectives, with at least one
      valid example. (#34)
- [ ] A valid configuration is sent to the configured LLM service through the
      NRP.ai integration, and an LLM failure shows an error without crashing
      the application. (#35)
- [ ] At least three valid scenarios are accepted and at least three invalid
      scenarios are rejected by the validation tests. (#36)
- [ ] Invalid or unvalidated scenario data cannot be loaded; a validated
      scenario populates the simulated files, processes, logs, network
      activity, and objectives, and the user can interact with them. (#36, #37)
- [ ] Investigation and incident-response actions are listed with timestamps,
      action types, and targets in chronological order, and each scenario
      attempt has its own history. (#38)
- [ ] A completed scenario can produce an after-action report that summarizes
      the incident, evaluates user actions, identifies missed or incorrect
      actions, and gives recommendations. (#39)
- [ ] A user can request an optional hint during an active scenario; hints are
      relevant to the scenario, do not complete objectives or modify the
      environment, and are unavailable when no scenario is active. (#40)
- [ ] Three scenarios from identical parameters are valid and distinguishable,
      three from different parameters are valid and reflect their
      configuration, and the results document parameters, validation results,
      and differences for all six; failed validation is recorded as a failure.
      (#41)
- [ ] AI-generated content is never executed as code, malware, shell commands,
      or direct host-system operations, and no credential appears in the
      repository, UI, logs, or reports. (#35, #36, #37)
- [ ] Every requirement above traces to an objective in proposal §2, and
      `python .github/scripts/check_repo.py` is green.

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Which malware categories and attack paths does the first configuration interface support? | jvillacorte | Before #33 |
| What exact fields are required for files, processes, logs, network connections, and objectives? | jvillacorte | Before #34 |
| Which NRP.ai API format, model, authentication method, and response mode will be used? | jvillacorte | Before #35 |
| Should invalid scenario data be regenerated automatically, or rejected with a retry option? | jvillacorte | Before #36 |
| Which user actions are included in the action log and after-action report? | jvillacorte | Before #38, #39 |
| Should hints come from the LLM, predefined guidance, or both? | jvillacorte | Before #40 |
| Which scenario fields may vary for identical parameters, and what minimum difference counts as distinct? | jvillacorte | Before #41 |
| What information is excluded from prompts, logs, reports, and external AI requests? | jvillacorte | Before AI integration testing |
