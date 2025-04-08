from app.models import Symptom, Disease, DiseaseSymptom
from typing import List

def get_probable_diseases(symptom_ids: List[int], top_n: int = 3):
    """
    Identifie les maladies probables en fonction des symptômes fournis.
    
    Args:
        symptom_ids: Liste d'IDs de symptômes
        top_n: Nombre de maladies à retourner
        
    Returns:
        Liste de tuples (disease, score, matched_symptoms)
    """
    # Obtenir toutes les maladies
    all_diseases = Disease.query.all()
    disease_scores = []
    
    for disease in all_diseases:
        total_score = 0
        matched_symptoms = []
        
        # Calculer le score de correspondance pour cette maladie
        for symptom_id in symptom_ids:
            association = DiseaseSymptom.query.filter_by(
                disease_id=disease.id, 
                symptom_id=symptom_id
            ).first()
            
            if association:
                total_score += association.weight
                symptom = Symptom.query.get(symptom_id)
                if symptom:
                    matched_symptoms.append(symptom.name)
        
        # Si la maladie correspond à au moins un symptôme
        if total_score > 0:
            disease_scores.append((disease, total_score, matched_symptoms))
    
    # Trier par score décroissant
    disease_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Retourner les top_n résultats
    return disease_scores[:top_n]