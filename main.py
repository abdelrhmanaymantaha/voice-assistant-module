
from Command_extraction import command_extract


from Recorder import recorder
from Speaker.speaker import text_to_sound
from SpeechToText import model
from command_execute import command_executor
from TextPreProcessing import text_processing



# Initialize the speech-to-text pipeline once
pipline = model.SpeechToTextPipeline()


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
            command = command_extract.extract_command_data(text)
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
