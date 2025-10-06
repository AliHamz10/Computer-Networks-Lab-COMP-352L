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

## Tasks Summary and Evidence (Continued)

### Task 02 — Server Clean Shutdown

- **Server**: `Task 02 [multithreaded_auth_server_with_shutdown].py` (enhanced server with shutdown capability)
- **Test Program**: `Task 02 [test_shutdown].py` (automated shutdown testing)
- **Description**: Adds the ability to terminate the server cleanly with proper thread management

**Key Features Added**:

- **Exit Command**: Type `exit` in server console to initiate graceful shutdown
- **Thread Management**: All active client threads are tracked and properly joined before exit
- **Graceful Shutdown**: Server waits for all client threads to complete (5-second timeout per thread)
- **Clean Resource Management**: Proper socket closure and thread cleanup
- **Shutdown Monitoring**: Background thread monitors console input for exit command

**Shutdown Process**:

1. User types `exit` in server console
2. Server sets shutdown flag and stops accepting new connections
3. Main socket is closed to prevent new connections
4. Server waits for all active client threads to complete
5. Each thread is given up to 5 seconds to finish gracefully
6. Server reports completion of thread joining process
7. Clean termination with proper resource cleanup

**Thread Management**:

- Active threads are tracked in `self.active_threads` list
- Each client thread removes itself from the list when completed
- Shutdown process waits for all threads with `thread.join(timeout=5.0)`
- Timeout prevents indefinite waiting for unresponsive threads
- Proper cleanup ensures no zombie threads remain

Usage:

```bash
# Terminal 1 - Start server with shutdown capability
python3 "Task 02 [multithreaded_auth_server_with_shutdown].py" --port 8000

# Terminal 2 - Connect client and interact
python3 "Task 01 [auth_client].py" --port 8000

# Terminal 1 - Type 'exit' to shutdown
exit
```

Expected shutdown output:

```text
=== Multithreaded Auth Server Started ===
Host: 127.0.0.1
Port: 8000
Time: 2025-10-06 10:30:00
Waiting for connections...
Type 'exit' and press Enter to shutdown the server
========================================

[CONNECTION] New client from ('127.0.0.1', 54321)
[CLIENT-1] Thread started from ('127.0.0.1', 54321)
[CLIENT-1] User 'testuser' registered successfully
[CLIENT-1] User 'testuser' logged in successfully
[CLIENT-1] testuser says: Hello server!
[CLIENT-1] User 'testuser' logged out
[CLIENT-1] Connection closed

exit

[SHUTDOWN] Exit command received...
[SHUTDOWN] Initiating graceful server shutdown...
[SHUTDOWN] Main socket closed
[SHUTDOWN] Waiting for 0 active threads to complete...
[SHUTDOWN] All threads have been processed
[SHUTDOWN] Server shutdown complete
```

**Screenshot**:

![Task 02 Server Shutdown](../Lab%2006/Screenshots/Task%2002.png)

---

### Task 03 — Client Tracking and Management

- **Server**: `Task 03 [multithreaded_auth_server_with_client_tracking].py` (enhanced server with client tracking)
- **Test Program**: `Task 03 [test_client_tracking].py` (automated client tracking testing)
- **Description**: Adds client tracking capabilities with dictionary management and server commands

**Key Features Added**:

- **Client Dictionary**: Maintains `{client_id: socket}` mapping for all connected clients
- **Client Information Tracking**: Stores username, address, connection time, and login status
- **Active Client Display**: Shows count of active and logged-in clients every 30 seconds
- **List Command**: Server-side `list` command to display all connected clients in table format
- **Count Command**: Server-side `count` command for immediate client count display
- **Real-time Updates**: Client tracking updates automatically on connect/disconnect/login/logout

**Client Tracking System**:

- **Dictionary Structure**: `self.connected_clients = {client_id: socket}`
- **Client Info**: `self.client_info = {client_id: {username, address, connected_time, logged_in}}`
- **Thread Safety**: All client tracking operations protected with locks
- **Automatic Cleanup**: Clients removed from tracking on disconnect
- **Status Updates**: Login/logout status tracked in real-time

**Server Commands**:

- **`list`**: Displays detailed table of all connected clients
- **`count`**: Shows immediate count of active and logged-in clients
- **`exit`**: Graceful server shutdown with thread management

**Client Information Display**:

The `list` command shows:
- Client ID
- Username (or "Not logged in")
- Address (IP:Port)
- Status (Connected/Logged in)
- Connected time

Usage:

```bash
# Terminal 1 - Start server with client tracking
python3 "Task 03 [multithreaded_auth_server_with_client_tracking].py" --port 8000

# Terminal 2, 3, 4 - Connect multiple clients
python3 "Task 01 [auth_client].py" --port 8000

# Terminal 1 - Use server commands
list
count
exit
```

Expected server output:

```text
=== Multithreaded Auth Server with Client Tracking ===
Host: 127.0.0.1
Port: 8000
Time: 2025-10-06 10:45:00
Waiting for connections...
Commands: 'exit' to shutdown, 'list' to show connected clients
============================================================

[CONNECTION] New client from ('127.0.0.1', 54321)
[CLIENT-1] Added to client tracking
[CLIENT-COUNT] Active clients: 1 | Logged in: 0

[CONNECTION] New client from ('127.0.0.1', 54322)
[CLIENT-2] Added to client tracking
[CLIENT-COUNT] Active clients: 2 | Logged in: 0

[CLIENT-1] User 'user1' logged in successfully
[CLIENT-COUNT] Active clients: 2 | Logged in: 1

list

[CLIENT-LIST] Connected clients (2):
--------------------------------------------------------------------------------
ID     Username         Address             Status       Connected           
--------------------------------------------------------------------------------
1      user1            127.0.0.1:54321    Logged in    10:45:15            
2      Not logged in    127.0.0.1:54322    Connected    10:45:20            
--------------------------------------------------------------------------------
```

