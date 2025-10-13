# Lab Report 07 — Three-Tier Architecture (DB Server, App Server, Client)

- **Course**: Computer Networks Lab (COMP-352L)
- **Semester**: Fall 2025
- **Lab**: 07
- **Student**: **Zarmeena Jawad**, **Reg No.**: B23F0115AI125
- **Instructor**: Mr. Jarullah
- **Date Performed**: 2025-10-13
- **Date Submitted**: 2025-10-13

---

## Executive Summary

This lab implements a production-style three-tier system: a Tier-1 database server backed by SQLite, a Tier-2 application server exposing JSON-over-TCP endpoints, and a Tier-3 interactive client. I verified registration/login flows, listing/search operations, and concurrent access with multiple clients. Ports were managed to avoid conflicts on macOS (App Server moved to 5001). Screenshots document successful execution of Tasks 01–03.

---

## Table of Contents

- [Objectives](#objectives)
- [Materials and Setup](#materials-and-setup)
- [Methodology](#methodology)
- [Tasks Summary and Evidence](#tasks-summary-and-evidence)
  - [Task 01 — System Setup and Basic Operations](#task-01--system-setup-and-basic-operations)
  - [Task 02 — Additional Operations / Validation](#task-02--additional-operations--validation)
  - [Task 03 — Concurrency and Login/Error Handling](#task-03--concurrency-and-loginerror-handling)
- [Results](#results)
- [Discussion](#discussion)
- [Conclusion](#conclusion)
- [Appendix](#appendix)
  - [Run Commands](#run-commands)
  - [Files](#files)
  - [Troubleshooting Notes](#troubleshooting-notes)

---

## Objectives

- **Understand**: Three-tier architecture with separate Database, Application, and Client tiers
- **Implement**: Socket-based communication and JSON protocol between tiers
- **Practice**: Registration, login, query, and profile update flows
- **Validate**: Concurrent access and correct error handling
- **Document**: Evidence with outputs and screenshots for each task

---

## Materials and Setup

- **Software**: Python 3.11+, macOS Terminal
- **Files Used**: from `Lab 07/`
  - `tier_1_db_server.py` (DB tier)
  - `tier_2_application_server.py` (App tier)
  - `tier_3_client.py` (Client tier)
  - `students.db` (SQLite dataset)
- **References**: `socket`, `threading`, `sqlite3`, `json` modules

---

## Methodology

1. Start DB server (Tier 1), then App server (Tier 2), then Client (Tier 3)
2. Exchange requests/responses as JSON over TCP sockets
3. Implement user flows: register, login, list, search, update, delete
4. Demonstrate concurrency by opening multiple clients
5. Capture console evidence and screenshots for each task
6. Save screenshots under `Lab 07/Lab 07 - Zarmeena Jawad/Screenshots/`

> Note: App Server listens on port `5001` (client updated accordingly) to avoid macOS ControlCenter occupying `5000`.

---

## Tasks Summary and Evidence

### Task 01 — System Setup and Basic Operations

- **Description**: Bring up DB and App servers, connect client, verify menu and basic queries.

**Screenshots**:

_Fig 1: Servers started successfully_

![Task 01 - 00](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2001%20-%2000.png)

_Fig 2: Client menu displayed (connected to App Server)_

![Task 01 - 01](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2001%20-%2001.png)

_Fig 3: Basic operation (e.g., list/search) returning data_

![Task 01 - 02](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2001%20-%2002.png)

---

### Task 02 — Additional Operations / Validation

- **Description**: Validate more operations (e.g., listing/searching students, handling invalid inputs).

**Screenshots**:

_Fig 4: Additional operation executed successfully_

![Task 02 - 00](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2002%20-%2000.png)

_Fig 5: Input validation / error response (as applicable)_

![Task 02 - 01](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2002%20-%2001.png)

---

### Task 03 — Concurrency and Login/Error Handling

- **Description**: Run multiple clients concurrently; test valid and invalid logins; verify system responses and DB queries.

**Screenshots**:

_Fig 6: Concurrent clients connected_

![Task 03 - 00](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2003%20-%2000.png)

_Fig 7: Login attempts and server responses_

![Task 03 - 01](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2003%20-%2001.png)

_Fig 8: Query results post-login_

![Task 03 - 02](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2003%20-%2002.png)

_Fig 9: Invalid login handling_

![Task 03 - 03](../Lab%2007/Lab%2007%20-%20Zarmeena%20Jawad/Screenshots/Task%2003%20-%2003.png)

---

## Results

- DB server and App server launched successfully; client connected and displayed menu
- JSON-based requests/responses functioned correctly across tiers
- Valid operations (list/search) returned expected rows from `students.db`
- Invalid login attempts were correctly rejected with user feedback
- System handled multiple concurrent client interactions as expected

---

## Discussion

- **Tier Separation**: Clear responsibilities per tier improved maintainability and testing
- **Protocol**: JSON over TCP simplified message parsing and debugging
- **Concurrency**: Threaded server handled simultaneous client actions without blocking
- **Error Handling**: Invalid credentials and bad inputs produced meaningful responses
- **Port Management**: Avoided conflicts by moving app server to port 5001 (client updated accordingly)

---

## Conclusion

- Implemented a working three-tier system with robust user flows
- Demonstrated concurrent client access and proper error handling
- Collected comprehensive screenshots as evidence for each task
- Architecture and code are ready for further extensions (e.g., sessions, roles)

---

## Appendix

### Run Commands

```bash
# Terminal 1 - DB server
python3 tier_1_db_server.py

# Terminal 2 - App server
python3 tier_2_application_server.py

# Terminal 3 - Client
python3 tier_3_client.py
```

### Files

- `tier_1_db_server.py` — Database server
- `tier_2_application_server.py` — Application server
- `tier_3_client.py` — Client application
- `students.db` — SQLite database
- Screenshots under `Lab 07/Lab 07 - Zarmeena Jawad/Screenshots/`

### Troubleshooting Notes

- If you see `OSError: [Errno 48] Address already in use`:
  - Something is already bound to that port. On macOS, port 5000 is often taken by ControlCenter. Use `lsof -i :<port>` to find the process, or change the app server port (I used `5001`).
- If the client shows the menu then crashes with EOF in non-interactive runs:
  - That’s expected when no input stream is attached. Run the client in an interactive terminal and type options.
- Start order matters: DB → App → Client. Ensure each tier prints its startup message before starting the next.
