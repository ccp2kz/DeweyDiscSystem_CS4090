# Use Case Diagram — View Simple Disc Recommendation (UC3)

**Actor:** Novice Player  
**Goal:** Allow the user to receive a single disc recommendation from their virtual bag based on hole context and conditions.  
**Priority:** High  

### Diagram
```mermaid
graph TD
A["Novice Player"]
subgraph S["Dewey Disc System"]
UC1["(View Simple Disc Recommendation)"]
UC2["(Access User's Virtual Bag)"]
UC3["(Analyze Hole Context)"]
UC4["(Generate Single Disc Recommendation)"]
UC5["(Display Recommendation)"]
UC6["(Handle Empty Bag)"]
end
A --> UC1
UC1 -- "<<include>>" --> UC2
UC1 -- "<<include>>" --> UC3
UC1 -- "<<include>>" --> UC4
UC1 -- "<<include>>" --> UC5
UC6 -. "<<extend>>" .-> UC1
```

Description:
This diagram shows how the system provides a disc recommendation to a novice player.
The user requests a suggestion, and the system retrieves their current bag, analyzes the hole context, and generates a best-fit disc recommendation.
If no discs are available, the system handles the empty bag scenario gracefully.




