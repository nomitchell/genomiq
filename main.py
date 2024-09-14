from flask import Flask, request, jsonify, render_template, send_file
import os

from plasmid import Plasmid
from model import Model

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

UPLOAD_FOLDER = 'input/plasmid'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'dna'}

# using global var for now, fix later
plasmid = None

model = Model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path):
    labels = []
    with open(file_path, 'r') as file:
        # Example processing logic
        for line in file:
            labels.append(line.strip())
    return labels

def convert_to_dict_of_dicts(data):
    return {i: item for i, item in enumerate(data)}

@app.route('/upload', methods=['POST'])
def upload_file():
    global plasmid

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], "plasmid.dna")
        file.save(filename)
        
        # Process the file and get labels
        plasmid = Plasmid(filename)
        features = convert_to_dict_of_dicts(plasmid.feat)
        print("returing features")
        return jsonify(features)
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/insert', methods=['POST'])
def insert_gene():
    global plasmid

    req_data = request.get_json()

    style = req_data["generation"]

    if style == "from-scratch":
        dna, zscore = model.run_scratch(req_data["message"])
    else:
        dna, _ = model.run_retrieval(req_data["message"])
        zscore = None

    print("here a time")
    plasmid.insert(dna)

    features = convert_to_dict_of_dicts(plasmid.feat)

    if zscore is not None:
        features[1000] = {'z_score': zscore}

    return jsonify(features)

@app.route('/save', methods=['GET'])
def save_file():
    global plasmid
    print("top")

    path = plasmid.save()

    print(path)
    
    return send_file(path, as_attachment=True)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this template contains your visualizer
