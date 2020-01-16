import json

from flask import *
from chatbot.app import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='static/templates')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'realestate.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Casa | Departamento | Suite | Oficina | Bodega | ...
    type = db.Column(db.String(32))
    # Urdesa | Kennedy | Via Samborondon | ...
    location = db.Column(db.String(32))
    contract = db.Column(db.String(32))  # Alquilar | Comprar
    price = db.Column(db.Float())
    description = db.Column(db.String(512))

    def __init__(self, type, location, contract, price, description):
        self.type = type
        self.location = location
        self.contract = contract
        self.price = price
        self.description = description

    def __str__(self):
        return f'{self.type} en {self.contract}, ubicada/o en {self.location}, por $ ${self.price}, {self.description}'


class PropertySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'type', 'location', 'contract',
                  'price', 'description')


property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)


@app.route("/")
def home():
    return render_template('chat.html')

@app.route("/list")
def table():
    return render_template('table-list.html')

@app.route("/form")
def form():
    return render_template('property-form.html')

def check_tag(intents_list, tag):
    c = 0
    for intent in intents_list:
        if intent['tag'] == tag:
            return (True, c)
        c += 1
    return (False, -1)

@app.route("/create_model")
def init():
    intents = []
    all_properties = Property.query.all()
    for property in all_properties:
        contract_verb = 'comprar' if property.contract == 'Venta' else 'alquilar'
        pattern = f'{contract_verb} {property.type} {property.location}'
        is_tag_present, tag_index = check_tag(intents, pattern)
        if is_tag_present:
            intent = intents[tag_index]
            if 'responses' in intent:
                intent['responses'].append(str(property))
            else:
                intent['responses'] = []
                intent['responses'].append(str(property))
        else:
            new_intent = {}
            new_intent['tag'] = pattern
            new_intent['patterns'] = []
            new_intent['patterns'].append(pattern)
            new_intent['responses'] = []
            new_intent['responses'].append(str(property))
            intents.append(new_intent)

    intents_dict = {}
    intents_dict['intents'] = intents

    intents_file = open(f'{basedir}/chatbot/properties_intents.json', 'w')
    intents_file.write(json.dumps(intents_dict))
    intents_file.close()
    init_bot()
    return "El modelo fue creado correctamente"

@app.route("/input/<msg>",methods=['GET'])
def input(msg=None):
    print(msg)
    aux=chat(msg)
    return jsonify(aux)

@app.route("/property", methods=["POST"])
def add_property():
    type = request.json['type']
    location = request.json['location']
    contract = request.json['contract']
    price = request.json['price']
    description = request.json['description']
    new_property = Property(type, location, contract,
                            price, description)
    db.session.add(new_property)
    db.session.commit()
    return property_schema.jsonify(new_property)

@app.route("/properties", methods=["GET"])
def get_properties():
    all_properties = Property.query.all()
    result = properties_schema.dump(all_properties)
    return jsonify(result)

@app.route("/properties/<id>", methods=["GET"])
def property_detail(id):
    property = Property.query.get(id)
    return property_schema.jsonify(user)

@app.route("/property/<id>", methods=["DELETE"])
def property_delete(id):
    property = Property.query.get(id)
    db.session.delete(property)
    db.session.commit()
    return property_schema.jsonify(property)

if __name__ == "__main__":
    app.run()