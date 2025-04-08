from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.forms import SymptomForm
from app.models import Symptom, Disease, HealthCenter
from app.diagnosis import get_probable_diseases
from app.maps import create_map, find_nearby_centers
from app.medical_data import init_medical_data
from flask import current_app


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # S'assurer que les données médicales sont initialisées
    if Symptom.query.count() == 0:
        with current_app.app_context():
            init_medical_data()
    
    # Récupérer tous les symptômes pour le formulaire
    symptoms = Symptom.query.all()
    
    # Créer le formulaire
    form = SymptomForm()
    form.symptoms.choices = [(s.id, s.name) for s in symptoms]
    
    if form.validate_on_submit():
        # Obtenir les symptômes sélectionnés
        selected_symptoms = form.symptoms.data
        
        # Obtenir la position de l'utilisateur
        latitude = form.latitude.data
        longitude = form.longitude.data
        
        # Rediriger vers la page de diagnostic
        return redirect(url_for('main.diagnosis_results', 
                               symptoms=','.join(map(str, selected_symptoms)),
                               lat=latitude if latitude else '',
                               lng=longitude if longitude else ''))
    
    return render_template('index.html', form=form)

@main_bp.route('/diagnosis', methods=['GET'])
def diagnosis_results():
    # Récupérer les paramètres
    symptom_ids = request.args.get('symptoms', '').split(',')
    symptom_ids = [int(s) for s in symptom_ids if s.isdigit()]
    
    latitude = request.args.get('lat', '')
    longitude = request.args.get('lng', '')
    
    try:
        latitude = float(latitude) if latitude else None
        longitude = float(longitude) if longitude else None
    except ValueError:
        latitude, longitude = None, None
    
    # Obtenir les maladies probables
    probable_diseases = get_probable_diseases(symptom_ids)
    
    # Trouver les centres de santé à proximité
    nearby_centers = find_nearby_centers(latitude, longitude)
    
    # Créer la carte des centres de santé
    health_map = create_map(latitude, longitude, nearby_centers)
    
    return render_template('diagnosis.html', 
                          diseases=probable_diseases,
                          centers=nearby_centers,
                          health_map=health_map)

@main_bp.route('/api/get-location', methods=['GET'])
def get_location():
    """API pour obtenir les coordonnées à partir d'une adresse."""
    address = request.args.get('address', '')
    
    # Utiliser une API de géocodage pour convertir l'adresse en coordonnées
    # Pour simplifier, nous utiliserons des coordonnées fixes pour cet exemple
    
    return jsonify({
        'latitude': 14.7167,
        'longitude': -17.4677
    })

@main_bp.route('/init-db', methods=['GET'])
def initialize_database():
    """Route pour initialiser la base de données (à des fins de développement)."""
    try:
        init_medical_data()
        return jsonify({'status': 'success', 'message': 'Base de données initialisée avec succès!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})