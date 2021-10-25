from flask import Flask, jsonify, request, render_template
from inference_model import inference_model

# Khởi tạo Flask
app = Flask(__name__)

# # Khởi tạo model
weights_file = './data/chatbot_weights.h5'
vocab_file = './data/vocab.pkl'
inv_vocab_file = './data/inv_vocab.pkl'

prediction = inference_model(weights_file, vocab_file, inv_vocab_file)
message = ""
reply = ""

# Hàm xử lý request
@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html')

@app.route("/test", methods=['GET', 'POST'])
def testfn():
    # POST request
    if request.method == 'POST':
        message = request.json['message']
        print ("Message: " + message)
        reply = prediction.predict_answer(message)
        print ("Reply: " + reply)
        return jsonify(reply=reply)

if __name__ == '__main__':
    app.run()