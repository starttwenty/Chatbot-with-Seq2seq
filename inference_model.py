import pickle
import re
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

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

class inference_model:
    def __init__(self, weights_file, vocab_file, inv_vocab_file):
        self.weights_file = weights_file
        self.vocab = pickle.load(open(vocab_file, 'rb'))
        self.inv_vocab = pickle.load(open(inv_vocab_file, 'rb'))
        
        enc_inp = Input(shape=(20, ))
        dec_inp = Input(shape=(20, ))
        
        VOCAB_SIZE = len(self.vocab)
        embed = Embedding(VOCAB_SIZE, output_dim=200, input_length=20, trainable=True)
        
        enc_embed = embed(enc_inp)
        enc_lstm = LSTM(200, return_sequences=True, return_state=True)
        enc_op, h, c = enc_lstm(enc_embed)
        enc_states = [h, c]
        
        dec_embed = embed(dec_inp)
        dec_lstm = LSTM(200, return_sequences=True, return_state=True)
        dec_op, _, _ = dec_lstm(dec_embed, initial_state=enc_states)
        
        self.dense = Dense(VOCAB_SIZE, activation='softmax')
        dense_op = self.dense(dec_op)
        
        model = Model([enc_inp, dec_inp], dense_op)
        model.load_weights(self.weights_file)
        
        # inference model
        self.enc_model = Model([enc_inp], enc_states)
        
        decoder_state_input_h = Input(shape=(200,))
        decoder_state_input_c = Input(shape=(200,))
        
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_outputs, state_h, state_c = dec_lstm(dec_embed, initial_state=decoder_states_inputs)
        decoder_states = [state_h, state_c]
        
        self.dec_model = Model([dec_inp]+ decoder_states_inputs,
                          [decoder_outputs]+ decoder_states)

    def predict_answer(self, question):
        question = clean_text(question)
        text = []
        for x in question.split():
            try:
                text.append(self.vocab[x])
            except:
                text.append(self.vocab['<OUT>'])
        print (text)
        text = pad_sequences([text], 20, padding='post')

        stat = self.enc_model.predict(text)
        empty_target_seq = np.zeros(( 1 , 1))
        empty_target_seq[0, 0] = self.vocab['<SOS>']
        
        stop_condition = False
        answer = ""
        while not stop_condition :
            dec_outputs , h, c= self.dec_model.predict([empty_target_seq] + stat )
            decoder_concat_input = self.dense(dec_outputs)
    
            sampled_word_index = np.argmax(decoder_concat_input[0, -1, :] )
            sampled_word = self.inv_vocab[sampled_word_index] + ' '
    
            if sampled_word != '<EOS> ':
                answer += sampled_word  
            if sampled_word == '<EOS> ' or len(answer.split()) > 20:
                stop_condition = True 
    
            empty_target_seq = np.zeros( ( 1 , 1 ) )  
            empty_target_seq[ 0 , 0 ] = sampled_word_index
            stat = [h, c]  
        return answer


# print("##########################################")
# print("#          Chatbot application           #")
# print("##########################################")

# weights_file = './data/chatbot_weights.h5'
# vocab_file = './data/vocab.pkl'
# inv_vocab_file = './data/inv_vocab.pkl'

# prediction = inference_model(weights_file, vocab_file, inv_vocab_file)
# while True:
#     question = input("You: ")
#     answer = prediction.predict_answer(question)
#     print("chatbot attention : ", answer )
#     print("==============================================")   