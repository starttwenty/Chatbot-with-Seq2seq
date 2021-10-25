Prepare
====================
Chatbot use Python ver 3.9
All libraries needed is in requirements.txt

Training
====================
* Download dataset from https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
* Need 2 files and store it in ./dataset:
```
movie_conversations.txt
movie_lines.txt
```
* Run file ```training.py``` with python
=> It will training with 100 epochs, then store weights in ./data/chatbot_weights.h5

Run Chatbot with terminal
====================
* Run file ```create_save_vocab.py``` to create 2 file vocab
```
vocab.pkl
inv_vocab.pkl
```
* Change these variables in file ```chatbot.py```
```
weights_file = './data/chatbot_weights.h5'
vocab_file = './data/vocab.pkl'
inv_vocab_file = './data/inv_vocab.pkl'
```
* Run file ```chatbot.py```


Run Chatbot with Web Interface
====================
* (Windows - Visual Studio Code) Run this command
```
python -m flask run
```
