import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import socket

# --- Network Configuration (MUST match server.py) ---
FLAG = "01111110"
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 666        # The port used by the server
BUFFER_SIZE = 1024

# --- Core Bit Stuffing Logic ---

# Converts text to binary, preserving '0'/'1' and encoding other characters as ASCII.
def text_to_binary(text):
    binary_parts = []
    for c in text:
        if c == '0' or c == '1':
            binary_parts.append(c)
        else:
            binary_parts.append(format(ord(c), '08b'))
    return "".join(binary_parts)

# Inserts a '0' bit after five consecutive '1's in the data.
def bit_stuff(data):
    stuffed_bits = []
    count = 0
    for bit in data:
        stuffed_bits.append(bit)
        if bit == '1':
            count += 1
            if count == 5:
                stuffed_bits.append('0')
                count = 0
        else:
            count = 0
    return "".join(stuffed_bits)

# --- Tkinter Application Class ---

class BitStuffingClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Client")
        master.geometry("800x550")

        # --- Variables ---
        self.input_var = tk.StringVar(value="1111101111111111") # Example showing stuffing
        self.raw_binary_var = tk.StringVar()
        self.stuffed_var = tk.StringVar()
        self.frame_var = tk.StringVar()
        self.transmission_status_var = tk.StringVar()
        self.ack_var = tk.StringVar(value="Waiting for transmission...")

        # --- Styles ---
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        style.configure("TButton", font=('Arial', 10, 'bold'))
        style.configure("Header.TLabel", font=('Arial', 14, 'bold'), foreground="#d9534f")

        # --- Main Layout ---
        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        ttk.Label(main_frame, text="CLIENT", style="Header.TLabel").pack(pady=10)

        # Input Frame
        input_frame = ttk.Frame(main_frame, padding="10", relief=tk.GROOVE)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Message Input:", font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, width=50, font=('Arial', 11))
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, text="🚀 ENCODE & SEND FRAME", command=self.run_simulation).grid(row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=10)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=5)

        # Output Frame
        output_frame = ttk.Frame(main_frame, padding="15", relief=tk.SOLID, borderwidth=1)
        output_frame.pack(fill="x", padx=5, pady=5)
        
        # Setup Client UI outputs
        r = 0
        self._create_output_section(output_frame, "1. Raw Binary Data", self.raw_binary_var, r); r += 2
        self._create_output_section(output_frame, "2. Stuffed Binary Data", self.stuffed_var, r); r += 2
        
        ttk.Label(output_frame, text=f"FLAG: {FLAG}", foreground="#e85e00").grid(row=r, column=0, sticky="w", pady=(5, 0))
        r+=1
        self._create_output_section(output_frame, "3. Transmission Frame", self.frame_var, r); r += 2
        
        # Transmission Status
        ttk.Label(output_frame, text="Transmission Status:", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", pady=(10, 0))
        self.status_label = ttk.Label(output_frame, textvariable=self.transmission_status_var, font=('Arial', 10, 'italic'), foreground="blue")
        self.status_label.grid(row=r+1, column=0, sticky="w", padx=5, pady=(0, 10)); r += 2

        # Server Acknowledgment
        ttk.Label(output_frame, text="Server Acknowledgment:", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", pady=(10, 0))
        self.ack_label = ttk.Label(output_frame, textvariable=self.ack_var, font=('Arial', 12, 'bold'), foreground="darkgreen")
        self.ack_label.grid(row=r+1, column=0, sticky="w", padx=5, pady=(0, 10))

        output_frame.columnconfigure(0, weight=1)

    # Helper function to create labeled output fields.
    def _create_output_section(self, parent, title, variable, row):
        ttk.Label(parent, text=f"{title}:", style="TLabel").grid(row=row, column=0, sticky="w", pady=(5, 0))
        entry = ttk.Entry(parent, textvariable=variable, width=80, state='readonly', font=('Courier', 10))
        entry.grid(row=row + 1, column=0, sticky="we", padx=5, pady=(0, 10))
        return entry

    # Main function that handles encoding and socket communication.
    def run_simulation(self):
        # Reset output variables.
        self.raw_binary_var.set("")
        self.stuffed_var.set("")
        self.frame_var.set("")
        self.transmission_status_var.set("Attempting connection...")
        self.ack_var.set("Waiting for server response...")
        
        user_input = self.input_var.get()
        if not user_input:
            messagebox.showerror("Error", "Please enter a message to simulate.")
            return

        # 1. Convert Input Data
        original_data = text_to_binary(user_input)
        self.raw_binary_var.set(original_data)

        # 2. Bit Stuffing
        stuffed_data = bit_stuff(original_data)
        self.stuffed_var.set(stuffed_data)

        # 3. Framing
        frame_to_send = FLAG + stuffed_data + FLAG
        self.frame_var.set(frame_to_send)

        # --- SOCKET TRANSMISSION ---
        try:
            # Create a socket (TCP) and connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                
                # Send the frame as UTF-8 encoded bytes
                s.sendall(frame_to_send.encode('utf-8'))
                
                # Update status
                self.transmission_status_var.set(f"SENT: Frame transmitted to {HOST}:{PORT}")

                # Wait for ACK from server
                ack = s.recv(BUFFER_SIZE)
                self.ack_var.set(ack.decode('utf-8'))

        except ConnectionRefusedError:
            self.transmission_status_var.set("ERROR: Connection Refused.")
            self.ack_var.set("Server is not running. Please start 'server.py' first.")
            messagebox.showerror("Connection Error", "Server is not running. Please start 'server.py' first.")
        except Exception as e:
            self.transmission_status_var.set(f"ERROR: {e}")
            self.ack_var.set("Transmission Failed.")
            messagebox.showerror("Socket Error", f"An error occurred during transmission: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BitStuffingClientApp(root)
    root.mainloop()