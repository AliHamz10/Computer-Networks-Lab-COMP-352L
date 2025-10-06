# Lab Report 06 — Multithreaded Server with Authentication

- **Course**: Computer Networks Lab (COMP-352L)
- **Semester**: Fall 2025
- **Lab**: 06
- **Students**:
  - **Name**: Ali Hamza, **Reg No.**: B23F0063AI106
  - **Name**: Zarmeena Jawad, **Reg No.**: B23F0115AI125
- **Instructor**: Mr. Jarullah
- **Date Performed**: 2025-10-06
- **Date Submitted**: 2025-10-06

---

## Objectives

- **Understand**: Multithreaded server architecture with concurrent client handling
- **Practice**: Building authentication systems with registration and login functionality
- **Implement**: Multiple client support with simultaneous registration and conversation
- **Test**: Concurrent client interactions and server performance under load
- **Document**: Evidence with outputs and screenshots for each task

---

## Materials and Setup

- **Software**: Python 3.11+, macOS Terminal
- **Files Used**: from `Lab 06/`
  - `Task 01 [multithreaded_auth_server].py`
  - `Task 01 [auth_client].py`
  - `Task 01 [test_multiple_clients].py`
  - `Task 01 [simple_test].py`
- **References**: `socket`, `threading`, `json` modules

---

## Methodology

1. Implement multithreaded server with authentication capabilities
2. Create client applications for registration, login, and chat functionality
3. Build automated test program for concurrent client simulation
4. Test server with multiple simultaneous clients (half register, half login/converse)
5. Capture console output and screenshots for each test scenario
6. Save screenshots under `Lab 06/Screenshots/`
7. Document results and evidence per task

---

## Tasks Summary and Evidence

### Task 01 — Multithreaded Server with Registration and Login

- **Server**: `Task 01 [multithreaded_auth_server].py` (multithreaded authentication server)
- **Client**: `Task 01 [auth_client].py` (interactive client for registration/login/chat)
- **Test Program**: `Task 01 [test_multiple_clients].py` (automated concurrent testing)
- **Simple Test**: `Task 01 [simple_test].py` (basic socket communication test)
- **Description**: Implements multithreaded server supporting multiple concurrent clients for registration, login, and conversation

**Key Features**:

- **Multithreading**: Each client connection runs in a separate thread for concurrent handling
- **Authentication System**: User registration and login with persistent credential storage
- **Chat Functionality**: Logged-in users can send messages and have conversations
- **Concurrent Support**: Multiple clients can register and login simultaneously
- **Persistent Storage**: User credentials saved to JSON file for persistence
- **Error Handling**: Comprehensive validation and graceful error management

**Server Capabilities**:

- Accepts multiple concurrent connections using threading
- Handles user registration with username/password validation
- Manages user login with credential verification
- Supports chat messaging for authenticated users
- Tracks logged-in users and prevents duplicate sessions
- Provides proper logout functionality

**Client Capabilities**:

- Interactive menu for registration, login, and chat
- Automatic connection handling with server welcome message
- Chat interface for authenticated users
- Proper error handling and user feedback

**Test Program Features**:

- Automated testing with configurable number of clients
- Half clients perform registration, half perform login/conversation
- Concurrent execution with threading
- Performance metrics and success rate reporting
- Detailed error reporting for failed operations

Usage:

```bash
# Terminal 1 - Start server
python3 "Task 01 [multithreaded_auth_server].py" --port 8000

# Terminal 2 - Interactive client
python3 "Task 01 [auth_client].py" --port 8000

# Terminal 3 - Simple socket test
python3 "Task 01 [simple_test].py"

# Terminal 4 - Multiple client test
python3 "Task 01 [test_multiple_clients].py" --clients 10
```

Expected server output:

```text
=== Multithreaded Auth Server Started ===
Host: 127.0.0.1
Port: 8000
Time: 2025-10-06 10:25:27
Waiting for connections...
Press Ctrl+C to stop the server
========================================

[CONNECTION] New client from ('127.0.0.1', 54321)
[CLIENT-1] Thread started from ('127.0.0.1', 54321)
[CLIENT-1] Received: 1:newuser:password123
[CLIENT-1] User 'newuser' registered successfully
[CLIENT-1] Sent: [Server] User 'newuser' registered successfully!
```

Expected client interaction:

```text
[Client] Connected to 127.0.0.1:8000
[Client] Server welcome: [Server] Welcome! Choose an option:
1. Register
2. Login
3. Exit

=== Authentication Client ===
1. Register
2. Login
3. Exit
Choose option (1-3): 1
Username: newuser
Password: password123
[Client] Registration response: [Server] User 'newuser' registered successfully!
```

**Screenshots**:

![Task 01 Server Startup](../Lab%2006/Screenshots/Task%2001-00.png)

![Task 01 Client Registration](../Lab%2006/Screenshots/Task%2001-01.png)

![Task 01 Client Login and Chat](../Lab%2006/Screenshots/Task%2001-02.png)

![Task 01 Simple Socket Test](../Lab%2006/Screenshots/Task%2001-03.png)

![Task 01 Multiple Client Test](../Lab%2006/Screenshots/Task%2001-04.png)

---

## Results

- Successfully implemented multithreaded server with authentication capabilities
- Demonstrated concurrent client handling with proper threading architecture
- Built comprehensive authentication system with registration and login
- Implemented chat functionality for authenticated users
- Created automated test program for concurrent client simulation
- Achieved 100% success rate for registration operations
- Demonstrated proper error handling and user feedback
- All screenshots captured showing complete functionality

---

## Discussion

- **Threading Architecture**: Each client connection runs in a separate thread, enabling true concurrent processing
- **Authentication Flow**: Proper separation of registration and login with credential validation
- **Concurrent Access**: Multiple clients can register and login simultaneously without conflicts
- **Persistent Storage**: JSON file storage ensures user data persists between server restarts
- **Error Handling**: Comprehensive validation prevents invalid operations and provides clear feedback
- **Performance**: Server handles multiple concurrent connections efficiently with minimal overhead
- **User Experience**: Clear prompts and responses make the system intuitive to use

---

## Conclusion

- Completed Task 01 with full multithreaded server implementation
- Demonstrated understanding of concurrent programming and authentication systems
- Successfully implemented multiple client support with proper resource management
- Built robust error handling and user feedback mechanisms
- Created comprehensive test suite for validation and performance measurement
- All code follows professional standards with proper documentation and type safety
- Ready for advanced networking concepts and production server applications

---

## Appendix

### Task 01 Commands:

```bash
# Start multithreaded server
python3 "Task 01 [multithreaded_auth_server].py" --port 8000

# Run interactive client
python3 "Task 01 [auth_client].py" --port 8000

# Run simple socket test
python3 "Task 01 [simple_test].py"

# Run multiple client test
python3 "Task 01 [test_multiple_clients].py" --clients 10
```

### Files Created:

- `Task 01 [multithreaded_auth_server].py` - Main multithreaded server
- `Task 01 [auth_client].py` - Interactive authentication client
- `Task 01 [test_multiple_clients].py` - Automated concurrent test program
- `Task 01 [simple_test].py` - Simple socket communication test
- `user_credentials.json` - Persistent user credential storage
- All screenshots saved in `Lab 06/Screenshots/`

### Key Features Implemented:

- Multithreaded server architecture
- User registration and login system
- Chat functionality for authenticated users
- Concurrent client handling
- Persistent credential storage
- Comprehensive error handling
- Automated testing framework
