import socket
import subprocess
import threading
import sys

class AudioStreamClient:
    def __init__(self, host=socket.gethostname(), port=5000):
        self.host = host
        self.port = port
        self.chunk_size = 8192
        self.running = False

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            # Convert MP3 to raw PCM using FFmpeg
            ffmpeg_process = subprocess.Popen([
                "ffmpeg", 
                "-i", filename,  # Input file
                "-loglevel", "panic",
                "-vn",  # No video
                "-f", "s16le",  # Raw PCM output
                "-acodec", "pcm_s16le",
                "-ar", "44100",  # Sample rate
                "-ac", "2",  # Stereo channels
                "pipe:1"
            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

            print("Starting audio stream...")
            self.running = True

            while self.running:
                data = ffmpeg_process.stdout.read(self.chunk_size)
                if not data:
                    break
                self.client_socket.sendall(data)

            print("Streaming finished")

        except Exception as e:
            print(f"Streaming error: {e}")

        finally:
            ffmpeg_process.kill()
            self.client_socket.close()

    def stop(self):
        self.running = False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} filename")
        sys.exit(-1)

    client = AudioStreamClient()
    stream_thread = threading.Thread(target=client.stream_audio, args=(sys.argv[1],))
    stream_thread.start()

    input("Press Enter to stop streaming...")
    client.stop()
    stream_thread.join()


if __name__ == "__main__":
    main()
