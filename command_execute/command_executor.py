from Command_extraction.command_extract import extract_command_data
from Recorder import recorder
from Speaker import speaker
from SpeechToText import model
from command_execute.mqtt import mqtt_send
from sql_modes import mode_database
from TextPreProcessing import text_processing
def command_execute(command:dict) -> dict:
    if command['intent'] == 'turn_on':

        mqtt_command = {f"{command['device']}" : True}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Turning on {command['device']} at {command['location']}"

    elif command['intent'] == 'turn_off':

        mqtt_command = {f"{command['device']}" : False}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Turning off {command['device']} at {command['location']}"

    elif command['intent'] == 'set_temperature': 

        mqtt_command = {"temperature" : f'{command['value']}'}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Setting temperature of {command['device']} at {command['location']} to {command['value']}"
        
    elif command['intent'] == 'set_fan_speed':

        mqtt_command = {"fan" : f'{command['value']}'}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Setting fan speed at {command['location']} to {command['value']}"

    elif command['intent'] == 'open_door':

        mqtt_command = {"door" : True}
        mqtt_send(mqtt_command,username="abdo",password="234",topic="home/security")
        response_msg = "Opening the door"

    elif command['intent'] == 'close_door':

        mqtt_command = {"door" : False}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/security")
        response_msg = "Closing the door"

    elif command['intent'] == 'execute_mode':
        mode_name = command['mode']
        print(f"Mode name: {mode_name}")
        db = mode_database.ModeDatabase()
        response_msg = f"Activating mode {mode_name}"
        mode = db.get_mode_by_name(mode_name)
        for cmd in mode['commands']:
            command_execute(cmd)

    elif command['intent'] == 'add_mode':
        speaker.text_to_sound('What is the mode name?')
        recorder.record_audio_silence('mode_name.wav')
        mode_name = model.SpeechToTextPipeline().transcribe('mode_name.wav')
        mode_name = text_processing.text_preprocessor(mode_name)
        print(f"Mode name: {mode_name}")
        db = mode_database.ModeDatabase()
        db.create_mode(mode_name)
        response_msg = f"Mode {mode_name} created successfully"

    else:
        print("Invalid command!")
        response_msg = None
    return response_msg



if __name__ == "__main__":

    
    from TextPreProcessing import text_processing


    test_phrases = [
        'activate study mode',
     ]
    

    for text in test_phrases:
        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        command = extract_command_data(text)
        print(f"Command: {command}")
        response = command_execute(command)
        print(response)

        print('-' * 50)


#     from mqtt import mqtt_send
#     command_list = [
#         {
#         'intent': 'turn_on',
#         'device': 'light',
#         'location': 'living room',
#         'temperature': None
#     },
#     {
#         'intent': 'turn_on',
#         'device': 'light',
#         'location': None,
#         'value': None
#     },
#     {
#         'intent': 'turn_off',
#         'device': 'light',
#         'location': None,
#         'value': None
#     }
#     ]
#     previous_command = {
#         'device': 'light',
#         'location': None,
#         'value': None
#     }
#     for command in command_list:
#         response = command_execute(command,previous_command=previous_command)  # Expected output: Turning on light at living room
#         print(response)
#         previous_command = command




