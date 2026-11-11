# Project Proposal — Cyber Sandbox

**Department of Computer Science**
**CPSC 490 Undergraduate Seminar in Computer Science — Proposal for Capstone Project**

**Group 14 — Cyber Squad** · Sponsor: independent
Authors: Goodson, Alex (alexgoodson-1991), Boynton, Daniel (danjobo), Nellesen, Jake (Jake-P-N), Nguyen, Vanna (NguyenVGH), Villacorte, Joseph (jvillacorte)
Date: 2026-10-15

## 0. Abstract

Cybersecurity education often emphasizes conceptual knowledge, while opportunities for repeated hands-on practice tend to be more limited in scope and practice. Thus, beginner students can benefit from supplemental environments, where they can safely apply what they have learned by practicing responding to threats without risking damage to a real system. 
This project proposes a Rogue-Lite Cybersecurity Training sandbox, an AI-assisted learning environment designed for beginner cybersecurity students. The application would be able to simulate a desktop environment, where users interact and investigate files, processes, logs, and network activity associated with malware incidents. The reach of the threats would remain enclosed within the simulated application, allowing users to practice identifying, containing, removing, and recovering from malicious activities in a controlled setting.
A primary feature of this system is the use of artificial intelligence to create variation between training scenarios. An LLM would be given input parameters, such as difficulty level, malware type, and a path of attack, then generate structured scenario data based on predefined guidelines. Pydantic would be used to validate this data before it is incorporated into the simulation. AI may also provide educational explanations and an after-action report describing the entire attack, and giving feedback on the user’s response.
The end goal of this project is to establish a framework for an accessible and continually repeatable cybersecurity training tool that can supplement traditional coursework with something more closely related to an actual cybersecurity event. Python and PySide6 are tentative options to create the simulated desktop interface, while a local/hosted LLM could be utilized through [NRP.ai](https://nrp.ai), which could support the dynamic scenario generation and feedback.


## 1. Introduction

Beginner cybersecurity students would be able to learn foundational concepts through provided lectures, readings and structured lab exercises, but developing practical incident-response skills also requires the opportunity to apply that knowledge. Providing a repeatable source of malware-related exercises can present various challenges involving safety and scenario variety. Predetermined exercises also have the possibility of providing less value upon repetition, once students become familiar with their general structure/expected events and solutions.
Unlike a traditional static exercise, in which the same sequences of events are presented each time, the proposed sandbox is designed around changing scenarios in which the student's understanding of their own knowledge becomes the main form of progression. While scenarios may change between attempts, the knowledge and structure of investigation developed by the student can carry into future experiences. 


### 1.1 Related Work

Various platforms exist that provide hands-on cybersecurity training through interactive exercises, and isolated environments. For example, TryHackMe [1], and Hack The Box [2] both provide guided lessons and virtual environments where users can practice cybersecurity techniques, while something such as CyberDefenders [3] focuses more on defensive investigations involving logs, network traffic and malware related information. Similarly, LetsDefend [4] provides a simulated Security Operations Center experience where users can investigate and respond to security incidents. Another platform, such as CyLab Security Academy [5] also demonstrates a more game-oriented design, which uses challenges and progression to promote a learning environment to its students. While all of these demonstrate the value of practical cybersecurity experience/education, the proposed project would explore a path that combines a simulated desktop environment with specifically AI-generated scenario variation and feedback, which could allow beginner students to repeatedly investigate numerous types of malware incidents, which in theory would allow for a large amount of variability.

| Existing approach | What it does | Pros | Cons | Why ours differs |
|---|---|---|---|---|
| TryHackMe [1] | Provides guided cybersecurity lessons and interactive virtual labs on it's website | Very beginner-friendly, with structured learning paths and practical exercises | Organized around preparing rooms and learning modules, which lacks a small amount of variability | Uses AI to generate varied malware scenarios with the users input, giving more freedom of choice |
| Hack The Box [2] | Provides cybersecurity training through VMs, guided modules and technical challenges | Realistic environments and expansive offensive and defensive training | Excercises tend to require more technical knowledge, and require working with an actual VM, which may still be difficult for a beginner | Focuses on beginner-level incident response, without requiring the prerequisite of setting up a VM |
| CyberDefenders [3] | Provides defensive cybersecurity analysis including malware, traffic logs, and forensic evidence | Emphasis on practical threat investigation and IRL security artifacts | Uses curated investigation labs, which can lack variability | Allows users to interact with a unique simulated system, practicing responding to specifically tailored malware incidents |
| LetsDefend [4] | Simulates a Security Operations Center (SOC) where users can investigate allerts and respond to security threats | Provides a realistic workflow and incidenct-response experience | Requires much more technical knowledge, a little overwhelming for beginner cybersecurity students to get into | Focuses on desktop-level malware, providing AI-generated security validation and feedback |
| CyLab Security Academy [5] | Provides game-oriented cybersecurity challenges, learning paths, and CTF objectives | Accessible to beginners through its challenges and method of progression. | Primarily relies on predefined challenges with established objectives, potentially limiting variation during repeated attempts. | Uses AI-generated malware scenarios to introduce changing threats and investigation requirements, encouraging students to apply previously learned knowledge to unfamiliar incidents. |


### 1.2 Problem Statements

P1-  Limited Acceess to Safe, Practical Cybersecurity Training: Beginning cybersecurity students need the opportunity to apply their foundational knowledge to practical security events, but providing hands-on malware exercuses can present challenges with safety and environment configuration depending on the level of experience the student has. Working with real malware requires carefully isolated environments and additional security precautions in order to prevent unintended effects on the host system.

P2- Limited Scenario Variation and ability for Repeated Learning Opportunities: Predetermined cybersecurity training scenarios may become less effective upon repetition, as students can become familiar witht he overall structure, expected events, and where to find the answers without actually training any practical experience. This can limit opportunities for students to practice adapting their skills to unfamiliar threats and situations when the time requires.

| Problem | Addressed by |
|---|---|
| P1 Limited access to safe and practical cybersecurity training | Goal 1: Develop an interactive and secure cybersecurity training environment (#22) |
| P2 Limited scenario variation and opportunities for repeated learning experiences | Goal 2: Integrate AI-assisted mechanics through scenario generation and custom-generated feedback (#23) |

## 2. Goals and Objectives

- **Goal 1: Develop an interactive and secure cybersecurity training environment** (Epic [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22))
  - Objective 1.1: Create a simulated desktop interface that contains a file explorer, process manager, system log viewer, and network activity viewer. ([[story:#24]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/24))
  - Objective 1.2: Implement a virtual file system that allows users to inspect, create, and delete simulated files. ([[story:#25]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/25))
  - Objective 1.3: Create a process manager for the desktop environment that allows users to inspect and terminate running simulated programs and processes. ([[story:#26]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/26))
  - Objective 1.4: Develop a system log viewer that displays timestamped events associated with the simulated system, including malware activity. ([[story:#27]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/27))
  - Objective 1.5: Develop a network activity viewer that displays simulated connections, including source and destination addresses, ports, and connection status. ([[story:#28]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/28))
  - Objective 1.6: Implement at least two simulated malware behaviors that modify simulated files, processes, and network activity while restricting their effects to the internal application. ([[story:#29]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/29))
  - Objective 1.7: Verify through separate test cases that each simulated malware behavior does not modify host-system files, processes, or network configurations. ([[story:#30]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/30))
  - Objective 1.8: Implement incident-response controls that allow users to identify, contain, remove, and recover from simulated malware threats. ([[story:#31]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/31))
  - Objective 1.9: Implement scenario controls that allow users to start, complete, restart, and reset training scenarios. ([[story:#32]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/32))

- **Goal 2: Integrate AI-assisted mechanics through scenario generation and custom-generated feedback** (Epic [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23))
  - Objective 2.1: Develop a scenario configuration interface that allows users to select malware type, difficulty level (easy, medium, or hard), and attack path. ([[story:#33]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/33))
  - Objective 2.2: Define a structured scenario schema containing simulated files, processes, logs, network activity, and incident-response objectives. ([[story:#34]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/34))
  - Objective 2.3: Integrate an LLM through [NRP.ai](https://nrp.ai) to generate structured cybersecurity scenarios based on user-selected parameters. ([[story:#35]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/35))
  - Objective 2.4: Implement Pydantic validation that accepts scenarios meeting predefined requirements and rejects scenarios containing invalid or unsupported data. ([[story:#36]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/36))
  - Objective 2.5: Implement a scenario loader that converts validated AI-generated data into interactive elements within the simulated desktop environment. ([[story:#37]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/37))
  - Objective 2.6: Develop an action-logging system that records user investigation and incident-response actions in chronological order. ([[story:#38]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/38))
  - Objective 2.7: Generate an AI-assisted after-action report that summarizes the simulated attack information, evaluates user actions, and recommends alternative incident-response procedures. ([[story:#39]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/39))
  - Objective 2.8: Implement an optional AI-assisted hint system that provides contextual information during an active training scenario. ([[story:#40]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/40))
  - Objective 2.9: Generate at least three distinct and structurally valid scenarios using identical input parameters to demonstrate scenario variability, and test three additional scenarios using different input parameters. ([[story:#41]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/41))



## 3. Proposed Approaches

Our project proposes an **in-memory cybersecurity simulation** to train beginner incident-response skills.

Instead of manipulating host operating-system resources, the application is intended to model files, processes, system logs, and network activity inside application state. This design aims to make training repeatable and prevent accidental harm to the user's machine while allowing realistic investigation and response workflows; the isolation behavior still requires implementation and testing.

For scenario generation, we will combine **user-selected parameters** (malware type, difficulty, attack path) with an LLM integration to produce structured scenario data. Because LLM output can be inconsistent, generated scenarios are treated strictly as data and must pass schema validation before they can be loaded into the training environment. This design reduces unsafe or malformed outputs while preserving scenario variability.

We selected this approach over static handcrafted scenarios because it supports repeated practice with varied incidents and stronger learning transfer. We also selected this approach over host-level sandbox execution because Sprint 2 priorities are specification, design clarity, and a reliable prototype skeleton, not high-risk runtime behavior. Detailed implementation choices, environment/tooling, and diagram artifacts are documented in §4.

## 4. Required Environment, Resources, and Planned Activities

### Environment and resources

The planned implementation uses Python 3.x, PySide6 for the desktop interface, and Pydantic for scenario validation. Python supports rapid development of the in-memory simulation and its AI integration; PySide6 provides a desktop-style interface, while Pydantic can reject malformed scenario data before it is loaded. Development and demonstrations are intended to run locally on Python-supported Windows, macOS, and Linux machines, avoiding production deployment complexity while enabling repeatable clean-clone runs. These are design choices, not claims that the prototype already runs on all three platforms. [[task:#59]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/59) [[task:#93]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/93)

The prototype is intended to keep simulation state in memory, with optional file-based fixtures for test scenarios. This supports reset and restart without deliberately modifying host files, processes, or network settings; isolation still needs to be verified by tests. The project is independent, requires no sponsor dataset, and plans to use local machines rather than production hosting for the prototype. These choices reduce external dependencies while the team validates the simulation design. [[task:#60]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/60)

For AI-assisted generation and feedback, the team plans to use an NRP.ai-compatible LLM endpoint with an account and API key supplied through environment variables. A local `.env` file and a checked-in `.env.example` without real secrets are planned to make configuration reproducible without committing credentials; the example file and integration are not yet present. The integration spike will evaluate generation and validation before scenario data enters the simulation. [[task:#79]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/79)

GitHub Issues and Projects, pull requests, GitHub Actions, `check_repo.py`, and the sprint-report workflow support traceability and review of the work described in §3. The planned test tool is `pytest`, with tests in `prototype/tests` for schema validation and host isolation. Those tests are still to be implemented; the current prototype CI can pass without collecting any tests. [[task:#83]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/83) [[task:#60]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/60)

### Diagrams

Figure references in this section correspond to design artifacts in `docs/design/`.

- **Figure 1. High-level architecture diagram** — [docs/design/architecture.md](../docs/design/architecture.md)

  Figure 1 shows the three planned layers of the application: a PySide6 presentation layer, an in-memory simulation core, and an AI integration layer. It also marks two intended safety boundaries: simulated operations stay within in-memory state rather than modifying host resources, and NRP.ai output must pass Pydantic validation before the scenario loader can place it in the simulation [[task:#53]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53).

  ![Figure 1: High-level architecture diagram](../docs/design/images/architecture-diagram.png)
  *Figure 1: High-level architecture showing the presentation layer, the AI integration layer with its untrusted-data boundary, and the in-memory simulation core with its host-isolation boundary.*

- **Figure 2. System context diagram** — [docs/design/system-context.md](../docs/design/system-context.md)

  Defines system boundaries and external actors/services, including users and LLM/API dependencies.

- **Figure 3. Data flow diagram** — [docs/design/data-flow.md](../docs/design/data-flow.md)

  Figure 3 illustrates the end-to-end data lifecycle, detailing external inputs, internal transformations across NRP.ai and Pydantic validation boundaries, and in-memory action logging and reporting.

  ![Figure 3: System Data Flow Diagram](../docs/design/images/data-flow-diagram.png)
  *Figure 3: System Data Flow Diagram modeling parameter input through generation, validation, desktop loading, chronological action logging, and after-action reporting.*

- **Figure 4. ER diagram for scenario schema and action logs** — [docs/design/data-model.md](../docs/design/data-model.md)

  Models structured scenario entities and action-history relationships.

- **Figure 5. Sequence diagram for critical scenario flow** — [docs/design/scenario-sequence.md](../docs/design/scenario-sequence.md)

  Covers configure -> generate -> validate -> load -> investigate/respond -> report flow.

- **Figure 6. User flow / screen-flow diagram** — [docs/design/user-flow.md](../docs/design/user-flow.md)

  Figure 6 shows the trainee's path from scenario setup through investigation and incident-response actions to scenario completion and the after-action report.

  ![Figure 6: User Flow / Screen-Flow Diagram](../docs/design/images/user-flow-diagram.png)
  *Figure 6: User flow diagram covering scenario start, investigation actions, response actions, and completion/report flow.*

### Specification and design documents

| Document | Kind | Covers | Issues |
|---|---|---|---|
| [docs/specs/training-environment.md](../docs/specs/training-environment.md) | specification | Goal 1 requirements for the interactive, secure training environment | [[task:#46]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/46) |
| [docs/specs/ai-scenarios.md](../docs/specs/ai-scenarios.md) | specification | Goal 2 requirements for AI-assisted scenario generation and feedback | [[task:#47]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/47) |
| [docs/design/architecture.md](../docs/design/architecture.md) | design | High-level architecture and component boundaries | [[task:#53]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53), [[task:#70]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/70) |
| [docs/design/system-context.md](../docs/design/system-context.md) | design | System boundary and external actors/services | [[task:#54]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/54) |
| [docs/design/data-flow.md](../docs/design/data-flow.md) | design | Data flow from user input through AI generation, validation, loading, and reporting | [[task:#55]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/55) |
| [docs/design/data-model.md](../docs/design/data-model.md) | design | ER/data model for scenario schema and action logs | [[task:#56]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/56) |
| [docs/design/scenario-sequence.md](../docs/design/scenario-sequence.md) | design | Sequence flow across configure/generate/validate/load/play/report | [[task:#57]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/57) |
| [docs/design/user-flow.md](../docs/design/user-flow.md) | design | User flow/game-loop and screen transitions | [[task:#58]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/58) |

#### Document summaries

`docs/specs/training-environment.md` defines the Goal 1 requirements for the simulated desktop training environment, including functional behavior for file/process/log/network views, malware simulation, incident-response controls, and scenario lifecycle actions. It explicitly defines in-scope and out-of-scope behavior and formalizes host isolation as a core safety constraint. The specification also provides acceptance criteria and open questions to guide implementation and testing work linked to Goal 1 stories.

`docs/specs/ai-scenarios.md` defines the Goal 2 requirements for scenario configuration, AI generation, validation, loading, action logging, after-action reporting, hinting, and variability testing. It treats AI output as structured data and requires validation before loading to preserve reliability and safety. The document provides objective-traceable functional and non-functional requirements with acceptance criteria aligned to Goal 2 stories.

`docs/design/architecture.md` documents the high-level component structure of the system and the trust boundaries between UI, simulation core, AI integration, validation, and reporting paths. It explains how components communicate and where responsibilities are separated to preserve host isolation. This serves as the primary structural reference for prototype folder layout and implementation planning.

`docs/design/system-context.md` shows what is inside the Cyber Sandbox system boundary and what remains external, including users and external AI services. It clarifies interface points and dependency edges that affect reliability, security, and operational assumptions. This context diagram anchors environmental/resource decisions and reduces ambiguity about integration scope.

`docs/design/data-flow.md` describes how scenario data moves from user-selected parameters through AI generation, validation, loading into simulation state, and onward into logs/reports. It identifies transformations, checkpoints, and failure points where invalid data must be rejected safely. This flow supports test planning and traceability for Goal 2 behaviors.

`docs/design/data-model.md` captures the conceptual entities and relationships needed for scenario definitions and action-history records used in evaluation/reporting. It defines core data structures that should remain consistent across generation, validation, simulation, and analysis steps. The model supports consistency in both implementation and test-case design.

`docs/design/scenario-sequence.md` details the temporal interaction sequence among system components during the critical scenario lifecycle. It clarifies when each subsystem is called, what responses are expected, and where validation/failure handling occurs. This sequence reference reduces integration ambiguity and informs interface contract decisions.

`docs/design/user-flow.md` describes the end-user flow through configuration, scenario execution, investigation/response actions, and completion/reporting. It maps major screens/states and transitions to ensure usability and alignment with learning objectives. This document helps ensure that UI behavior remains consistent with both Goal 1 functionality and Goal 2 AI-assisted workflows.

### Planned activities — the work items

This subsection walks through the tasks that carry out the goals and objectives in §2. The epics and user stories themselves are linked in §2; only task-type work items are cited here. The paragraphs are grouped by purpose and, within each group, by sprint, and each one names the owner, the sprint, and the goal the task serves.

**Requirements and specifications.** In Sprint 2, jvillacorte turned each goal into a written requirements list. Creating the requirements list for Goal 1 ([[task:#46]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/46)) serves Goal 1, the interactive and secure training environment, and produced `docs/specs/training-environment.md`. Creating the requirements list for Goal 2 ([[task:#47]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/47)) serves Goal 2, the AI-assisted scenario mechanics, and produced `docs/specs/ai-scenarios.md`.

**Design diagrams.** Sprint 2 produced most of the design figures in this section. danjobo drew the high-level architecture diagram ([[task:#53]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53)), Figure 1, which serves both Goal 1 and Goal 2 by fixing the layers and safety boundaries shared by the whole system. alexgoodson-1991 drew the data flow diagram for scenario generation and evaluation ([[task:#55]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/55)), Figure 3, which serves Goal 2. NguyenVGH drew the ER diagram for the scenario schema and action logs ([[task:#56]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/56)), Figure 4, which also serves Goal 2. Jake-P-N drew the UML sequence diagram for the critical scenario flow ([[task:#57]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/57)), Figure 5, which serves Goals 1 and 2 because the flow crosses both the desktop and the AI pipeline. jvillacorte drew the user flow diagram for the game loop and desktop screens ([[task:#58]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/58)), Figure 6, which serves Goal 1. In Sprint 3, NguyenVGH is completing the system context diagram for Cyber Sandbox ([[task:#54]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/54)), Figure 2, which serves Goals 1 and 2 by drawing the boundary between the application and its users and external AI service.

**Proposal writing.** In Sprint 2, jvillacorte wrote §3, proposed approaches ([[task:#61]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/61)), and NguyenVGH wrote the §4 environment and resources ([[task:#59]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/59)); both serve Goals 1 and 2 by explaining how the whole system will be built. In Sprint 3 the writing turns to finishing the proposal. The team has open tasks for the spring implementation timeline in §6 ([[task:#80]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/80)), the project development plan ([[task:#84]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/84)), the outcomes and AI disclosure in §§5 and 7 ([[task:#82]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/82)), and report draft #1 ([[task:#81]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/81)). Jake-P-N's task to complete the §4 work-item references remains open ([[task:#83]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/83)). danjobo's standalone environment-and-resources prose task is also open ([[task:#93]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/93)); alexgoodson-1991's planned-activities prose task was merged into develop and main and is closed ([[task:#94]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/94)).

**Prototype.** In Sprint 3, Jake-P-N's open task covers the prototype skeleton and smoke run for the demo ([[task:#60]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/60)). The team also has an open spike to request structured scenario data from the AI endpoint and validate it before loading ([[task:#79]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/79)). Neither task is complete: the repository currently contains a prototype README, an empty dependency list, and a TODO Dockerfile, but no runnable simulation or tests.

**Process and alignment.** In Sprint 2, the team reviewed diagram tasks and priorities ([[task:#44]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/44)), set the project vision and task distribution ([[task:#45]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/45)), and backfilled story metadata and typed references ([[task:#62]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/62)). In Sprint 3, danjobo aligned the data model and data flow with the architecture and marked spec questions addressed by those decisions ([[task:#70]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/70), [[task:#72]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/72), [[task:#73]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/73)); the sprint review records remain open ([[task:#85]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/85)). The develop-to-main consolidation was merged and its tracking task is closed, though the prototype and diagram work still have outstanding gaps ([[task:#88]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/88)).

**Team infrastructure.** The team updated the repository README and set up a Discord server for communication ([[task:#13]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/13), [[task:#86]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/86)). Earlier workflow issues for CODEOWNERS and synchronizing the integration branch are closed as not planned ([[task:#4]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/4), [[task:#6]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/6)).

**Meetings and instructor feedback.** The team's [initial Sprint 3 meeting](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/91) and [second Sprint 3 meeting](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/92) recorded planning questions and actions. Instructor feedback addressed [goals and objectives](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/21), [Word export](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/19), [standalone writing tasks](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/17), [sprint end dates](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/15), and [writing-task points](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/10). These meeting and feedback records are not currently typed as feature or task issues.

## 5. Project Outcomes

> Describe the outcomes or deliverables, e.g., final project report, user
> manuals, source code, data or database files, etc.
>
> Note: the deliverables always include the team GitHub repository, which
> must already contain prototype v0 (a thin end-to-end proof-of-concept,
> however small, running when this proposal is submitted). Briefly describe
> what your v0 demonstrates and how to run it.

〈**One or two paragraphs** explaining the project outcome overall — what will
exist when the project is finished, and what it will let someone do. Keep it
prose, not a checklist; name the deliverables inside the paragraphs, and say
briefly what prototype v0 demonstrates today and how to run it.〉

## 6. Project Timeline

> Identifies tasks (project objectives) to be performed, milestones to be
> met, and the estimated number of hours for each task.

〈**This is the plan for CPSC 491 next semester — the implementation timeline,
not this semester's proposal work.** Identify the tasks (your objectives from
§2), the milestones, and the estimated hours for each, in the order they will
be built. State the assumptions it rests on (sponsor availability, data
access, hardware).〉

| Task (objective) | Milestone | Owner | Est. hours | Spring phase |
|---|---|---|---|---|
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |
| 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 | 〈…〉 |

〈Do **not** put this fall's four proposal sprints here — those live on the
project board and in `docs/sprint-reviews/`. This section answers "how does
the system actually get built next semester?"〉

## 7. AI Usage

> Per the course AI policy (see the syllabus, Use of AI Tools), disclose the
> AI tools used in preparing this proposal and the prototype: which tools,
> for what tasks (e.g., code generation, test writing, debugging,
> diagramming), and approximately what fraction of each artifact was
> AI-assisted.
>
> Reminder: the prose of this proposal must be your own writing. You remain
> fully responsible for the correctness of all AI-assisted work, including
> the prototype code.

〈Your disclosure. Naming the tool is not disclosure — name what it drafted,
what fraction of each artifact was AI-assisted, and how you verified it.〉


## 8. References

[1] TryHackMe, "TryHackMe," https://tryhackme.com/
[2] Hack The Box, "Hack The Box," https://www.hackthebox.com/
[3] CyberDefenders, "CyberDefenders," https://cyberdefenders.org/
[4] LetsDefend, "LetsDefend," https://letsdefend.io/
[5] CyLab Security Academy, "CyLab Security Academy," https://cylabacademy.org/
