import pyaudio
import numpy as np
import asyncio
import websockets
import json
import sys

# Parameters
CHUNK_SIZE = 1024  # Size of audio chunk
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1  # Mono audio

# Check for command-line arguments
if len(sys.argv) < 5:
    print("Usage: python script.py <samprate> <uuid> <threshold> <hold_time> <fade_out_time>")
    sys.exit(1)

try:
    RATE = int(sys.argv[1])  # Sample rate from CLI argument
    SCENE_UUID = sys.argv[2]  # UUID from CLI argument
    THRESHOLD = int(sys.argv[3])  # Threshold from CLI argument
    HOLD_TIME = float(sys.argv[5])  # Hold time from CLI argument
    FADE_OUT_TIME = float(sys.argv[4])  # Fade out time from CLI argument
except ValueError:
    print("Invalid input. Please ensure sample rate and threshold are integers and hold/fade times are floats.")
    sys.exit(1)

async def on_peak_detected(websocket):
    ## Function to call when peak is detected
    command = {
        "for": SCENE_UUID,
        "call": "flash",
        "args": [0.0, HOLD_TIME, FADE_OUT_TIME]
    }

    await websocket.send(json.dumps(command))


async def detect_peak_in_audio(data, websocket):
    # Convert byte data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Get the peak value in this chunk of audio
    peak = np.abs(audio_data).max()
    
    # Trigger the peak detection if above threshold
    if peak > THRESHOLD:
        await on_peak_detected(websocket)

async def main():
    uri = "ws://localhost:3824"
    supported_protocols = ["spectrum-json"]

    # Create the WebSocket connection
    websocket = await websockets.connect(uri, subprotocols=supported_protocols)

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    print("Listening for peaks...")

    try:
        while True:
            # Read audio chunk
            data = stream.read(CHUNK_SIZE)
            await detect_peak_in_audio(data, websocket)

    except KeyboardInterrupt:
        print("\nStopping detection...")

    # Close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    asyncio.run(main())

