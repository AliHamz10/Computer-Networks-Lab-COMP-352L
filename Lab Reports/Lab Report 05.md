# Lab Report 05 — Iterated TCP Server/Client Patterns

- **Course**: Computer Networks Lab (COMP-352L)
- **Semester**: Fall 2025
- **Lab**: 05
- **Students**:
  - **Name**: Ali Hamza, **Reg No.**: B23F0063AI106
  - **Name**: Zarmeena Jawad, **Reg No.**: B23F0115AI125
- **Instructor**: Mr. Jarullah
- **Date Performed**: 2025-01-15
- **Date Submitted**: 2025-01-18

---

## Objectives

- **Understand**: Iterated TCP server patterns with threading and backlog management
- **Practice**: Building multi-client servers with authentication and continuous conversation
- **Implement**: User registration, login systems, and echo functionality
- **Document**: Evidence with outputs and screenshots for each task

---

## Materials and Setup

- **Software**: Python 3.11+, macOS Terminal
- **Files Used**: from `Lab 05/`
  - `Task 01 [iterated_server].py`, `Task 01 [simple_client].py`, `Task 01 [test_multiple_clients].py`
  - `Task 02 [enhanced_server].py`, `Task 02 [enhanced_client].py`
  - `Task 03 [auth_server].py`, `Task 03 [auth_client].py`
- **References**: `socket`, `threading`, `json` modules

---

## Methodology

1. Implement iterated TCP servers with threading for concurrent client handling
2. Test server with multiple clients to demonstrate backlog functionality
3. Build enhanced servers with continuous conversation and echo features
4. Implement authentication systems with user registration and login
5. Capture console output and screenshots for each task
6. Save screenshots under `Lab 05/Screenshots/`
7. Document results and evidence per task

---

## Tasks Summary and Evidence

### Task 01 — Test server with multiple clients using backlog=3

- **Server**: `Task 01 [iterated_server].py` (backlog=3, threading for multiple clients)
- **Client**: `Task 01 [simple_client].py` (auto-determined client numbering)
- **Test Script**: `Task 01 [test_multiple_clients].py` (automated testing with 5 clients)
- **Description**: Tests server with backlog=3 using threading to handle multiple concurrent clients

**Key Features**:
- Server uses `socket.listen(3)` for backlog limit
- Threading handles multiple clients concurrently
- Clients automatically determine their number from server welcome message
- Test script runs 5 clients with staggered connections

Usage:

```bash
# Terminal 1 - Start server
python3 "Lab 05/Task 01 [iterated_server].py" --port 5000

# Terminal 2 - Run single client
python3 "Lab 05/Task 01 [simple_client].py" --port 5000

# Terminal 3 - Run automated test with 5 clients
python3 "Lab 05/Task 01 [test_multiple_clients].py"
```

Expected interaction (example):

```text
Server started on localhost:5000
Backlog set to 3 - waiting for connections...

New connection from ('127.0.0.1', 54321)
Thread started for Client 1 from ('127.0.0.1', 54321)
Sent to Client 1: Connected to Client 1
```

**Screenshot**: `Lab 05/Screenshots/Task 01.png`

---

### Task 02 — Enhanced server with continuous conversation

- **Server**: `Task 02 [enhanced_server].py` (echo functionality with connection established message)
- **Client**: `Task 02 [enhanced_client].py` (prompts for IP/port, continuous conversation)
- **Description**: Server sends connection established message immediately and echoes all client messages with "(Echoed)" suffix

**Key Features**:
- Server sends `[Server]Connection Established.` immediately after connection
- Echoes messages with `[Server] message (Echoed)` format
- Handles "disconnect" message with `[Server]Connection terminated.`
- Shows `Listening on 127.0.0.1:8000` after disconnect

Usage:

```bash
# Terminal 1 - Start enhanced server
python3 "Lab 05/Task 02 [enhanced_server].py" --port 8000

# Terminal 2 - Run enhanced client
python3 "Lab 05/Task 02 [enhanced_client].py"
# Enter: 127.0.0.1 and 8000 when prompted
```

Expected interaction (example):

```text
Enter server IP Address: 127.0.0.1
Enter server port: 8000
[Server]Connection Established.
[Client] Hello.
[Server] Hello (Echoed)
[Client] Testing server echo.
[Server] Testing server echo (Echoed)
[Client] disconnect
[Server]Connection terminated.
```

**Screenshots**:

