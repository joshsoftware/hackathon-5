import socket
import time

class MP3StreamClient:
    def __init__(self, host=socket.gethostname(), port=5000):
        self.host = host
        self.port = port
        self.chunk_size = 8192  # Size of chunks to read from file
    
    def stream_file(self, filename):
        client_socket = socket.socket()
        try:
            client_socket.connect((self.host, self.port))
            
            with open(filename, 'rb') as file:
                while True:
                    data = file.read(self.chunk_size)
                    if not data:
                        break
                    client_socket.send(data)
                    # Small delay to simulate real-time streaming
                    time.sleep(0.1)
                    
            print("Finished streaming file")
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    client = MP3StreamClient()
    # Replace with your MP3 file path
    client.stream_file('uploaded_audio_files/recording.mp3')