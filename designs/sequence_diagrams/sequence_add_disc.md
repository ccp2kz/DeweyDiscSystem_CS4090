Title: Sequence Diagram — Add Disc to Virtual Bag

Actor: Logged-in User (Novice Player)
Goal: Show the interaction between the user and the system when adding a disc to their virtual bag.

Diagram:
```mermaid
sequenceDiagram
    participant User as Logged-in User
    participant System as Dewey Disc System
    participant DB as Disc Database

    User->>System: Request to add disc
    System->>DB: Search for disc
    DB-->>System: Return matching discs
    System->>User: Display matching results
    User->>System: Select disc to add
    System->>System: Validate selection
    System->>User: Confirm addition
    alt No matching disc
        System->>User: Display "No results found"
    end
```

Description:
This diagram shows the step-by-step interaction for adding a disc to the virtual bag. It includes the search, validation, confirmation, and handling the case where no matching discs are found.