![Task 02 Server](../Lab%2005/Screenshots/Task%2002-00.png)

![Task 02 Client](../Lab%2005/Screenshots/Task%2002-01.png)

---

### Task 03 — Authentication server with registration and login

- **Server**: `Task 03 [auth_server].py` (user registration, login, credential storage)
- **Client**: `Task 03 [auth_client].py` (interactive registration and login flow)
- **Description**: Implements complete authentication system with user registration, login validation, and credential persistence

**Key Features**:
- User registration with username/password confirmation
- Login system with retry logic for incorrect credentials
- Credential storage in JSON file with dictionary backup
- Proper error handling and validation
- Exact console output format matching requirements

**Registration Flow**:
- Server prompts: `[Server] Welcome! Would you like to (1) Register or (2) Login?`
- Client responds: `[Client] 1`
- Server prompts for username and password with confirmation
- Server confirms: `[Server] User 'username' registered successfully!`

**Login Flow**:
- Server prompts: `[Server] Welcome! Would you like to (1) Register or (2) Login?`
- Client responds: `[Client] 2`
- Username validation with "user unknown. Try again" error
- Password validation with "Password incorrect. Try again" error
- Success message: `[Server] Welcome username!`

Usage:

```bash
# Terminal 1 - Start authentication server
python3 "Lab 05/Task 03 [auth_server].py" --port 8000

# Terminal 2 - Run client for registration
python3 "Lab 05/Task 03 [auth_client].py"
# Enter: 127.0.0.1 and 8000, then choose 1 for registration

# Terminal 3 - Run client for login
python3 "Lab 05/Task 03 [auth_client].py"
# Enter: 127.0.0.1 and 8000, then choose 2 for login
```

Expected interaction (registration example):

```text
[Server] Welcome! Would you like to (1) Register or (2) Login?
[Client] 1
[Server] Username:
[Client] jarullah
[Server] password
[Client] 12345678
[Server] Retype password
[Client] 12345678
[Server] User 'jarullah' registered successfully!
```

Expected interaction (login example):

```text
[Server] Welcome! Would you like to (1) Register or (2) Login?
[Client] 2
[Server] Username:
[Client] jarullah
[Server] Password
[Client] 12345678
[Server] Welcome jarullah!
```

**Screenshots**:

![Task 03 Registration](../Lab%2005/Screenshots/Task%2003-00.png)

![Task 03 Login](../Lab%2005/Screenshots/Task%2003-01.png)

---

## Results

- Successfully implemented iterated TCP server with backlog=3 and threading
- Demonstrated multi-client handling with proper connection management
- Built enhanced server with continuous conversation and echo functionality
- Implemented complete authentication system with registration and login
- All tasks follow exact console output format from requirements
- Credentials persist between server restarts via JSON file storage

---

## Discussion

- **Threading**: Each client connection runs in a separate thread, allowing concurrent handling
- **Backlog Management**: `socket.listen(3)` limits queued connections, demonstrating TCP backlog behavior
- **Authentication**: JSON file storage provides persistence while dictionary provides fast lookup
- **Error Handling**: Comprehensive validation and retry logic for robust user experience
- **Message Formatting**: Consistent `[Server]` and `[Client]` prefixes for clear communication

---

## Conclusion

- Completed all three tasks with proper threading, authentication, and communication patterns
- Demonstrated understanding of iterated server patterns and multi-client handling
- Implemented robust authentication system with persistent credential storage
- All code follows proper error handling and type safety practices
- Ready for advanced networking concepts and real-world server applications

---

## Appendix

### Task 01 Commands:
```bash
# Start server
python3 "Lab 05/Task 01 [iterated_server].py" --port 5000

# Run single client
python3 "Lab 05/Task 01 [simple_client].py" --port 5000

# Run automated test
python3 "Lab 05/Task 01 [test_multiple_clients].py"
```

### Task 02 Commands:
```bash
# Start enhanced server
python3 "Lab 05/Task 02 [enhanced_server].py" --port 8000

# Run enhanced client
python3 "Lab 05/Task 02 [enhanced_client].py"
```

### Task 03 Commands:
```bash
# Start authentication server
python3 "Lab 05/Task 03 [auth_server].py" --port 8000

# Run authentication client
python3 "Lab 05/Task 03 [auth_client].py"
```

### Files Created:
- `user_credentials.json` - Persistent credential storage
- All screenshots saved in `Lab 05/Screenshots/`
- Complete source code with proper documentation and error handling
