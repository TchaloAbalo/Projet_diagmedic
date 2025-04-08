from app import db
from app.models import Symptom, Disease, DiseaseSymptom, HealthCenter

def init_medical_data():
    """Initialise la base de données avec des informations médicales."""
    
    # Créer les symptômes
    symptoms = [
        {'name': 'Fièvre'},
        {'name': 'Maux de tête'},
        {'name': 'Douleurs articulaires'},
        {'name': 'Fatigue'},
        {'name': 'Toux'},
        {'name': 'Écoulement nasal'},
        {'name': 'Maux de gorge'},
        {'name': 'Sueurs nocturnes'},
        {'name': 'Nausées'},
        {'name': 'Vomissements'},
        {'name': 'Diarrhée'},
        {'name': 'Éruption cutanée'},
        {'name': 'Douleurs abdominales'},
        {'name': 'Courbatures'},
        {'name': 'Frissons'},
        {'name': 'Soif excessive'},
        {'name': 'Urine foncée'},
        {'name': 'Bouche sèche'},
        {'name': 'Respiration rapide'},
        {'name': 'Vertiges'}
    ]
    
    for s in symptoms:
        symptom = Symptom.query.filter_by(name=s['name']).first()
        if not symptom:
            symptom = Symptom(name=s['name'])
            db.session.add(symptom)
    
    # Créer les maladies
    diseases = [
        {
            'name': 'Paludisme',
            'description': 'Maladie parasitaire transmise par la piqûre de moustiques anophèles.',
            'first_aid': 'Consultez un médecin dès que possible. Prenez du paracétamol pour la fièvre et hydratez-vous.'
        },
        {
            'name': 'Grippe',
            'description': 'Infection virale respiratoire contagieuse.',
            'first_aid': 'Reposez-vous, hydratez-vous, prenez du paracétamol pour la fièvre et les douleurs.'
        },
        {
            'name': 'Déshydratation',
            'description': 'Perte excessive d\'eau et de sels minéraux dans le corps.',
            'first_aid': 'Buvez régulièrement de petites quantités d\'eau ou de solutions de réhydratation.'
        },
        {
            'name': 'Gastro-entérite',
            'description': 'Inflammation de la muqueuse intestinale et gastrique.',
            'first_aid': 'Hydratez-vous, mangez léger, évitez les produits laitiers et les aliments épicés.'
        },
        {
            'name': 'Dengue',
            'description': 'Maladie virale transmise par les moustiques Aedes.',
            'first_aid': 'Consultez un médecin, prenez du paracétamol pour la fièvre, évitez l\'aspirine.'
        }
    ]
    
    for d in diseases:
        disease = Disease.query.filter_by(name=d['name']).first()
        if not disease:
            disease = Disease(name=d['name'], description=d['description'], first_aid=d['first_aid'])
            db.session.add(disease)
    
    db.session.commit()
    
    # Associations symptômes-maladies avec pondération
    disease_symptoms = [
        # Paludisme
        {'disease': 'Paludisme', 'symptom': 'Fièvre', 'weight': 2.0},
        {'disease': 'Paludisme', 'symptom': 'Maux de tête', 'weight': 1.5},
        {'disease': 'Paludisme', 'symptom': 'Frissons', 'weight': 1.8},
        {'disease': 'Paludisme', 'symptom': 'Sueurs nocturnes', 'weight': 1.7},
        {'disease': 'Paludisme', 'symptom': 'Fatigue', 'weight': 1.2},
        {'disease': 'Paludisme', 'symptom': 'Douleurs articulaires', 'weight': 1.0},
        
        # Grippe
        {'disease': 'Grippe', 'symptom': 'Fièvre', 'weight': 1.8},
        {'disease': 'Grippe', 'symptom': 'Maux de tête', 'weight': 1.2},
        {'disease': 'Grippe', 'symptom': 'Toux', 'weight': 2.0},
        {'disease': 'Grippe', 'symptom': 'Écoulement nasal', 'weight': 1.5},
        {'disease': 'Grippe', 'symptom': 'Maux de gorge', 'weight': 1.3},
        {'disease': 'Grippe', 'symptom': 'Fatigue', 'weight': 1.7},
        {'disease': 'Grippe', 'symptom': 'Courbatures', 'weight': 1.6},
        
        # Déshydratation
        {'disease': 'Déshydratation', 'symptom': 'Soif excessive', 'weight': 2.0},
        {'disease': 'Déshydratation', 'symptom': 'Urine foncée', 'weight': 1.8},
        {'disease': 'Déshydratation', 'symptom': 'Bouche sèche', 'weight': 1.7},
        {'disease': 'Déshydratation', 'symptom': 'Fatigue', 'weight': 1.2},
        {'disease': 'Déshydratation', 'symptom': 'Vertiges', 'weight': 1.5},
        
        # Gastro-entérite
        {'disease': 'Gastro-entérite', 'symptom': 'Nausées', 'weight': 1.8},
        {'disease': 'Gastro-entérite', 'symptom': 'Vomissements', 'weight': 2.0},
        {'disease': 'Gastro-entérite', 'symptom': 'Diarrhée', 'weight': 2.0},
        {'disease': 'Gastro-entérite', 'symptom': 'Douleurs abdominales', 'weight': 1.7},
        {'disease': 'Gastro-entérite', 'symptom': 'Fièvre', 'weight': 1.0},
        
        # Dengue
        {'disease': 'Dengue', 'symptom': 'Fièvre', 'weight': 2.0},
        {'disease': 'Dengue', 'symptom': 'Douleurs articulaires', 'weight': 1.9},
        {'disease': 'Dengue', 'symptom': 'Maux de tête', 'weight': 1.5},
        {'disease': 'Dengue', 'symptom': 'Éruption cutanée', 'weight': 1.8},
        {'disease': 'Dengue', 'symptom': 'Douleurs abdominales', 'weight': 1.2},
        {'disease': 'Dengue', 'symptom': 'Fatigue', 'weight': 1.4}
    ]
    
    for ds in disease_symptoms:
        disease = Disease.query.filter_by(name=ds['disease']).first()
        symptom = Symptom.query.filter_by(name=ds['symptom']).first()
        
        if disease and symptom:
            existing = DiseaseSymptom.query.filter_by(disease_id=disease.id, symptom_id=symptom.id).first()
            if not existing:
                association = DiseaseSymptom(disease_id=disease.id, symptom_id=symptom.id, weight=ds['weight'])
                db.session.add(association)
    
    # Créer les centres de santé
    health_centers = [
        {
            'name': 'Hôpital Central',
            'address': '123 Rue de la Santé',
            'latitude': 14.7167,
            'longitude': -17.4677,
            'phone': '+221 33 123 4567'
        },
        {
            'name': 'Clinique du Soleil',
            'address': '45 Avenue des Baobabs',
            'latitude': 14.7020,
            'longitude': -17.4800,
            'phone': '+221 33 234 5678'
        },
        {
            'name': 'Centre Médical de l\'Espoir',
            'address': '78 Boulevard de la Paix',
            'latitude': 14.7300,
            'longitude': -17.4500,
            'phone': '+221 33 345 6789'
        }
    ]
    
    for hc in health_centers:
        center = HealthCenter.query.filter_by(name=hc['name']).first()
        if not center:
            center = HealthCenter(
                name=hc['name'],
                address=hc['address'],
                latitude=hc['latitude'],
                longitude=hc['longitude'],
                phone=hc['phone']
            )
            db.session.add(center)
    
    db.session.commit()