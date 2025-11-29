# 🚀 Bit Stuffing Client–Server Simulation (Python + Tkinter + Sockets)

A complete **bit stuffing and unstuffing simulation** using **Python**, featuring:  
✔ GUI-based client (Tkinter)  
✔ TCP socket communication  
✔ Frame creation and decoding  
✔ Flag-based bit stuffing and de-stuffing  
✔ ASCII-safe binary encoding and recovery  

---

## 📌 Overview

This project implements a full demonstration of **Bit Stuffing**, commonly used in data link layer protocols like HDLC. It uses a **Tkinter GUI client** and a **TCP server** to simulate:

- Text → Binary conversion  
- Bit stuffing  
- Frame creation using the flag `01111110`  
- Transmission over sockets  
- Server-side frame validation  
- Bit unstuffing  
- Binary-to-text recovery  
- ACK response to client  

---

## 🖥 Client (Tkinter GUI)

The client performs:

- Conversion of user text to binary  
- Bit stuffing after every five consecutive `1`s  
- Frame encapsulation  
- Transmission to server  
- Display of:
  - Raw binary  
  - Stuffed data  
  - Final frame  
  - Transmission status  
  - Server acknowledgment  

---

## 🗄 Server (TCP Socket)

The server:

- Accepts incoming frames  
- Validates start and end flags  
- Extracts stuffed data  
- Performs bit unstuffing  
- Recovers original text (ASCII)  
- Returns ACK messages  

---

## 🔧 Technologies Used

- Python 3  
- Tkinter (GUI)  
- TCP Socket Programming  
- Bit Stuffing / Unstuffing  
- ASCII Encoding  

---

## 📂 Project Structure

```
client_gui.py     # Tkinter GUI client
server.py         # TCP server
README.md
```

---

## 📘 How It Works

### 1. Text → Binary  
- Characters encoded as **8-bit ASCII**  
- '0' and '1' preserved as raw bits  

### 2. Bit Stuffing  
Insert a `0` after every **five consecutive 1s**.

### 3. Framing  
Final frame format:

```
01111110 + stuffed_data + 01111110
```

### 4. Transmission  
Client sends frame to server via TCP at:

```
HOST = 127.0.0.1
PORT = 666
```

### 5. Server Processing  
- Validates flags  
- Unstuffs data  
- Converts binary → text  
- Sends ACK  

---

## ▶️ How to Run

### Start Server
```
python server.py
```

### Start Client
```
python client_gui.py
```

Ensure FLAG, HOST, and PORT match in both files.

---

## 🛡 Features

| Feature | Status |
|--------|--------|
| Binary Conversion | ✔️ |
| Bit Stuffing | ✔️ |
| Bit Unstuffing | ✔️ |
| Framing | ✔️ |
| Flag Detection | ✔️ |
| GUI Interface | ✔️ |
| TCP Communication | ✔️ |
| ACK Handling | ✔️ |

---

## 📧 Author

Suitable for students and developers learning:  
- Data Link Layer  
- HDLC framing  
- Socket programming  
- Bit stuffing mechanisms  

---
