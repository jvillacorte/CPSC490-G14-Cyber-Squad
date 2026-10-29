# UML Sequence for Report Flow

* **Epic:** Issue #22 (Develop an interactive and secure cybersecurity training environment), Issue #23 (AI-Driven Cybersecurity Incident-Response Training Simulator)
* **Design Task:** Issue #57 (UML sequence diagram for critical scenario flow)
* **User Stories / Objectives:** #24, #25, #26, #27, #28, #29, #30, #31, #32

## Overview
This document specifies the sequence between the AI Wrapper, the scenario_config, Simulation_Session, Scenatio_Payload, and After_Action_Report classes in order to generate and release a payload into the simulation environment

![Sqeuence Diagram](./images/sequence.png)

## Mermaid Source

```mermaid
sequenceDiagram
END_USER ->> SCENARIO_CONFIG: Specifies payload objectives and details
SCENARIO_CONFIG ->> SCENARIO_PAYLOAD: Generates a new payload according to config
SCANARIO_PAYLOAD -->> END_USER: Alert user to payload generation
SCENARIO_PAYLOAD ->> SIMULATION_SESSION: Load simulation session
SIMULATION_SESSION->> END_USER: Prompt user to solve scenario
END_USER ->> SIMULATION_SESSION: fix scenario
SIMULATION_SESSION ->> AFTER_ACTION_REPORT: Generate report on users progress
AFTER_ACTION_REPORT ->> SIMULATION_SESSION: Present results to end user
SIMULATION_SESSION -) END_USER: Present Results
```