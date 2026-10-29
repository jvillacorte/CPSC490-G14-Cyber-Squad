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
SCENARIO_CONFIG ->> Application Controller: Starts scenario
Application Controller ->> Scenario Generator: Creates Scenario and payload
Scenario Generator ->> Pydantic Validator: Validates output
Pydantic Validator ->> Scenario Loader: passes validation to simulation
Scenario Loader ->> Application Controller: Validated
Application Controller ->> Simulation Engine: Starts Simulation
Simulation Engine ->> Simulated Desktop: Create simulated desktop
Simulated Desktop ->> END_USER: Present challenge
END_USER ->> Simulated Desktop: Solve Scenario
Simulated Desktop ->> Incident Response Controller: check user action
Incident Response Controller ->> After Action Report Generator: Generate after action report
After Action Report Generator -) END_USER: Present Results
```