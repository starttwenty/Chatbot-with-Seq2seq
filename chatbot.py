from inference_model import inference_model

print("##########################################")
print("#          Chatbot application           #")
print("##########################################")

weights_file = './data/chatbot_weights.h5'
vocab_file = './data/vocab.pkl'
inv_vocab_file = './data/inv_vocab.pkl'

prediction = inference_model(weights_file, vocab_file, inv_vocab_file)
while True:
    question = input("You: ")
    answer = prediction.predict_answer(question)
    print("chatbot attention : ", answer )
    print("==============================================")