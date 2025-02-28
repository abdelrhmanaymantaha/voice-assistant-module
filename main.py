from Command_extraction.command_extract import  extract_command_data
from Recorder import recorder
from Speaker.speaker import text_to_sound
from SpeechToText import model
from command_execute import command_executor
from TextPreProcessing import text_processing
from sql_modes import mode_database
import threading


# Define a function to initialize components in parallel
def initialize_components():
    global pipline, db
    pipline = model.SpeechToTextPipeline()  # Initialize speech-to-text model
    db = mode_database.ModeDatabase()  # Initialize database

# Create and start a thread for initialization
init_thread = threading.Thread(target=initialize_components)
init_thread.start()

init_thread.join()  # This ensures the components are ready before proceeding
print("Components initialized!")



def main():     
    SPEECH_FILE = "output.wav"
    AUDIO_DURATION = 2
    while True:
        try:
            
            text_to_sound('How can I help you?')
            recorder.record_audio_silence(output_file=SPEECH_FILE)
            text = pipline.transcribe(SPEECH_FILE)
            print(f"User said: {text}")

            print(f"Input: {text}")

            text = text_processing.text_preprocessor(text)
            print(f"Processed text: {text}")
            command = extract_command_data(text)
            print(f'user command: {command}')
            response = command_executor.command_execute(command)
            if  response:
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
        except {
        Exception
        } as e:
            print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()
