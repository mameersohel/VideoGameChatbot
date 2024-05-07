import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
games = json.loads(open('games.json').read())
words = pickle.load(open('words.pkl', 'rb'))
labels = pickle.load(open('labels.pkl', 'rb'))
model = load_model('chatbot_model.h5')

#tokenizes user input and compare with game tags to detect game names
#returns a list of detected game names
def detect_game_name(input):
    tokens = word_tokenize(input.lower())
    game_names = []
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens) + 1):
            sequence = " ".join(tokens[i:j])
            for game in games['games']:
                if sequence == game['tag'].lower():
                    game_names.append(sequence)
                    break
    return game_names

#tokenizes and lemmatizes the input sentence
#lemmatization reduces words to their base root
#returns a list of the lemmatized words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#create a bag of words for the user input
#each element in the bag represents the presence or absence of a word in the input sentence (1's and 0's)
#returns array representing the bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word.lower() == w:
                bag[i] = 1
    return np.array(bag)

#predicts the class (game tag) of the input sentence using a trained model
#uses bag of words representation and a trained neural model
#returns a list of dictionaries containing the predicted game tags and their probabilities
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.07
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'game': labels[r[0]]}) #add probability 'probability': str(r[1])})
    return return_list

#retrieves information about detected game based on its tag and the requested information type
def detected_response(game_tag, info_type):
    for game in games['games']:
        if game['tag'].lower() == game_tag:
            if info_type == 'description':
                description = game.get('responses', 'Description not available')
                if isinstance(description, list):
                    return '\n'.join(description)
                else:
                    return description
            elif info_type == 'release date':
                releasedate = game.get('release_date', 'Release date not available')
                if isinstance(releasedate, list):
                    return '\n'.join(releasedate)
                else:
                    return releasedate
            elif info_type == 'developer':
                developer = game.get('developer', 'Developer not available')
                if isinstance(developer, list):
                    return '\n'.join(developer)
                else:
                    return developer
    return "I'm sorry, that information is not available right now."

#generates a response for the predicted game based on available responses from the dataset
def predicted_response(predicted_games):
    tag = predicted_games[0]['game']
    for game in games['games']:
        if game['tag'] == tag:
            response = random.choice(game['responses'])
            return response
