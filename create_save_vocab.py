import pickle
import re

# ====================================================
# Import dataset
# ====================================================
lines = open('movie_lines.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')

# Split data into questions and answers
id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]

conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))

questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i+1]])
        
## delete variables
del(conversation, conversations, conversations_ids, i, id2line, line, lines)

# ====================================================
# Clean questions and answer
# ====================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))

clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))
    
## delete variables
del(answer, answers, question, questions)


# ====================================================
# Create vocabulary
# ====================================================
word2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1

## delete variables
del(word, question, answer)

threshold = 20
vocab = {}
vocab['<PAD>'] = 0
word_number = 1
for word, count in word2count.items():
    if count >= threshold:
        vocab[word] = word_number
        word_number += 1

tokens = ['<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    vocab[token] = len(vocab)
    
inv_vocab = {w_i: w for w, w_i in vocab.items()}

del(threshold, word_number, count, word, token, tokens, word2count)

# ====================================================
# Save vocabulary to file
# ====================================================
file = open('./data/vocab.pkl', 'wb')
pickle.dump(vocab, file)
file.close

file = open('./data/inv_vocab.pkl', 'wb')
pickle.dump(inv_vocab, file)
file.close