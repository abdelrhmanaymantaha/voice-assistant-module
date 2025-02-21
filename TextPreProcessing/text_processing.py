import string

# Define your custom list of stopwords
stop_words = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
    "you", "your", "yours", "yourself", "yourselves", "he", "him", 
    "his", "himself", "she", "her", "hers", "herself", "it", "its", 
    "itself", "they", "them", "their", "theirs", "themselves", "what", 
    "which", "who", "whom", "this", "that", "these", "those", "am", 
    "is", "are", "was", "were", "be", "been", "being", "have", "has", 
    "had", "having", "do", "does", "did", "doing", "a", "an", "the", 
    "and", "but", "if", "or", "because", "as", "until", "while", 
    "of", "at", "by", "for", "with", "about", "against", "between", 
    "into", "through", "during", "before", "after", "above", "below", 
    "to", "from", "out", "over","under", "again", "further", "then", "once", "here", "there", 
    "when", "where", "why", "how", "all", "any", "both", "each", 
    "few", "more", "most", "other", "some", "such", "no", "nor", 
    "not", "only", "own", "same", "so", "than", "too", "very", 
    "s", "t", "can", "will", "just", "don", "should", "now","the","please"
}

def text_preprocessor (text:str):
    translator = str.maketrans('', '', string.punctuation)
    text = text.lower()
    text = text.translate(translator)

    words = text.split()

    # Remove stopwords
    filtered_words = [word for word in words if word.lower() not in stop_words] 

    preprocessed_text = " ".join(filtered_words)   
    return preprocessed_text


if __name__ == "__main__":
    text = ' please Turn off the light of living Room light.'

    print(text_preprocessor(text= text))

    