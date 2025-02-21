from Speaker import speaker
def command_execute(command:dict, previous_command:dict=None) -> dict:
    if command['intent'] == 'turn_on':
        if command["device"] == 'light' and command['location'] == None and previous_command != None and previous_command['device'] == 'light':
            command['location'] = previous_command['location']
        response_msg = f"Turning on {command['device']} at {command['location']}"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": command['device'],
            "location": command['location'],
            "status": True,
            "value": None
        }
    elif command['intent'] == 'turn_off':
        if command["device"] == 'light' and command['location'] == None and previous_command != None and previous_command['device'] == 'light':
            command['location'] = previous_command['location']

        response_msg = f"Turning off {command['device']} at {command['location']}"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": command['device'],
            "location": command['location'],
            "status": False,
            "value": None
        }
    elif command['intent'] == 'set_temperature':  
        response_msg = f"Setting temperature of {command['device']} at {command['location']} to {command['value']}°C"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": command['device'],
            "location": command['location'],
            "status": None,
            "value": command['value']
        }
    elif command['intent'] == 'set_fan_speed':
        response_msg = f"Setting fan speed of {command['device']} at {command['location']} to {command['value']}"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": command['device'],
            "location": command['location'],
            "status": None,
            "value": command['value'],
        }
    elif command['intent'] == 'open_door':
        response_msg = f"Opening the door"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": "door",
            "location":None,
            "status": True,
            "value": None
        }
    elif command['intent'] == 'close_door':
        response_msg = f"Closing the door"
        print(response_msg)
        speaker.text_to_sound(response_msg)
        response = {
            "device": "door",
            "location": None,
            "status": False,
            "value": None
        }
    else:
        print("Invalid command!")
        response = None
    return response



if __name__ == "__main__":
    from mqtt import mqtt_send
    command_list = [
        {
        'intent': 'turn_on',
        'device': 'light',
        'location': 'living room',
        'temperature': None
    },
    {
        'intent': 'turn_on',
        'device': 'light',
        'location': None,
        'value': None
    },
    {
        'intent': 'turn_off',
        'device': 'light',
        'location': None,
        'value': None

    }
    ]
    previous_command = None
    for command in command_list:
        response = command_execute(command,previous_command=previous_command)  # Expected output: Turning on light at living room
        print(response)
        previous_command = response
    # mqtt_send(response,username="abdo",password="234")  # Expected output: Message 'Turning on light at living room' published to topic 'home/assistant'



