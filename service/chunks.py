import pyaudio
import wave
import sys
import subprocess
import socket
import threading
import time

class AudioStreamClient:
    def __init__(self, host=socket.gethostname(), port=5000):
        self.host = host
        self.port = port
        self.chunk_size = 1024
        self.running = False
        
    def connect(self):
        self.client_socket = socket.socket()
        try:
            self.client_socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def stream_audio(self, filename):
        if not self.connect():
            return
            
        try:
            # Start FFmpeg process to convert input file to raw PCM
            ffmpeg_process = subprocess.Popen([
                "ffmpeg", 
                "-i", filename,
                "-loglevel", "panic",
                "-vn",  # Disable video
                "-f", "s16le",  # Output format
                "-acodec", "pcm_s16le",  # Audio codec
                "-ar", "44100",  # Sample rate
                "-ac", "2",  # Channels
                "pipe:1"
            ], stdout=subprocess.PIPE)

            print("Starting audio stream...")
            self.running = True
            
            # Read and stream data
            while self.running:
                data = ffmpeg_process.stdout.read(self.chunk_size)
                if len(data) == 0:
                    break
                    
                # Send to socket
                self.client_socket.send(data)
                
            print("Streaming finished")
            
        except Exception as e:
            print(f"Streaming error: {e}")
            
        finally:
            # Cleanup
            if 'ffmpeg_process' in locals():
                ffmpeg_process.kill()
            self.client_socket.close()
    
    def stop(self):
        self.running = False

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} filename")
        sys.exit(-1)
        
    client = AudioStreamClient()
    
    # Start streaming in a separate thread
    stream_thread = threading.Thread(target=client.stream_audio, args=(sys.argv[1],))
    stream_thread.start()
    
    # Wait for user input to stop
    input("Press Enter to stop streaming...")
    client.stop()
    stream_thread.join()

if __name__ == "__main__":
    main()