from Command_extraction.command_extract import extract_command
from Recorder import recorder
from Speaker.speaker import text_to_sound
from SpeechToText import model
from command_execute.command_executor import command_execute
from command_execute import mqtt
from TextPreProcessing import text_processing

SPEECH_FILE = "output.wav"
AUDIO_DURATION = 2
previous_command = None

try:
    while True:
        text_to_sound('How can I help you?')
        recorder.record_audio_silence(output_file=SPEECH_FILE)
        text = model.speech_to_text(SPEECH_FILE)
        print(f"User said: {text}")

        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        text_to_sound(text)
        command = extract_command(text)
        print(f'user command: {command}')
        response = command_execute(command, previous_command=previous_command)
        if  response:
            previous_command = response
            print( f"previous location: {previous_command['location']}")
            print(f"Response: {response}")
            print()

            if 'stop' in text:
                break
        else:
            print("Invalid command!")
            text_to_sound("Sorry, I didn't understand that command. Please try again.")

        print("Waiting for the next command...")
        user = input("Press Enter to continue...")
        if user == 'n':
            
            break

except KeyboardInterrupt:
    print("Exiting...")
    pass
except {
    Exception
} as e:
    print(f"An error occurred: {e}")