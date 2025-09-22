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
Example output (may vary by OS):

```text
Port  TCP Service  UDP Service
20    ftp-data     ftp-data
21    ftp          ftp
22    ssh          ssh
23    telnet       telnet
25    smtp         smtp
53    domain       domain
67    bootps       bootps
80    http         http
110   pop3         pop3
443   https        https
```

**Screenshot**: `Lab 04/Screenshots/Task 01.png`

---

### Task 02 — TBD

Add description, outputs, and screenshots when implemented.

---

### Task 03 — TBD

Add description, outputs, and screenshots when implemented.

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
