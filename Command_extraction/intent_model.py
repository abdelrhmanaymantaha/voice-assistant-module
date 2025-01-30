import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

class SmartHomeIntentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))  # Using bigrams
        self.model = LogisticRegression()

    def load_data(self):
        data = [
    # Turn On/Off Devices
    {"text": "Turn on the living room lights", "intent": "turn_on"},
    {"text": "Switch off the living room lights", "intent": "turn_off"},
    {"text": "Power on the bedroom fan", "intent": "turn_on"},
    {"text": "Power off the bedroom fan", "intent": "turn_off"},
    {"text": "Turn on the air conditioner", "intent": "turn_on"},
    {"text": "Turn off the air conditioner", "intent": "turn_off"},
    {"text": "Power on the TV", "intent": "turn_on"},
    {"text": "Turn off the TV", "intent": "turn_off"},
    {"text": "Activate the heater", "intent": "turn_on"},
    {"text": "Deactivate the heater", "intent": "turn_off"},
    {"text": "Start the coffee machine", "intent": "turn_on"},
    {"text": "Stop the coffee machine", "intent": "turn_off"},
    {"text": "Enable the security system", "intent": "turn_on"},
    {"text": "Disable the security system", "intent": "turn_off"},
    {"text": "Power up the living room fan", "intent": "turn_on"},
    {"text": "Power down the living room fan", "intent": "turn_off"},
    {"text": "Turn on the kitchen lights", "intent": "turn_on"},
    {"text": "Turn off the kitchen lights", "intent": "turn_off"},
    {"text": "Switch on the bathroom fan", "intent": "turn_on"},
    {"text": "Switch off the bathroom fan", "intent": "turn_off"},
    {"text": "Turn on the ceiling fan", "intent": "turn_on"},
    {"text": "Turn off the ceiling fan", "intent": "turn_off"},
    {"text": "Power up the stereo", "intent": "turn_on"},
    {"text": "Power down the stereo", "intent": "turn_off"},
    {"text": "Enable the sprinkler system", "intent": "turn_on"},
    {"text": "Disable the sprinkler system", "intent": "turn_off"},
    {"text": "Start the dishwasher", "intent": "turn_on"},
    {"text": "Stop the dishwasher", "intent": "turn_off"},
    {"text": "Activate the outdoor lights", "intent": "turn_on"},
    {"text": "Deactivate the outdoor lights", "intent": "turn_off"},
    {"text": "Power up the garage lights", "intent": "turn_on"},
    {"text": "Power down the garage lights", "intent": "turn_off"},
    {"text": "Activate the washing machine", "intent": "turn_on"},
    {"text": "Deactivate the washing machine", "intent": "turn_off"},

    # Set Temperature of Any Device
    {"text": "Set the thermostat to 72 degrees", "intent": "set_temperature"},
    {"text": "Set the heater to 75 degrees", "intent": "set_temperature"},
    {"text": "Adjust the AC to 20 degrees", "intent": "set_temperature"},
    {"text": "Set the bedroom temperature to 22 degrees", "intent": "set_temperature"},
    {"text": "Change the thermostat to 24 degrees", "intent": "set_temperature"},
    {"text": "Set the office heater to 78 degrees", "intent": "set_temperature"},
    {"text": "Cool the room to 18 degrees", "intent": "set_temperature"},
    {"text": "Increase the temperature to 25 degrees", "intent": "set_temperature"},
    {"text": "Lower the AC to 19 degrees", "intent": "set_temperature"},
    {"text": "Set the living room temperature to 70 degrees", "intent": "set_temperature"},
    {"text": "Set the kitchen to 68 degrees", "intent": "set_temperature"},
    {"text": "Adjust the office to 72 degrees", "intent": "set_temperature"},
    {"text": "Change the bedroom temperature to 74 degrees", "intent": "set_temperature"},
    {"text": "Set the bathroom temperature to 76 degrees", "intent": "set_temperature"},
    {"text": "Cool down the living room to 20 degrees", "intent": "set_temperature"},
    {"text": "Increase the kitchen temperature to 22 degrees", "intent": "set_temperature"},
    {"text": "Lower the bedroom temperature to 18 degrees", "intent": "set_temperature"},
    {"text": "Set the garage to 65 degrees", "intent": "set_temperature"},
    {"text": "Adjust the basement to 70 degrees", "intent": "set_temperature"},
    {"text": "Change the attic to 75 degrees", "intent": "set_temperature"},
    
    # Open/Close Door
    {"text": "Open the front door", "intent": "open_door"},
    {"text": "Close the front door", "intent": "close_door"},
    {"text": "Unlock the garage door", "intent": "open_door"},
    {"text": "Lock the garage door", "intent": "close_door"},
    {"text": "Open the back door", "intent": "open_door"},
    {"text": "Close the back door", "intent": "close_door"},
    {"text": "Open the main gate", "intent": "open_door"},
    {"text": "Close the main gate", "intent": "close_door"},
    {"text": "Open the patio door", "intent": "open_door"},
    {"text": "Close the patio door", "intent": "close_door"},
    {"text": "Unlock the front door", "intent": "open_door"},
    {"text": "Lock the front door", "intent": "close_door"},
    {"text": "Open the basement door", "intent": "open_door"},
    {"text": "Close the basement door", "intent": "close_door"},
    {"text": "Open the attic door", "intent": "open_door"},
    {"text": "Close the attic door", "intent": "close_door"},
    {"text": "Unlock the back door", "intent": "open_door"},
    {"text": "Lock the back door", "intent": "close_door"},
    {"text": "Open the side door", "intent": "open_door"},
    {"text": "Close the side door", "intent": "close_door"},
    
    # Set Fan Speed
    {"text": "Set the fan speed to 3", "intent": "set_fan_speed"},
    {"text": "Set the bedroom fan speed to level 2", "intent": "set_fan_speed"},
    {"text": "Adjust the fan speed to 5", "intent": "set_fan_speed"},
    {"text": "Change the fan speed to 1", "intent": "set_fan_speed"},
    {"text": "Lower the fan speed to 2", "intent": "set_fan_speed"},
    {"text": "Increase the fan speed to 4", "intent": "set_fan_speed"},
    {"text": "Set the living room fan speed to 3", "intent": "set_fan_speed"},
    {"text": "Set the kitchen fan speed to level 4", "intent": "set_fan_speed"},
    {"text": "Adjust the office fan speed to 2", "intent": "set_fan_speed"},
    {"text": "Change the bathroom fan speed to 1", "intent": "set_fan_speed"},
    {"text": "Lower the ceiling fan speed to 3", "intent": "set_fan_speed"},
    {"text": "Increase the garage fan speed to 5", "intent": "set_fan_speed"},
    {"text": "Set the attic fan speed to 4", "intent": "set_fan_speed"},
    {"text": "Set the basement fan speed to 2", "intent": "set_fan_speed"},
    {"text": "Adjust the patio fan speed to 3", "intent": "set_fan_speed"},
    {"text": "Change the living room fan speed to 5", "intent": "set_fan_speed"},
    {"text": "Lower the kitchen fan speed to 1", "intent": "set_fan_speed"},
    {"text": "Increase the bedroom fan speed to 4", "intent": "set_fan_speed"},
    {"text": "Set the office fan speed to 2", "intent": "set_fan_speed"},
    {"text": "Adjust the bathroom fan speed to 3", "intent": "set_fan_speed"},
    
    # Additional sample
    {"text": "Activate the fan", "intent": "turn_on"},
    {"text": "Deactivate the fan", "intent": "turn_off"},
    {"text": "Switch off the lights in the kitchen", "intent": "turn_off"},
    {"text": "Switch on the lights in the living room", "intent": "turn_on"},
]


        return pd.DataFrame(data)

    def train(self, df):
        X_train, X_test, y_train, y_test = train_test_split(df["text"], df["intent"], test_size=0.2, random_state=42)
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        self.model.fit(X_train_tfidf, y_train)
        y_pred = self.model.predict(X_test_tfidf)
        print(classification_report(y_test, y_pred))

    def save_model(self, model_path, vectorizer_path):
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)

    def load_model(self, model_path, vectorizer_path):
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict_intent(self, text, threshold=0.3):
        text_tfidf = self.vectorizer.transform([text])
        probabilities = self.model.predict_proba(text_tfidf)
        max_prob = max(probabilities[0])
        print(f"Max Probability: {max_prob}")
        print(f"Predicted Intent: {self.model.predict(text_tfidf)[0]}")
        if max_prob < threshold:
            return "unsupported"
        return self.model.predict(text_tfidf)[0]
    
if __name__ == "__main__":
    model = SmartHomeIntentModel()
    df = model.load_data()
    model.train(df)
    model.save_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")
    model.load_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")

    new_input = [
        "Turn off the living room lights",
        "Set the thermostat to 72 degrees",
        "Open the front door",
        "Turn on the bedroom fan",
        "Turn on the air conditioner",
        "Turn on the heater",
        "Turn on the TV",
        "turn the lights in the living room off",
        "set temperature to 22 in the bedroom ",
        "i want you to turn the fan in the living room off",
        "tell me a joke",
        "what is the weather like today",
        "play some music",
        "increase the volume",
    ]
    for text in new_input:
        intent = model.predict_intent(text)
        print(f"Input: {text}")
        print(f"Predicted Intent: {intent}")
        print()
