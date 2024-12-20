import socket
import os
from datetime import datetime
import threading
import time

class AudioStreamServer:
    def __init__(self, host=socket.gethostname(), port=5000, chunk_duration=5):
        self.host = host
        self.port = port
        self.chunk_duration = chunk_duration
        self.buffer = bytearray()
        self.buffer_lock = threading.Lock()
        
        # Create directory for saved chunks
        self.save_dir = "ts_chunks"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        # Size of chunks to read from socket
        self.socket_chunk_size = 8192
        
        # Approximate size for 5 seconds of audio data (bitrate * duration)
        # Assuming 128kbps audio
        self.bytes_per_chunk = 128 * 1024 * chunk_duration // 8
    
    def start(self):
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f"Server listening on port {self.port}...")
        
        processing_thread = threading.Thread(target=self.process_chunks)
        processing_thread.daemon = True
        processing_thread.start()
        
        while True:
            conn, address = server_socket.accept()
            print(f"Connection from: {address}")
            self.handle_client(conn)
    
    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(self.socket_chunk_size)
                if not data:
                    break
                
                with self.buffer_lock:
                    self.buffer.extend(data)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            conn.close()
    
    def process_chunks(self):
        while True:
            with self.buffer_lock:
                if len(self.buffer) >= self.bytes_per_chunk:
                    # Extract chunk
                    chunk_data = bytes(self.buffer[:self.bytes_per_chunk])
                    self.buffer = self.buffer[self.bytes_per_chunk:]
                    self.save_chunk(chunk_data)
            time.sleep(0.1)
    
    def save_chunk(self, chunk_data):
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chunk_{timestamp}.ts"
            filepath = os.path.join(self.save_dir, filename)
            
            # Save the audio chunk as a TS file
            with open(filepath, 'wb') as f:
                f.write(chunk_data)
            print(f"Saved chunk as TS: {filename}")
            
        except Exception as e:
            print(f"Error saving chunk: {e}")

if __name__ == '__main__':
    server = AudioStreamServer()
    server.start()
