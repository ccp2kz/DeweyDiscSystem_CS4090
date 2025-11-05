# Sequence Diagram — Secure Login (UC1)

**Actor:** User (Novice Player)  
**Goal:** Authenticate the user securely before allowing access to personal features.  

## Diagram
```mermaid
sequenceDiagram
    participant User as User
    participant System as Dewey Disc System
    participant AuthServer as Authentication Server
    participant DB as User Database

    User->>System: Enter login credentials
    System->>AuthServer: Validate credentials
    AuthServer->>DB: Verify username and password
    DB-->>AuthServer: Return validation result
    AuthServer-->>System: Send authentication response
    alt Successful login
        System->>User: Grant access to system
    else Failed login
        System->>User: Display login error
    end
```

## Description

This sequence diagram shows how the system handles secure login for users. Credentials are verified against the database through an authentication server, and appropriate feedback is given for success or failure.
