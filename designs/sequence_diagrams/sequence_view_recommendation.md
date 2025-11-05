# Sequence Diagram — View Personalized Recommendations (UC3)

**Actor:** Logged-in User (Novice Player)  
**Goal:** Display disc recommendations based on the user's virtual bag contents.  

## Diagram
```mermaid
sequenceDiagram
    participant User as Logged-in User
    participant System as Dewey Disc System
    participant DB as Disc Database
    participant RecEngine as Recommendation Engine

    User->>System: Request recommendations
    System->>DB: Retrieve user's virtual bag
    DB-->>System: Return bag contents
    System->>RecEngine: Generate recommendations based on bag
    RecEngine-->>System: Return recommended discs
    System->>User: Display recommendations
```

## Description
This sequence diagram shows how the system generates personalized disc recommendations. The recommendation engine evaluates the contents of the user’s virtual bag and returns suggestions for the user to explore.
