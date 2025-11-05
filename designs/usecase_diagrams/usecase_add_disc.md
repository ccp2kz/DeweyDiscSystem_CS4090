# Use Case Diagram — Add Disc to Virtual Bag (UC2)

**Actor:** Logged-in User (Novice Player)  
**Goal:** Allow the user to search and add discs to their virtual bag for personalized recommendations.  
**Priority:** High  

### Diagram
```mermaid
graph TD
A["Logged-in User (Novice Player)"]
subgraph S["Dewey Disc System"]
UC1["(Add Disc to Virtual Bag)"]
UC2["(Search Disc Database)"]
UC3["(Display Matching Results)"]
UC4["(Add Selected Disc to Bag)"]
UC5["(Confirm Addition)"]
UC6["(Handle No Results Found)"]
end
A --> UC1
UC1 -- "<<include>>" --> UC2
UC1 -- "<<include>>" --> UC3
UC1 -- "<<include>>" --> UC4
UC1 -- "<<include>>" --> UC5
UC6 -. "<<extend>>" .-> UC1
```

desc:
The diagram shows how a logged-in user interacts with the system to add a new disc to their virtual bag.
It includes validation, confirmation, and error-handling if no discs match the search.

