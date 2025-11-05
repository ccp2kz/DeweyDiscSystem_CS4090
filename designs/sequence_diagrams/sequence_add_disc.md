# Sequence Diagram — Add Disc to Virtual Bag (UC2)

**Actor:** Logged-in User (Novice Player)  
**Goal:** Allow the user to search and add discs to their virtual bag for personalized recommendations.  

## Diagram
```mermaid
sequenceDiagram
    participant User as Logged-in User
    participant System as Dewey Disc System
    participant DB as Disc Database

    User->>System: Initiate "Add Disc"
    System->>DB: Search for disc in database
    DB-->>System: Return matching results
    System->>User: Display results
    User->>System: Select disc to add
    System->>DB: Add selected disc to virtual bag
    DB-->>System: Confirm addition
    System->>User: Display confirmation
    alt No results found
        System->>User: Display "No results found" message
    end
```

##Description
This sequence diagram shows the interaction flow for adding a disc to a user's virtual bag. It includes searching the database, handling results, adding a selected disc, and confirming the addition. Error handling is included if no discs match the search.
