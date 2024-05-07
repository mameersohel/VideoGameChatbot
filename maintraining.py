import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split

lemmatizer = WordNetLemmatizer()

games = json.loads(open('games.json').read())
#initialize lists to store words, labels, and training data
words = []
labels = []
docs_x = []
docs_y = ['?', '!', '.', ',']

#iterate through each game pattern in the JSON data to tokenize and add to words list
for game in games['games']:
    for pattern in game['patterns']:
        wordList = nltk.word_tokenize(pattern)
        words.extend(wordList)
        docs_x.append((wordList, game['tag']))

        #add game tag to labels if not already present
        if game['tag'] not in labels:
            labels.append(game['tag'])

#lemmatization of words and filtering out punctuation marks from the words list and sort them
words = [lemmatizer.lemmatize(word) for word in words if word not in docs_y]
words = sorted(set(words))
labels = sorted(set(labels))

#save words and labels file
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(labels, open('labels.pkl', 'wb'))

#list of training data for neural network
training = []
output_empty = [0] * len(labels) #zeros list for labels

#going through each tokenized pattern and its matching tag
for docs in docs_x:
    bag = []
    wordPatterns = docs[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    #add 1's and 0's for matching words in lemmatized pattern
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)
    #add bag and outputRow to the training list
    outputRow = list(output_empty)
    outputRow[labels.index(docs[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)
#split data into training and testing
train_data, test_data = train_test_split(training, test_size=0.4, random_state=42)

#separate X and Y for training and testing
trainX = train_data[:, :len(words)]
trainY = train_data[:, len(words):]
testX = test_data[:, :len(words)]
testY = test_data[:, len(words):]

#create neural network model and layers
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1024, input_shape=(len(trainX[0]),), activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(512, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

#make SGD optimizer with learning rate, momentum, and nesterov momentum
sgd = tf.keras.optimizers.SGD(learning_rate=0.1, momentum=0.9, nesterov=True)
#compile model with categorical cross-entropy loss function and SGD optimizer
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#train model with epochs and batch size
model.fit(trainX, trainY, epochs=100, batch_size=32, verbose=1)

#accuracy
loss, accuracy = model.evaluate(testX, testY)
print('Test Accuracy:', accuracy)

#save model
model.save('chatbot_model.h5')
print('Model saved.')