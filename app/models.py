from app import db

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Symptom {self.name}>'

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    first_aid = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Disease {self.name}>'

class DiseaseSymptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), nullable=False)
    weight = db.Column(db.Float, default=1.0)  # Poids du symptôme pour cette maladie
    
    disease = db.relationship('Disease', backref=db.backref('symptoms', lazy=True))
    symptom = db.relationship('Symptom', backref=db.backref('diseases', lazy=True))

class HealthCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    def __repr__(self):
        return f'<HealthCenter {self.name}>'