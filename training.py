import re

# ====================================================
# Bước 1: Chia dữ liệu thành tập câu hỏi và câu trả lời
# ====================================================
lines = open('./dataset/movie_lines.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('./dataset/movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')

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
# Bước 2: Làm sạch dữ liệu
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
# Bước 3: Tạo từ điển với ngưỡng = 20
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
# Bước 4: Biểu diễn số
# ====================================================
for i in range(len(clean_answers)):
    clean_answers[i] = '<SOS> ' + clean_answers[i] + ' <EOS>'

encoder_inp = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in vocab:
            ints.append(vocab['<OUT>'])
        else:
            ints.append(vocab[word])
    encoder_inp.append(ints)
decoder_inp = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in vocab:
            ints.append(vocab['<OUT>'])
        else:
            ints.append(vocab[word])
    decoder_inp.append(ints)
    
## delete variables
del(answer, clean_answers, clean_questions, i, ints, question, word)

sorted_encoder = []
sorted_decoder = []

for i in enumerate(encoder_inp):
    if len(i[1]) < 21 and len(decoder_inp[i[0]]) < 21:
        sorted_encoder.append(encoder_inp[i[0]])
        sorted_decoder.append(decoder_inp[i[0]])

## delete variables
del(decoder_inp, encoder_inp, i)

from tensorflow.keras.preprocessing.sequence import pad_sequences
encoder_input = pad_sequences(sorted_encoder, 20, padding='post', truncating='post')
decoder_input = pad_sequences(sorted_decoder, 20, padding='post', truncating='post')


# ====================================================
# Xây dựng mô hình học máy Seq2seq
# ====================================================
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input

enc_inp = Input(shape=(20, ))
dec_inp = Input(shape=(20, ))

VOCAB_SIZE = len(vocab)
embed = Embedding(VOCAB_SIZE, input_length=20, output_dim=200, trainable=True)

enc_embed = embed(enc_inp)
enc_lstm = LSTM(200, return_sequences=True, return_state=True)
enc_op, h, c = enc_lstm(enc_embed)
enc_states = [h, c]

dec_embed = embed(dec_inp)
dec_lstm = LSTM(200, return_sequences=True, return_state=True)
dec_op, _, _ = dec_lstm(dec_embed, initial_state=enc_states)

dense = Dense(VOCAB_SIZE, activation='softmax')
dense_op = dense(dec_op)

model = Model([enc_inp, dec_inp], dense_op)

model.compile(loss='categorical_crossentropy',metrics=['acc'],optimizer='adam')

model.summary()


# ====================================================
# Huấn luyện mô hình học máy Seq2seq
# ====================================================

epochs = 100
batch_size = 128
total_batches = len(encoder_input) // batch_size
save_text = []

from tensorflow.keras.utils import to_categorical
import numpy as np


# model.load_weights('./data/chatbot_weights.h5')

for epoch in range(epochs):
    loss_ave = []
    acc_ave = []
    for j in range(total_batches):
        indx = np.random.choice(np.arange(len(encoder_input)), batch_size, replace=False)
        x_input = encoder_input[indx]
        y_input = decoder_input[indx]
        output = []
        for i in y_input:
            output.append(i[1:])
        output = pad_sequences(output, 20, padding='post', truncating='post')
        output = to_categorical(output, len(vocab))
        loss = model.train_on_batch([x_input, y_input], output)
        loss_ave.append(loss[0])
        acc_ave.append(loss[1])
        if j%500 == 0 and j != 0:
            model.save_weights('./data/chatbot_weights.h5')
        print('Batch: {}/{}, loss = {}, acc = {}'.format(j, total_batches, loss[0], loss[1]))
    save_text.append([np.average(loss_ave), np.average(acc_ave)])
    np.savetxt('./data/log_v3.txt', np.array(save_text), delimiter=" ,")    
    model.save_weights('./data/chatbot_weights.h5')
    print('Epoch: {}/{}, Loss Average = {}, Acc Ave = {}'.format(epoch + 1, epochs, np.average(loss_ave), np.average(acc_ave)))