**Screenshots**:

![Task 03 Server with Client Tracking](../Lab%2006/Screenshots/Task%2003%20-%2000.png)

![Task 03 List Command Output](../Lab%2006/Screenshots/Task%2003%20-%2001.png)

---

### Task 04 — Group Chat with Broadcast Messages

- **Server**: `Task 04 [multithreaded_auth_server_with_group_chat].py` (enhanced server with group chat)
- **Client**: `Task 04 [group_chat_client].py` (interactive group chat client)
- **Test Program**: `Task 04 [test_group_chat].py` (automated group chat testing)
- **Description**: Implements group chat functionality with broadcast messages and sender ID tracking

**Key Features Added**:

- **Broadcast Command**: `broadcast:message` sends messages to all clients in chat room
- **Sender ID Tracking**: All messages include sender ID in format `[Group Chat] Username (ID:X): message`
- **Group Chat Room**: Clients must join chat room to participate in group communication
- **Real-time Broadcasting**: Messages instantly sent to all connected clients
- **Chat Room Management**: Track and display chat room members with `chatroom` command
- **Dual Messaging**: Support for both broadcast (group) and private messages

**Group Chat System**:

- **Chat Room**: `self.chat_room = []` - List of client IDs in chat room
- **Broadcast Function**: `broadcast_message()` sends to all clients in chat room
- **Sender ID Format**: `[Group Chat] {username} (ID:{client_id}): {message}`
- **Join Chat**: Clients must explicitly join chat room using option 3
- **Real-time Updates**: Chat room membership tracked in real-time

**Message Types**:

- **Broadcast Messages**: `broadcast:message` - Sent to all clients in chat room
- **Private Messages**: `chat:message` - Private server response
- **Join Chat**: `3` - Join the group chat room
- **Logout**: `logout` - Leave chat room and logout

**Server Commands**:

- **`chatroom`**: Shows current chat room members
- **`list`**: Displays all connected clients
- **`count`**: Shows client counts including chat room members
- **`exit`**: Graceful server shutdown

Usage:

```bash
# Terminal 1 - Start server with group chat
python3 "Task 04 [multithreaded_auth_server_with_group_chat].py" --port 8000

# Terminal 2, 3, 4 - Connect group chat clients
python3 "Task 04 [group_chat_client].py" --port 8000

# Terminal 1 - Use server commands
chatroom
list
exit
```

Expected server output:

```text
=== Multithreaded Auth Server with Group Chat ===
Host: 127.0.0.1
Port: 8000
Time: 2025-10-06 11:00:00
Waiting for connections...
Commands: 'exit' to shutdown, 'list' to show connected clients, 'chatroom' to show chat members
======================================================================

[CONNECTION] New client from ('127.0.0.1', 54321)
[CLIENT-1] Added to client tracking
[CLIENT-COUNT] Active: 1 | Logged in: 0 | In chat: 0

[CLIENT-1] User 'alice' logged in successfully
[CLIENT-1] alice joined chat room
[CLIENT-COUNT] Active: 1 | Logged in: 1 | In chat: 1

[BROADCAST] Sent to Client 1: Hello everyone!
[Group Chat] alice (ID:1): Hello everyone!

[CONNECTION] New client from ('127.0.0.1', 54322)
[CLIENT-2] Added to client tracking
[CLIENT-2] User 'bob' logged in successfully
[CLIENT-2] bob joined chat room
[CLIENT-COUNT] Active: 2 | Logged in: 2 | In chat: 2

[BROADCAST] Sent to Client 1: Hi alice!
[BROADCAST] Sent to Client 2: Hi alice!
[Group Chat] bob (ID:2): Hi alice!

chatroom

[CHAT-ROOM] Chat room members (2):
--------------------------------------------------
Client 1: alice
Client 2: bob
--------------------------------------------------
```

**Screenshots**:

![Task 04 Group Chat Server](../Lab%2006/Screenshots/Task%2004%20-%2000.png)

![Task 04 Group Chat Interaction](../Lab%2006/Screenshots/Task%2004%20-01.png)

---

## Conclusion

- Completed Task 01 with full multithreaded server implementation
- Completed Task 02 with clean server shutdown and thread management
- Completed Task 03 with comprehensive client tracking and management system
- Completed Task 04 with group chat functionality and broadcast messaging
- Demonstrated understanding of concurrent programming and authentication systems
- Successfully implemented multiple client support with proper resource management
- Built robust error handling and user feedback mechanisms
- Implemented graceful server termination with proper thread joining
- Created comprehensive client tracking with dictionary management and server commands
- Built real-time client monitoring with detailed information display
- Implemented group chat with broadcast messaging and sender ID tracking
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
- `Task 02 [multithreaded_auth_server_with_shutdown].py` - Enhanced server with shutdown capability
- `Task 02 [test_shutdown].py` - Automated shutdown testing program
- `Task 03 [multithreaded_auth_server_with_client_tracking].py` - Server with client tracking
- `Task 03 [test_client_tracking].py` - Automated client tracking test program
- `Task 04 [multithreaded_auth_server_with_group_chat].py` - Server with group chat functionality
- `Task 04 [group_chat_client].py` - Interactive group chat client
- `Task 04 [test_group_chat].py` - Automated group chat test program
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
- Clean server shutdown with thread management
- Graceful termination with proper resource cleanup
- Client tracking with dictionary management
- Real-time client monitoring and display
- Server-side commands for client management
- Group chat with broadcast messaging
- Sender ID tracking in all messages
- Chat room management and membership tracking
