## Lab Report 03 — HTTP Analysis with Wireshark

- **Course**: Computer Networks Lab (COMP-352L)
- **Semester**: Fall 2025
- **Lab**: 03
- **Students**:
  - **Name**: Ali Hamza, **Reg No.**: B23F0063AI106
  - **Name**: Zarmeena Jawad, **Reg No.**: B23F0115AI125
- **Instructor**: Mr. Jarullah
- **Date Performed**: 2025-09-22
- **Date Submitted**: 2025-09-25

---

### Objectives

- **Understand**: Inspect HTTP request and response exchanges using Wireshark
- **Analyze**: Identify status codes, headers, payloads, and caching behavior
- **Correlate**: Map TCP segments to HTTP messages and object retrievals

---

### Materials and Setup

- **Software**: Wireshark (latest stable)
- **PCAP Files Used**: from `Lab 03/`
  - `cached-page.pcapng`
  - `extract-object.pcapng`
  - `http-404.pcapng`
  - `http-500error.pcapng`
  - `http-cached-wikipedia.pcapng`
  - `http-espn2007.pcapng`
  - `http-espn2011.pcapng`
  - `http-espn2012.pcapng`
  - `http-facebook.pcapng`
  - `http-fault-post.pcapng`
  - `http-winpcap.pcapng`
  - `sec-nessus.pcapng`

---

### Methodology

1. Open each `.pcapng` in Wireshark
2. Use filters:
   - `http`
   - `http.request` and `http.response`
   - `tcp.stream eq N` to isolate transactions
3. Follow streams: Right click → Follow → HTTP/TCP Stream
4. Inspect key headers: `Host`, `User-Agent`, `Content-Type`, `Content-Length`, `Cache-Control`, `ETag`, `If-Modified-Since`, `If-None-Match`
5. Record findings and screenshots per question

---

### Questions and Answers

#### Q1. You are analyzing an HTTP session as a user browses a new website. What HTTP response code indicates the page was found locally?

- **Answer**: The HTTP response code 304 Not Modified indicates the page was served from the local cache instead of being downloaded again from the server.
- **Evidence**: As shown in the screenshot below, multiple packets contain the response line HTTP/1.1 304 Not Modified. The details pane also shows caching headers such as ETag and Last-Modified, confirming cached content validation.
- **Screenshot**:
  ![Q1 Screenshot](../Lab%2003/Screenshots/Question%2301.png)

---

#### Q2. How is an HTTP 404 Not Found categorized?

- **Answer**: The HTTP `404 Not Found` response is categorized as a **Client Error** status code (part of the 4xx class). It indicates that the client was able to communicate with the server, but the server could not find the requested resource.
- **Evidence**: The screenshot shows `HTTP/1.1 404 Not Found` along with headers like `Content-Type: text/html` and the full request URI `http://www.people.com.cn/hello`, which confirms the missing resource.
- **Screenshot**:  
  ![Q2 Screenshot](../Lab%2003/Screenshots/Question%2302.png)

---

#### Q3. How can you determine that a client is loading web pages out of cache?

- **Answer**: Identify `304 Not Modified` responses and validation headers such as `ETag` with `If-None-Match`, or `Last-Modified` with `If-Modified-Since`. These indicate the server validated the cached copy rather than sending the full object.
- **Evidence**: In `cached-page.pcapng`, the response line `HTTP/1.1 304 Not Modified` appears alongside headers like `ETag` and `Last-Modified`, confirming cache usage.
- **Screenshot**:  
  ![Q3 Screenshot](../Lab%2003/Screenshots/Question%2303.png)

---

#### Q4. What display filter should you avoid if you want to view the TCP handshake and TCP ACKs during a web browsing session?

- **Answer**: Avoid `http` filter, since it hides TCP handshake and ACK packets. Use `tcp` instead
- **Evidence**: `http` filter omits SYN, SYN-ACK, ACK packets
- **Screenshot**:  
  ![Q4 Screenshot](../Lab%2003/Screenshots/Question%2304.png)

---

#### Q5. What is the HTTP request method used to send data up to an HTTP server?

- **Answer**: The `POST` method is used to send data to the server
- **Evidence**: Seen in `http-fault-post.pcapng`

---

#### Q6. What is the syntax for capture and display filters for HTTP traffic running over port 80?

- **Answer**:
  - **Capture filter**: `tcp port 80`
  - **Display filter**: `http`
- **Evidence**: Used in Wireshark for restricting to HTTP traffic

---

### Results

- **Status Codes Observed**: 200, 304, 404, 500
- **Notable Headers**: `ETag`, `Last-Modified`, `Cache-Control`, `Expires`, `Content-Type`, `Content-Length`
- **Caching Behavior**: Verified through `304 Not Modified` and validation headers
- **Object Extraction**: Objects successfully extracted from `extract-object.pcapng`

---

### Discussion

- HTTP status codes reveal client and server communication states
- Caching improves efficiency, confirmed with `304 Not Modified` responses
- TCP handshakes are essential for reliable HTTP communication
- Filters in Wireshark must be chosen carefully to capture the desired layers

---

### Conclusion

- Learned to analyze HTTP sessions using Wireshark
- Observed and categorized different HTTP status codes
- Identified caching through headers and `304` responses
- Practiced applying capture and display filters

**Key Takeaways**:

- `200 OK` = successful retrieval
- `304 Not Modified` = served from cache
- `404 Not Found` = client error
- `POST` = sends data to server
- Capture filter: `tcp port 80`, Display filter: `http`

---

### References

- Wireshark User’s Guide
- RFC 7230–7235 (HTTP/1.1 Semantics and Headers)
- Course materials and `Lab 03.pdf`

---

### Appendix

- **Useful Filters**:
  - `http && tcp.stream eq 3`
  - `http.response.code == 304`
  - `frame contains "ETag"`
