# Computer Networks Lab (COMP-352L)

Hands-on labs for Computer Networks covering packet analysis, sockets, and iterative server patterns. Includes code, lab manuals, and reports with evidence.

## Repository Structure

- `Lab Manuals/` — PDF lab manuals for each lab
- `Lab 03/` — HTTP analysis in Wireshark (PCAPs + screenshots)
- `Lab 04/` — Socket programming tasks (Python)
- `Lab 05/` — Iterated TCP server/client exercises (Python)
- `Lab Reports/` — Markdown lab reports

## Prerequisites

- Python 3.10+
- Git installed

## Getting Started

```bash
git clone https://github.com/AliHamz10/Computer-Networks-Lab-COMP-352L.git
cd Computer-Networks-Lab-COMP-352L
```

## Lab 03 — HTTP Analysis (Wireshark)

- Open PCAPs in `Lab 03/` with Wireshark.
- See findings and references in `Lab Reports/Lab Report 03.md`.

## Lab 04 — Socket Programming (Python)

Tasks implemented under `Lab 04/`:

1. Task 01 — Service names for 10 ports

   - Script: `Task 01 [services_names).py`
   - Prints TCP/UDP service names via `socket.getservbyport`.

2. Task 02 — Resolve IP addresses of domains

   - Script: `Task 02 [resolve_domains).py`
   - Resolves A records via `socket.gethostbyname`.

3. Task 03 — Echo: user-provided message

   - Server: `Task 03 [echo_server_helper).py`
   - Client: `Task 03 [echo_client_user_message).py`
   - Start server, then run client and type your message.

4. Task 04 — Server displays host address info

   - Server: `Task 03 [echo_server_helper).py` (prints hostname, FQDN, IPs)
   - Shows bound host:port on startup.

5. Task 05 — Greet if user's name is present
   - Server: `Task 05 [greet_server).py` (`--user <Name>`)
   - Client: `Task 05 [greet_client).py`
   - If the message contains the name (case-insensitive), replies `Hello, <Name>!`; otherwise `Unknown user`.

Quick commands (Lab 04):

```bash
# Task 01
python3 "Lab 04/Task 01 [services_names).py"

# Task 02
python3 "Lab 04/Task 02 [resolve_domains).py"

# Task 03
python3 "Lab 04/Task 03 [echo_server_helper).py" --port 5000
python3 "Lab 04/Task 03 [echo_client_user_message).py"

# Task 05
python3 "Lab 04/Task 05 [greet_server).py" --user Ali --port 5051
python3 "Lab 04/Task 05 [greet_client).py" --port 5051 "Hi I'm Ali"
```

## Lab 05 — Iterated TCP Server/Client

- See `Lab 05/` for iterated server patterns and simple clients.
- Details and results will be documented in the corresponding lab report.

## Reports

- Lab 03: `Lab Reports/Lab Report 03.md`
- Lab 04: `Lab Reports/Lab Report 04.md`

## Conventions

- Keep file/directory names intact (spaces and brackets are intentional).
- Use relative links in Markdown for portability.
- Prefer small, descriptive commits per task; open a PR for full lab completion.
