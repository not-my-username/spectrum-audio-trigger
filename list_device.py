import pyaudio

# Initialize PyAudio
audio = pyaudio.PyAudio()

def list_devices():
    print("Available input devices:")
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            print(f"Device Index: {i} - {device_info['name']}")

def get_supported_sample_rates(device_index):
    device_info = audio.get_device_info_by_index(device_index)
    print(f"Checking supported sample rates for device: {device_info['name']}")
    
    # Common sample rates to check
    common_rates = [8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
    
    supported_rates = []
    for rate in common_rates:
        try:
            if audio.is_format_supported(rate, input_device=device_index, input_channels=1, input_format=pyaudio.paInt16):
                supported_rates.append(rate)
        except ValueError:
            pass
    
    return supported_rates

# List all devices
list_devices()

# Ask user to input a device index to check sample rates
device_index = int(input("Enter device index to check supported sample rates: "))

# Get and print supported sample rates
supported_rates = get_supported_sample_rates(device_index)
print(f"Supported sample rates for device {device_index}: {supported_rates if supported_rates else 'None'}")

# Terminate PyAudio
audio.terminate()



