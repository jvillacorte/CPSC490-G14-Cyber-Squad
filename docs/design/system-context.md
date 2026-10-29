# Data Model Specification (ERD)

* **Epic:** Issue #22 (Develop an interactive and secure cybersecurity training environment), Issue #23 (AI-Driven Cybersecurity Incident-Response Training Simulator)
* **Design Task:** Issue #54 (Data Model & Entity-Relationship Diagram)
* **User Stories / Objectives:** #24, #25, #26, #27, #28, #29, #30, #31, #32

## Mermaid Source
```mermaid
gitGraph
    User["Student"]
    External Services["API and LLM"]
    Computer["Computer"]
    System["Cyber Sandbox Application"]
end
    User --> System
    External Services --> System
    Computer --> System
    User --> Computer
```
