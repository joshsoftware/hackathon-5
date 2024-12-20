import socket
import os
from datetime import datetime
import threading
import time

class AudioStreamServer:
    def __init__(self, host=socket.gethostname(), port=5000, chunk_duration=10):
        self.host = host
        self.port = port
        self.chunk_duration = chunk_duration
        self.buffer = bytearray()
        self.buffer_lock = threading.Lock()
        
        self.save_dir = "raw_chunks"
        os.makedirs(self.save_dir, exist_ok=True)

        self.socket_chunk_size = 8192
        self.bytes_per_chunk = 44100 * 2 * 2 * self.chunk_duration  # 44.1kHz, 16-bit, stereo
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on port {self.port}...")

        threading.Thread(target=self.process_chunks, daemon=True).start()

        while True:
            conn, address = server_socket.accept()
            print(f"Connection from: {address}")
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(self.socket_chunk_size)
                if not data:
                    break
                
                with self.buffer_lock:
                    self.buffer.extend(data)
                    print(f"Received {len(data)} bytes")
                    
        except Exception as e:
            print(f"Client handling error: {e}")
        finally:
            conn.close()

    def process_chunks(self):
        while True:
            with self.buffer_lock:
                if len(self.buffer) >= self.bytes_per_chunk:
                    chunk_data = bytes(self.buffer[:self.bytes_per_chunk])
                    self.buffer = self.buffer[self.bytes_per_chunk:]
                    self.save_chunk_as_raw(chunk_data)
            time.sleep(0.1)

    def save_chunk_as_raw(self, chunk_data):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chunk_{timestamp}.raw"
            filepath = os.path.join(self.save_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(chunk_data)
            
            print(f"Saved chunk as RAW: {filename}")

        except Exception as e:
            print(f"Error saving RAW file: {e}")


if __name__ == '__main__':
    server = AudioStreamServer()
    server.start()
