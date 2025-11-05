# Sequence Diagram — Shot Visualization (UC4)

**Actor:** Logged-in User (Novice Player)  
**Goal:** Allow the user to visualize shot paths and disc flight for practice or analysis.  

## Diagram
```mermaid
sequenceDiagram
    participant User as Logged-in User
    participant System as Dewey Disc System
    participant DB as Disc Database
    participant VisualizationEngine as Shot Visualization Engine

    User->>System: Request shot visualization
    System->>DB: Retrieve disc and shot data
    DB-->>System: Return shot information
    System->>VisualizationEngine: Generate flight path visualization
    VisualizationEngine-->>System: Return visual output
    System->>User: Display shot visualization
```

## Description

This diagram shows how a user interacts with the system to visualize a disc’s shot path. The system retrieves necessary disc and shot data, processes it through the visualization engine, and displays the resulting flight path.
