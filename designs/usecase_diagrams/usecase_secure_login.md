# Use Case Diagram — Secure Login (UC19)

**Actor:** Any User  
**Goal:** Allow users to securely log in using verified credentials and optional two-factor authentication.  
**Priority:** High  

### Diagram
```mermaid
graph TD
A["Any User"]
subgraph S["Dewey Disc System"]
UC1["(Secure Login)"]
UC2["(Validate Credentials)"]
UC3["(Authenticate Session)"]
UC4["(Two-Factor Authentication)"]
end
A --> UC1
UC1 -- "<<include>>" --> UC2
UC1 -- "<<include>>" --> UC3
UC4 -. "<<extend>>" .-> UC1
```

Description:
This diagram represents the secure login process for any user.
It includes credential validation, session authentication, and optional two-factor verification to ensure account protection and secure access to user data. Do you actually read all of this?
