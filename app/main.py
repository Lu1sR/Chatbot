import json

from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
from app.chatbot.app import *

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
        verb = 'venta' if self.contract == 'Venta' else 'alquiler'
        verb1 = 'vende' if self.contract == 'Venta' else 'alquila'
        monthly = 'mensuales' if self.contract == 'Alquiler' else ''
        conector = 'un' if self.type == 'Departamento' else 'una'
        str_templates = [
            f'{self.type} en {verb}, ubicación:{self.location} por $ {self.price} {monthly}, {self.description}',
            f'Se {verb1} {self.type} {self.description}, ubicación: {self.location}, valor de $ {self.price} {monthly}',
            f'En {self.location} hay disponible {conector} {self.type} con {self.description}, $ {self.price} {monthly}',
            f'Hay {conector} {self.type} que se {verb1}, ubicación: {self.location}, el precio es $ {self.price} {monthly}',
        ]
        # f'{self.type} en {self.contract}, ubicada/o en {self.location}, por $ {self.price}, {self.description}'
        return random.choice(str_templates)


class PropertySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'type', 'location', 'contract',
                  'price', 'description')


property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)


@app.route("/chat")
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


@app.route("/create_model", methods=["GET"])
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
            #new_intent['patterns'].append(pattern)

            contract_verb2 = 'venta' if property.contract == 'Venta' else 'alquiler'
            contract_verb3 = 'vendiendo' if property.contract == 'Venta' else 'alquilando'
            conector = 'un' if property.type == 'Departamento' else 'una'
            conector2 = 'los' if property.type == 'Departamento' else 'las'

            patterns1 = f'Necesito {contract_verb} {conector} {property.type} en {property.location}'
            patterns2 = f'Hay {property.type}s en {contract_verb2} en {property.location}?'
            patterns3 = f'Estan {contract_verb3} {property.type}s en {property.location}?'
            patterns4 = f'Que precio tiene el {contract_verb2} de {conector} {property.type} en {property.location}'
            patterns5 = f'Quiero {contract_verb} {conector} {property.type} en {property.location}'
            patterns6 = f'Deseo {contract_verb} {conector} {property.type} en {property.location}'
            patterns7 = f'Busco {conector} {property.type} para {contract_verb} en {property.location}'
            patterns8 = f'Que precio tienen {conector2} {property.type}s en {property.location}?'

            new_intent['patterns'].append(patterns1)
            new_intent['patterns'].append(patterns2)
            new_intent['patterns'].append(patterns3)
            new_intent['patterns'].append(patterns4)
            new_intent['patterns'].append(patterns5)
            new_intent['patterns'].append(patterns6)
            new_intent['patterns'].append(patterns7)
            new_intent['patterns'].append(patterns8)

            new_intent['responses'] = []
            new_intent['responses'].append(str(property))
            intents.append(new_intent)

    intents_dict = {}
    intents_dict['intents'] = intents
    intents_file = open(f'{basedir}/chatbot/properties_intents.json', 'w')
    intents_file.write(json.dumps(intents_dict))
    intents_file.close()
    os.remove('model/model.h5')
    init_bot()
    return "El modelo fue creado correctamente"


@app.route("/input/<msg>", methods=['GET'])
def input(msg=None):
    print(msg)
    aux = chat(msg)
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
