from Command_extraction.command_extract import extract_command_data
from Speaker import speaker
from mqtt import mqtt_send
def command_execute(command:dict, previous_command:dict=None) -> dict:
    if command['intent'] == 'turn_on':
        if command['device'] == previous_command['device'] and command['location'] == None:
            command['location'] = previous_command['location']

        mqtt_command = {f"{command['device']}" : False}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Turning on {command['device']} at {command['location']}"

    elif command['intent'] == 'turn_off':
        if command['device'] == previous_command['device'] and command['location'] == None:
            command['location'] = previous_command['location']
            mqtt_command = {f"{command['device']}" : False}
            mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Turning off {command['device']} at {command['location']}"

    elif command['intent'] == 'set_temperature':  
        if command['device'] == previous_command['device'] and command['location'] == None:
            command['location'] = previous_command['location']
            mqtt_command = {f"{command['device']}" : f'{command['value']}'}
            mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Setting temperature of {command['device']} at {command['location']} to {command['value']}"
        
    elif command['intent'] == 'set_fan_speed':
        if command['location'] == None:
            command['location'] = previous_command['location']
            mqtt_command = {"fan" : f'{command['value']}'}
            mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Setting fan speed at {command['location']} to {command['value']}"

    elif command['intent'] == 'open_door':
        mqtt_command = {"door" : True}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Opening the door"
    elif command['intent'] == 'close_door':
        mqtt_command = {"door" : False}
        mqtt_send(mqtt_command,username="abdo",password="234",topic=f"home/{command['location']}")
        response_msg = f"Closing the door"
    else:
        print("Invalid command!")
        response_msg = None
    return response_msg



if __name__ == "__main__":
    import importlib
    
    from TextPreProcessing import text_processing

    importlib.reload(text_processing)
    test_phrases = [
        'set heater to 30 degrees',
     ]
    
    previous_command = {
        'device': None,
        'location': None,
        'value': None
    }
    for text in test_phrases:
        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        command = extract_command_data(text)
        print(f"Command: {command}")
        response = command_execute(command,previous_command=previous_command)
        print(response)
        previous_command = command
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




