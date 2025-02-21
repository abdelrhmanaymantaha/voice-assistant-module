import re
import os
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

devices = {"light", "ac", 'heater','tv' , 'fan'}
locations = {"living room", "bedroom", "kitchen", "bathroom"}
devices = {"lights", "ac", 'heater','tv' , 'fan','light'}

# Initialize the model at the beginning
model = SmartHomeIntentModel()
import os

# Check if model files exist
if not os.path.exists("smart_home_intent_model.pkl") or not os.path.exists("tfidf_vectorizer.pkl"):
    print("Model files not found. Training and saving the model...")

    df = model.load_data()  # Load data
    model.train(df)  # Train the model
    model.save_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")  # Save the model

# Load the model after ensuring it exists
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
    intent = model.predict_intent(text)
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

def extract_command(text: str) -> dict:
    """
    Extract all command components from the input text.
    Returns a dictionary with intent, device, location, and value.
    """
    text = text.lower()
    
    return {
        "intent":str(model.predict_intent(text)),
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
        "activate the fan",
        'Open the lights in the living room',
        'Open the lights in the living room.',
        'activate my mode',
        'activate the lights in the living room',
        'open the main door'


    ]
    from TextPreProcessing import text_processing 

    for text in test_phrases:
        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        print(extract_command(text))
        print('-' * 50)
