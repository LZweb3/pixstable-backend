from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(10), nullable=False)  # 'KYC' ou 'KYB'
    data = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(20), default='Pendente')  # Pendente, Aprovado, Rejeitado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)