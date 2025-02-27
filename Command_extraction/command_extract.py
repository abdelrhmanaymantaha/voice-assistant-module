import re
import os
from Speaker import speaker
from Recorder import recorder
from SpeechToText import model
from TextPreProcessing import text_processing 
if __name__ == "__main__":
    from intent_model import SmartHomeIntentModel
else:
    from Command_extraction.intent_model import SmartHomeIntentModel


intent_patterns = {
    "TurnOnDevice": ["turn on", "switch on", "enable", "power up", "activate"],
    "TurnOffDevice": ["turn off", "switch off", "disable", "power down", "deactivate"],
    "SetTemperature": ["set temperature", "change temperature", "adjust temperature", "raise temperature", "lower temperature"],
    "LockDoor": ["lock the door", "secure the door", "close the door"],
    "UnlockDoor": ["unlock the door", "open the door", "unsecure the door"],
}


locations = {"living room", "bedroom", "kitchen", "bathroom"}
devices = {"lights", "ac", 'heater','tv' , 'fan','light'}

# Initialize the model at the beginning
intent_model = SmartHomeIntentModel()


# Check if model files exist
if not os.path.exists("smart_home_intent_model.pkl") or not os.path.exists("tfidf_vectorizer.pkl"):
    print("Model files not found. Training and saving the model...")

    df = intent_model.load_data()  # Load data
    intent_model.train(df)  # Train the model
    intent_model.save_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")  # Save the model

# Load the model after ensuring it exists
intent_model.load_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")



def get_intent(text, intent_patterns: dict):
    """
    Match the text to an intent using keyword matching.
    
    Args:
        text (str): The preprocessed input text.
        intent_patterns (dict): A dictionary mapping intents to their patterns.
    
    Returns:
        str: The matched intent, or None if no match is found.
    """
    for intent, patterns in intent_patterns.items():
        for pattern in patterns:
            if pattern in text:
                return intent
    return None  # No matching intent found

def get_intent_model(text):
    """
    Predict the intent of the input text using a pre-trained model.
    
    Args:
        text (str): The preprocessed input text.
    
    Returns:
        str: The predicted intent.
    """
    intent = intent_model.predict_intent(text)
    return intent


def get_device(text, devices):
    """
    Extract the device from the input text.
    
    Args:
        text (str): The preprocessed input text.
        devices (set): A set of device names.
    
    Returns:
        str: The extracted device, or None if no device is found.
    """
    # Create a regex pattern to match whole words
    pattern = r'\b(?:' + '|'.join(re.escape(device) for device in devices) + r')\b'
    
    # Search for the pattern in the input text
    match = re.search(pattern, text, re.IGNORECASE)
    
    # Return the matched device or None if no match is found
    return match.group(0) if match else None

def get_location(text, locations):
    """
    Extract the location from the input text.
    
    Args:
        text (str): The preprocessed input text.
        locations (set): A set of location names.
    
    Returns:
        str: The extracted location, or None if no location is found.
    """
    for location in locations:
        if location in text:
            return location
    return None  # No location found

def get_value(text: str):
    # Improved regex pattern to find temperature values
    text = text.lower()
    
    # Look for patterns like "to 25", "at 25", "set 25", etc.
    matches = re.findall(r'(to|at|set|adjust)\s+(\d+)(?:°| degrees?)?', text)
    
    # If no matches, look for standalone numbers
    if not matches:
        matches = re.findall(r'\b(\d+)(?:°| degrees?)?\b', text)
    
    # Return the first found number
    if matches:
        try:
            # Handle different match formats
            value = matches[0][1] if isinstance(matches[0], tuple) else matches[0]
            return int(value)
        except (IndexError, ValueError):
            return None
    return None

def extract_command_data(text: str, max_retries: int = 2) -> dict:
    """
    Extract all command components from the input text.
    Returns a dictionary with intent, device, location, and value.

    :param text: The input text from the user.
    :param max_retries: Maximum number of retries for missing entities.
    :return: A dictionary containing the command components or None if the command is invalid.
    """
    intent = get_intent_model(text)
    if intent == "unsupported":
        return None

    device = None
    location = None
    value = None

    if intent in ["turn_on", "turn_off"]:
        device = get_device(text, devices)
        location = get_location(text, locations)
        value = None
        # Retry for missing device
        retries = 0
        while device is None and retries < max_retries:
            device = uncompleted_command("device")
            device = get_device(device, devices)
            retries += 1

        # Retry for missing location
        retries = 0
        while location is None and retries < max_retries:
            location = uncompleted_command("location")
            location = get_location(location, locations)
            retries += 1

    elif intent == "set_temperature":
        location = get_location(text, locations)
        value = get_value(text)
        device = None

        # Retry for missing location
        retries = 0
        while location is None and retries < max_retries:
            location = uncompleted_command("location")
            location = get_location(location, locations)
            retries += 1

        # Retry for missing value
        retries = 0
        while value is None and retries < max_retries:
            value = uncompleted_command("value")
            value = get_value(value)
            retries += 1

    elif intent == "set_fan_speed":
        device = None
        location = get_location(text, locations)
        value = get_value(text)

        # Retry for missing location
        retries = 0
        while location is None and retries < max_retries:
            location = uncompleted_command("location")
            location = get_location(location, locations)
            retries += 1

        # Retry for missing value
        retries = 0
        while value is None and retries < max_retries:
            value = uncompleted_command("value")
            value = get_value(value)
            retries += 1

    # If any required entity is still missing after retries, discard the command
    if (intent in ["turn_on", "turn_off"] and (device is None or location is None)) or \
       (intent == "set_temperature" and (location is None or value is None)) or \
       (intent == "set_fan_speed" and (location is None or value is None)):
        return None

    return {"intent": intent, "device": device, "location": location, "value": value}


def uncompleted_command (missing_entity:str) -> str:
    """
      find the missing entity in the command
    """
    if missing_entity == "device":
        speaker.text_to_sound("sorry, what device do you say?")
    elif missing_entity == "location":
        speaker.text_to_sound("sorry, what room do you say?")
    elif missing_entity == "value":
        speaker.text_to_sound("sorry, what value do you say?")
    
    recorder.record_audio_silence('entity.wav')
    entity = model.SpeechToTextPipeline().transcribe('entity.wav')
    entity = text_processing.text_preprocessor(entity)
    return entity

if __name__ == "__main__":
    # Test with different phrasings
    test_phrases = [
        # "set temperature to 25 degrees of the heater in the living room",
        # "set temperature of the heater in the living room to 25",
        # "adjust the living room heater at 23°",
        # "change temperature to 22 in the bedroom heater",
        "set heater to 30 degrees",
        # "turn on the light in the kitchen",
        # "switch on the fan in the living room",
        # "turn the lights in the living room off",
        # "I want you to turn the fan in the living room off",
        # "could you please turn off the fan in the living room",
        # "enable the ac in the bedroom",
        # "power up the fan in the living room",
        # "make the fan speed 3 in the bedroom",
        # "activate the fan",
        # 'Open the lights in the living room',
        # 'Open the lights in the living room.',
        # 'activate my mode',
        # 'activate the lights in the living room',
        # 'open the main door',
        # 'tell me a joke',


    ]
    from TextPreProcessing import text_processing 

    for text in test_phrases:
        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        print(extract_command_data(text))
        print('-' * 50)
