# 💬 Two-Way Chat System Instructions

## For the HOST (Person starting the chat):

1. **Run the setup script:**

   ```bash
   python3 start_chat.py
   ```

2. **Choose option 1** (Start Server)

3. **Enter port 8000** (or just press Enter)

4. **Wait for your friend to connect**

5. **Start typing messages!**

---

## For the FRIEND (Person joining the chat):

1. **Download these files:**

   - `chat_client.py`
   - `start_chat.py`

2. **Run the setup script:**

   ```bash
   python3 start_chat.py
   ```

3. **Choose option 2** (Start Client)

4. **Enter the host's IP address** (e.g., 10.1.30.113)

5. **Enter port 8000**

6. **Enter your nickname**

7. **Start chatting!**

---

## Features:

- ✅ Real-time messaging
- ✅ Multiple people can join
- ✅ Nicknames for each person
- ✅ Type `/quit` to exit
- ✅ Shows when people join/leave

## Example Usage:

```
💬 Two-Way Chat System
==============================
1. Start Server (Host)
2. Start Client (Join)
3. Exit

Choose option (1-3): 1
Enter server port (default 8000): 8000
🚀 Chat server started on 0.0.0.0:8000
📡 Waiting for connections...
✅ New connection from 192.168.1.100:54321
📝 Ali joined the chat!
💬 Ali: Hello everyone!
💬 Ali: How are you doing?
```

## Troubleshooting:

- Make sure both people are on the same network
- Check firewall settings
- Try different ports if 8000 doesn't work
- Make sure the host starts the server first
