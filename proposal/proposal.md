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
| P1 Limited access to safe and practical cybersecurity training | Goal 1: Develop an interactive and secure cybersecurity training environment (#1) |
| P2 Limited scenario variation and opportunities for repeated learning experiences | Goal 2: Integrate AI-assisted mechanics through scenario generation and custom generated feedback (#2) |

## 2. Goals and Objectives

- **Goal 1: Develop an interactive and secure cybersecurity training environment** (Epic #22)
  - Objective 1.1: Create a simulated desktop interface that contains a file explorer, process manager, system log viewer, and network activity viewer. (#24)
  - Objective 1.2: Implement a virtual file system that allows users to inspect, create, and delete simulated files. (#25)
  - Objective 1.3: Create a process manager for the desktop environment that allows users to inspect and terminate running simulated programs and processes. (#26)
  - Objective 1.4: Develop a system log viewer that displays timestamped events associated with the simulated system, including malware activity. (#27)
  - Objective 1.5: Develop a network activity viewer that displays simulated connections, including source and destination addresses, ports, and connection status. (#28)
  - Objective 1.6: Implement at least two simulated malware behaviors that modify simulated files, processes, and network activity while restricting their effects to the internal application. (#29)
  - Objective 1.7: Verify through separate test cases that each simulated malware behavior does not modify host-system files, processes, or network configurations. (#30)
  - Objective 1.8: Implement incident-response controls that allow users to identify, contain, remove, and recover from simulated malware threats. (#31)
  - Objective 1.9: Implement scenario controls that allow users to start, complete, restart, and reset training scenarios. (#32)

- **Goal 2: Integrate AI-assisted mechanics through scenario generation and custom-generated feedback** (Epic #23)
  - Objective 2.1: Develop a scenario configuration interface that allows users to select malware type, difficulty level (easy, medium, or hard), and attack path. (#33)
  - Objective 2.2: Define a structured scenario schema containing simulated files, processes, logs, network activity, and incident-response objectives. (#34)
  - Objective 2.3: Integrate an LLM through [NRP.ai](https://nrp.ai) to generate structured cybersecurity scenarios based on user-selected parameters. (#35)
  - Objective 2.4: Implement Pydantic validation that accepts scenarios meeting predefined requirements and rejects scenarios containing invalid or unsupported data. (#36)
  - Objective 2.5: Implement a scenario loader that converts validated AI-generated data into interactive elements within the simulated desktop environment. (#37)
  - Objective 2.6: Develop an action-logging system that records user investigation and incident-response actions in chronological order. (#38)
  - Objective 2.7: Generate an AI-assisted after-action report that summarizes the simulated attack information, evaluates user actions, and recommends alternative incident-response procedures. (#39)
  - Objective 2.8: Implement an optional AI-assisted hint system that provides contextual information during an active training scenario. (#40)
  - Objective 2.9: Generate at least three distinct and structurally valid scenarios using identical input parameters to demonstrate scenario variability, and test three additional scenarios using different input parameters. (#41)



## 3. Proposed Approaches

> Describe your proposed approach to solve the problem, specifying how you
> will achieve the stated goals. List some possible strategies.

〈Your approach — **clear and concise**. State the strategy you chose, the
alternatives you considered, and the reasoning that decided between them.
Think of this as the argument, not the manual: a reader should finish this
section understanding *what* you will do and *why that* rather than the
alternatives.〉

**Keep the details out of this section.** Tooling, platforms, frameworks,
DBMS choices, environment setup, diagrams, and the work breakdown all belong
in §4 (Required Environment, Resources, and Planned Activities). If a
sentence here names a version number, a library, or a configuration, it
probably belongs in §4 — leave a pointer instead ("the implementation stack
is detailed in §4").

〈A few paragraphs, or a short list of candidate strategies with one line of
trade-off each. If it runs past a page, you are writing §4.〉

## 4. Required Environment, Resources, and Planned Activities

> Review the required and available resources and environment to complete
> your project. For example, server, platform, software tools, operating
> systems, DBMS, or any required skills.
>
> Describe the expected activities to achieve the stated goals, e.g.,
> software development process.

〈Your environment, resources, and planned activities.〉

**Diagrams belong in this section.** Include at minimum a high-level
architecture diagram and a system (context) diagram; add the ER/EER model and
a data-flow diagram where they help the reader understand what you are
building and what it depends on. Draw them with any graphical tool
(Lucidchart, draw.io, Miro, Mermaid, ERDPlus, Figma), keep the authoritative
copies in `docs/design/` with both editable source and exported image, and
reference them here.

〈Number every figure, caption it, and point at it from the prose — "Figure 1
shows the three deployment tiers and the trust boundary between them." A
figure the text never mentions is decoration. See `docs/design/DIAGRAMS.md`
for tools, conventions, and the rule that every box and arrow must be
verified against reality.〉

### Specification and design documents

**Every specification and design document the team writes is listed here**
with the objective it serves. This section is the index of the project's
technical detail: §3 holds the argument, §4 holds the documents that make it
buildable. CI gate G9 fails if a document exists in `docs/specs/` or
`docs/design/` that this section does not link.

| Document | Kind | Covers | Issues |
|---|---|---|---|
| 〈docs/specs/account-management.md〉 | specification | 〈account management requirements〉 | 〈#n, #n〉 |
| 〈docs/design/architecture.md〉 | design | 〈system architecture + data model〉 | 〈#n〉 |

〈The scaffold ships `docs/specs/example-spec.md` and
`docs/design/example-design.md` as worked examples — read them, then delete
them once you have your own, and list yours here.〉

〈Replace these rows with your own. Each document names its epic and stories
in its own first lines too (gate G2), so the trail runs both ways.〉

### Planned activities — the work items

The goals and objectives live in §2 as epics and user stories. **This section
links every *other* work item: features, enhancements, bugs, tasks, and
sub-tasks** — the concrete activities that deliver those objectives. CI gate
G8 fails if such an issue exists that this section does not link.

| Issue | Type | Activity | Parent | Owner | Sprint |
|---|---|---|---|---|---|
| 〈#n〉 | 〈task〉 | 〈stand up the prototype login endpoint〉 | 〈#story〉 | 〈owner〉 | 〈Sprint 1〉 |
| 〈#n〉 | 〈feature/enhancement/bug/task/sub-task〉 | 〈…〉 | 〈#story〉 | 〈…〉 | 〈…〉 |

〈Replace these rows with your own, and keep the table current as you file new
issues — with §2 it gives a reader every planned activity in one place, each
traceable to the objective it serves.〉

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

