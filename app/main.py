from flask import *
from chatbot.app import *

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='static/templates')


if __name__ == "__main__":
    app.run()
    

@app.route("/create_model")
def init():
    init_bot()
    return "El modelo fue creado correctamente"

@app.route("/")
def home():
    return render_template('chat.html')

@app.route("/input/<msg>",methods=['GET'])
def input(msg=None):
    print(msg)
    aux=chat(msg)
    return jsonify(aux)
    