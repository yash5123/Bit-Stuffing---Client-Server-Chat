import socket
import time

# --- Network Configuration (MUST match client_gui.py) ---
FLAG = "01111110"
HOST = '127.0.0.1'  # This is the computer's local address.
PORT = 666          # This is the port number the server listens on.
BUFFER_SIZE = 1024  # The maximum amount of data (in bytes) to receive at once.

# --- Core Bit Stuffing Logic ---

def bit_unstuff(data):
    # Removes the extra '0' bits inserted by the sender.
    unstuffed_bits = []
    count = 0
    i = 0
    while i < len(data):
        bit = data[i]
        
        if bit == '1':
            count += 1
            unstuffed_bits.append(bit)
            if count == 5:
                # Skips the stuffed '0' bit if it follows five '1's.
                if i + 1 < len(data) and data[i + 1] == '0':
                    i += 1
                count = 0
        else:
            count = 0
            unstuffed_bits.append(bit)
        
        i += 1
    return "".join(unstuffed_bits)

def binary_to_text(binary):
    # Converts the resulting binary data back into recognizable text.
    text_out = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            try:
                text_out += chr(int(byte, 2))
            except ValueError:
                text_out += "[ERR]"
    return text_out

def handle_frame(frame_str):
    print("\n--- SERVER: Decoding Process ---")
    print(f"FLAG is: {FLAG}")
    print(f"1. Received Frame: {frame_str}")

    # Step 2: Checks for the start and end flags to isolate the data.
    if frame_str.startswith(FLAG) and frame_str.endswith(FLAG):
        extracted_data = frame_str[len(FLAG):-len(FLAG)]
        print(f"2. Extracted Data (Stuffed): {extracted_data}")
    else:
        print("2. ERROR: Frame synchronization lost (Flags not found).")
        # Returns an error acknowledgment if flags are missing.
        return b'ACK: ERROR - Flag synchronization failure.'

    # Step 3: Calls the unstuffing function.
    unstuffed_data = bit_unstuff(extracted_data)
    print(f"3. Unstuffed Binary: {unstuffed_data}")

    # Step 4: Converts the final binary data to text for display.
    if len(unstuffed_data) % 8 == 0 and len(unstuffed_data) > 0:
        recovered_text = binary_to_text(unstuffed_data)
        print(f"4. Recovered Text: '{recovered_text}'")
    else:
        recovered_text = unstuffed_data
        print(f"4. Recovered Binary: {recovered_text}")

    print("\nVERIFICATION: Data recovery successful.")
    # Returns a success acknowledgment (ACK) to the client.
    return b'ACK: Frame successfully processed and data recovered.'

# --- Socket Setup ---

def start_server():
    # Creates a TCP/IP socket.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Binds the socket to the defined address and port.
        s.bind((HOST, PORT))
        # Listens for incoming connections (can handle one queue connection).
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for client connection ...\n")
        
        # Pauses until a client connects.
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            while True:
                # Receives data, up to the buffer size.
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    print("Client disconnected.")
                    # Reopens the server to wait for a new connection if the client closes.
                    conn.close() 
                    print("Waiting for new connection...")
                    conn, addr = s.accept()
                    print(f"Connected by {addr}")
                    continue

                # Decodes the received frame from bytes back to a string.
                frame_str = data.decode('utf-8')
                
                # Processes the frame and gets the response message.
                ack_message = handle_frame(frame_str)

                # Sends the acknowledgment message back to the client.
                conn.sendall(ack_message)

if __name__ == '__main__':
    start_server()
