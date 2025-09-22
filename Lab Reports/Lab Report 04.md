# Lab Report 04 — Socket Programming Basics

- **Course**: Computer Networks Lab (COMP-352L)
- **Semester**: Fall 2025
- **Lab**: 04
- **Students**:
  - **Name**: Ali Hamza, **Reg No.**: B23F0063AI106
  - **Name**: Zarmeena Jawad, **Reg No.**: B23F0115AI125
- **Instructor**: Mr. Jarullah
- **Date Performed**: 2025-09-22
- **Date Submitted**: 2025-09-25

---

## Objectives

- **Understand**: Core socket APIs in Python (TCP/UDP) and the service/port mapping
- **Practice**: Writing small client/server utilities and network queries
- **Document**: Evidence with outputs and screenshots for each task

---

## Materials and Setup

- **Software**: Python 3.11+, macOS Terminal
- **Files Used**: from `Lab 04/`
  - `Task 01 [services_names).py`
- **References**: `socket` module docs

---

## Methodology

1. Implement the required script(s) in `Lab 04/`
2. Run each task, capture console output and screenshots
3. Save screenshots under `Lab 04/Screenshots/`
4. Summarize results below per task

---

## Tasks Summary and Evidence

### Task 01 — Get service names for 10 different ports

- **Script**: `Task 01 [services_names).py`
- **Description**: Uses `socket.getservbyport` to map selected ports to standard service names for both TCP and UDP

**Screenshot**: `Lab 04/Screenshots/Task 01.png`

---

### Task 02 — Find the IP address of 10 different domains

- **Script**: `Task 02 [resolve_domains).py`
- **Description**: Resolves A records for 10 popular domains using `socket.gethostbyname`

**Screenshot**: `Lab 04/Screenshots/Task 02.png`

---

### Task 3 — Modify the client so user provides the message

- **Script**: `Task 03 [echo_client_user_message).py` (interactive client)
- **Helper**: `Task 03 [echo_server_helper).py` (local echo server for testing)
- **Description**: Client prompts for host, port, and the message; sends bytes to server and prints any echoed response.

Usage:

```bash
python3 "Lab 04/Task 03 [echo_server_helper).py"   # in one terminal
python3 "Lab 04/Task 03 [echo_client_user_message).py"  # in another
# accept defaults and type message when prompted
```

Expected interaction (example):

```text
Server host (default 127.0.0.1):
Server port (default 5000):
Message to send: hello echo
Server responded: hello echo
```

**Screenshots**:

![Task 03 Echo Server](../Lab%2004/Screenshots/Task%2003%20[Echo%20Server%20Helper].png)

![Task 03 Echo Client](../Lab%2004/Screenshots/Task%2003%20[Echo%20Client%20User].png)

---

### Task 04 — Display the server machine address

- **Script**: `Task 03 [echo_server_helper).py` (updated)
- **Description**: Server prints hostname, FQDN, and resolved IP addresses on startup, along with the bound host:port.

Usage:

```bash
python3 "Lab 04/Task 03 [echo_server_helper).py" --host 127.0.0.1 --port 5000
```

Expected header (example):

```text
=== Server Host Information ===
Hostname: <your-hostname>
FQDN:     <your-fqdn>
Addresses:
  - 127.0.0.1
  - ::1
Listening on: 127.0.0.1:5000
===============================
```

**Screenshot**:

![Task 04 Server Info](../Lab%2004/Screenshots/Task%2004.png)

---

### Task 05 — Greet if user's name appears in the message

- **Server**: `Task 05 [greet_server).py` (arg `--user <Name>`, default port 5050)
- **Client**: `Task 05 [greet_client).py` (send arbitrary message)
- **Behavior**: If the message contains the username token (case-insensitive), server replies `Hello, <Name>!`; otherwise `Unknown user`.

Usage:

```bash
# Terminal 1
python3 "Lab 04/Task 05 [greet_server).py" --user Ali --port 5051

# Terminal 2
python3 "Lab 04/Task 05 [greet_client).py" --port 5051 "Hi I'm Ali"
python3 "Lab 04/Task 05 [greet_client).py" --port 5051 "Hello there"
```

Expected output:

```text
Hello, Ali!
Unknown user
```

**Screenshots**: `Lab 04/Screenshots/Task 05 - with name.png`, `Lab 04/Screenshots/Task 05 - without name.png`

---

## Results

- Verified service name resolution for 10 common ports across TCP/UDP
- Repository structured with per-task evidence

---

## Discussion

- The `services` database on the OS maps port/protocol pairs to conventional names; availability may differ by platform
- UDP entries can be "unknown" where not defined; both were handled

---

## Conclusion

- Completed Task 01 with clear, reproducible output and screenshot placeholder
- Ready to proceed with subsequent socket tasks

---

## Appendix

- Run Task 01:
  - `python3 "Lab 04/Task 01 [services_names).py"`
