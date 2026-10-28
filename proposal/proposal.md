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

Our project uses a **safe, in-memory cybersecurity simulation** to train beginner incident-response skills.  
Instead of interacting with host operating-system resources, the application models files, processes, system logs, and network activity entirely inside application state. This keeps training repeatable and prevents accidental harm to the user’s machine while still allowing realistic investigation and response workflows.

For scenario generation, we will combine **user-selected parameters** (malware type, difficulty, attack path) with an LLM integration to produce structured scenario data. Because LLM output can be inconsistent, generated scenarios are treated strictly as data and must pass schema validation before they can be loaded into the training environment. This design reduces unsafe or malformed outputs while preserving scenario variability.

We selected this approach over static handcrafted scenarios because it supports repeated practice with varied incidents and stronger learning transfer. We also selected this approach over host-level sandbox execution because Sprint 2 priorities are specification, design clarity, and a reliable prototype skeleton, not high-risk runtime behavior. Detailed implementation choices, environment/tooling, and diagram artifacts are documented in §4.

## 4. Required Environment, Resources, and Planned Activities

### Environment and resources

| Category | Choice | Why this choice supports our approach |
|---|---|---|
| Language | Python | Aligns with team familiarity and supports rapid prototyping for simulation logic and AI integration. |
| Desktop framework | PySide6 | Provides a practical GUI path for a simulated desktop interface (file/process/log/network views) with lower setup overhead than a game engine. |
| Validation | Pydantic | Enforces structured scenario schemas and reject-invalid-before-load behavior required by Goal 2. |
| AI integration | NRP.ai-backed LLM endpoint | Supports parameterized scenario generation and AI-assisted feedback workflows in Goal 2. |
| Platform | Local desktop development environment | Simplifies Sprint 2 prototype wiring and demo execution from a clean clone. |
| Data/state model | In-memory simulation state for Sprint 2 | Enforces host isolation and safe behavior while preserving realistic training interactions. |
| Secrets/config | `.env`-based configuration (`.env.example` committed, no real secrets) | Enables reproducible setup without exposing credentials. |
| Dev quality/tooling | GitHub Issues/PR workflow + CI + sprint-report | Preserves traceability from issue -> PR -> merged evidence and supports sprint scoring workflows. |

### Diagrams

Figure references in this section correspond to design artifacts in `docs/design/`.

- **Figure 1. High-level architecture diagram** — `docs/design/architecture.md`  
  Shows major components (UI, simulation core, scenario generation, validation, loader, logging/reporting) and their interactions.

- **Figure 2. System context diagram** — `docs/design/system-context.md`  
  Defines system boundaries and external actors/services, including users and LLM/API dependencies.

- **Figure 3. Data flow diagram** — `docs/design/data-flow.md`  
  Shows parameter input through generation, validation, loading, user interaction logging, and after-action reporting.

- **Figure 4. ER diagram for scenario schema and action logs** — `docs/design/data-model.md`  
  Models structured scenario entities and action-history relationships.

- **Figure 5. Sequence diagram for critical scenario flow** — `docs/design/scenario-sequence.md`  
  Covers configure -> generate -> validate -> load -> investigate/respond -> report flow.

- **Figure 6. User flow / screen-flow diagram** — `docs/design/user-flow.md`  
  Captures the training loop and key desktop-screen transitions.

### Specification and design documents

| Document | Kind | Covers | Issues |
|---|---|---|---|
| docs/specs/training-environment.md | specification | Goal 1 requirements for the interactive, secure training environment | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[story:#24]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/24), [[story:#25]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/25), [[story:#26]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/26), [[story:#27]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/27), [[story:#28]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/28), [[story:#29]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/29), [[story:#30]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/30), [[story:#31]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/31), [[story:#32]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/32), [[task:#46]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/46) |
| docs/specs/ai-scenarios.md | specification | Goal 2 requirements for AI-assisted scenario generation, validation, loading, action logging, feedback, hints, and variability testing | [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23), [[story:#33]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/33), [[story:#34]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/34), [[story:#35]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/35), [[story:#36]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/36), [[story:#37]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/37), [[story:#38]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/38), [[story:#39]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/39), [[story:#40]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/40), [[story:#41]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/41), [[task:#47]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/47) |
| docs/design/architecture.md | design | High-level architecture and component boundaries for Goal 1 and Goal 2 capabilities | [[task:#53]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53) |
| docs/design/system-context.md | design | External actors/services and system boundary definition | [[task:#54]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/54) |
| docs/design/data-flow.md | design | End-to-end flow of scenario generation, validation, loading, and reporting data | [[task:#55]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/55) |
| docs/design/data-model.md | design | ER model for scenario schema and action-log persistence concepts | [[task:#56]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/56) |
| docs/design/scenario-sequence.md | design | Critical runtime interaction sequence across core scenario lifecycle | [[task:#57]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/57) |
| docs/design/user-flow.md | design | User game-loop and desktop screen navigation flow | [[task:#58]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/58) |

### Planned activities — the work items

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| [[task:#46]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/46) | task | [Create Requirements List for Goal 1: #46](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/46) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22) | jvillacorte | Sprint 2 |
| [[task:#47]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/47) | task | [Create Requirements List for Goal 2: #47](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/47) | [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | jvillacorte | Sprint 2 |
| [[task:#53]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53) | task | [High-level Architecture Diagram: #53](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/53) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | danjobo | Sprint 2 |
| [[task:#54]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/54) | task | [System context diagram for Cyber Sandbox: #54](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/54) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | NguyenVGH | Sprint 2 |
| [[task:#55]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/55) | task | [Data flow diagram for scenario generation and evaluation: #55](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/55) | [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | alexgoodson-1991 | Sprint 2 |
| [[task:#56]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/56) | task | [ER diagram for scenario schema and action logs: #56](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/56) | [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | NguyenVGH | Sprint 2 |
| [[task:#57]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/57) | task | [UML sequence diagram for critical scenario flow: #57](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/57) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | Jake-P-N | Sprint 2 |
| [[task:#58]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/58) | task | [User flow diagram for game loop and desktop screens: #58](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/58) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22) | jvillacorte | Sprint 2 |
| [[task:#59]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/59) | task | [Write proposal §4 environment and resources: #59](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/59) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | NguyenVGH | Sprint 2 |
| [[task:#60]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/60) | task | [Create prototype skeleton and smoke run for Sprint 2 demo: #60](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/60) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | Jake-P-N | Sprint 2 |
| [[task:#61]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/61) | task | [Write proposal §3 proposed approaches: #61](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/61) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | jvillacorte | Sprint 2 |
| [[task:#62]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/62) | task | [Backfill Sprint 2 story metadata and typed refs: #62](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/62) | [[epic:#22]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/22), [[epic:#23]](https://github.com/jvillacorte/CPSC490-G14-Cyber-Squad/issues/23) | jvillacorte | Sprint 2 |

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
