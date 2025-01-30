import re
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

devices = {"fan", "light", "ac", 'heater'}
locations = {"living room", "bedroom", "kitchen", "bathroom"}

# Initialize the model at the beginning
model = SmartHomeIntentModel()
df = model.load_data()
model.train(df)
model.save_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")
model.load_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")

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
    return model.predict_intent(text)

def get_device(text, devices):
    """
    Extract the device from the input text.
    
    Args:
        text (str): The preprocessed input text.
        devices (set): A set of device names.
    
    Returns:
        str: The extracted device, or None if no device is found.
    """
    for device in devices:
        if device in text:
            return device
    return None  # No device found

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

def extract_command(text: str) -> dict:
    """
    Extract all command components from the input text.
    Returns a dictionary with intent, device, location, and value.
    """
    text = text.lower()
    
    return {
        "intent": get_intent_model(text),
        "device": get_device(text, devices),
        "location": get_location(text, locations),
        "value": get_value(text),
    }

if __name__ == "__main__":
    # Test with different phrasings
    test_phrases = [
        "set temperature to 25 degrees of the heater in the living room",
        "set temperature of the heater in the living room to 25",
        "adjust the living room heater at 23°",
        "change temperature to 22 in the bedroom heater",
        "set heater to 30 degrees",
        "turn on the light in the kitchen",
        "switch on the fan in the living room",
        "turn the lights in the living room off",
        "I want you to turn the fan in the living room off",
        "could you please turn off the fan in the living room",
        "enable the ac in the bedroom",
        "power up the fan in the living room",
        "make the fan speed 3 in the bedroom",

    ]

    for text in test_phrases:
        print(f"Input: {text}")
        print(extract_command(text))
