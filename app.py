from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models import db, Client

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/submit_kyc', methods=['POST'])
def submit_kyc():
    return handle_submission('KYC')

@app.route('/submit_kyb', methods=['POST'])
def submit_kyb():
    return handle_submission('KYB')

def handle_submission(form_type):
    data = request.form.to_dict()
    client = Client(form_type=form_type, data=data)
    db.session.add(client)
    db.session.commit()

    client_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(client.id))
    os.makedirs(client_folder, exist_ok=True)

    for file_key in request.files:
        file = request.files[file_key]
        file.save(os.path.join(client_folder, file.filename))

    return jsonify({'message': 'Submitted successfully', 'client_id': client.id}), 201

@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'form_type': c.form_type,
        'status': c.status,
        'created_at': c.created_at.isoformat(),
        'data': c.data
    } for c in clients])

@app.route('/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(client_id))
    if os.path.exists(upload_folder):
        files = os.listdir(upload_folder)
        file_urls = [f'/uploads/{client_id}/{filename}' for filename in files]
    else:
        file_urls = []
    
    return jsonify({
        'id': client.id,
        'form_type': client.form_type,
        'status': client.status,
        'created_at': client.created_at.isoformat(),
        'data': client.data,
        'documents': file_urls
    })

@app.route('/client/<int:client_id>/status', methods=['POST'])
def update_client_status(client_id):
    client = Client.query.get_or_404(client_id)
    status = request.json.get('status')
    if status not in ['Pendente', 'Aprovado', 'Rejeitado']:
        return jsonify({'error': 'Invalid status'}), 400
    
    client.status = status
    db.session.commit()
    return jsonify({'message': 'Status updated'})

@app.route('/uploads/<int:client_id>/<path:filename>', methods=['GET'])
def uploaded_file(client_id, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(client_id)), filename)

if __name__ == '__main__':
    app.run(debug=True)