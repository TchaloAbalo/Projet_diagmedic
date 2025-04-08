import folium
from app.models import HealthCenter
from geopy.distance import geodesic
from typing import Tuple

def create_map(latitude: float, longitude: float, health_centers: list) -> str:
    """
    Crée une carte avec les centres de santé à proximité.
    
    Args:
        latitude: Latitude de l'utilisateur
        longitude: Longitude de l'utilisateur
        health_centers: Liste des centres de santé à afficher
        
    Returns:
        HTML de la carte
    """
    # Créer une carte centrée sur la position de l'utilisateur
    map_center = [latitude, longitude] if latitude and longitude else [14.7167, -17.4677]  # Dakar par défaut
    m = folium.Map(location=map_center, zoom_start=13)
    
    # Ajouter un marqueur pour la position de l'utilisateur
    if latitude and longitude:
        folium.Marker(
            location=[latitude, longitude],
            popup='Votre position',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    # Ajouter les centres de santé sur la carte
    for center in health_centers:
        folium.Marker(
            location=[center.latitude, center.longitude],
            popup=f"<b>{center.name}</b><br>{center.address}<br>Tél: {center.phone}<br><a href='https://www.google.com/maps/dir/?api=1&destination={center.latitude},{center.longitude}' target='_blank'>Itinéraire</a>",
            icon=folium.Icon(color='green', icon='plus')
        ).add_to(m)
    
    return m._repr_html_()

def find_nearby_centers(latitude: float, longitude: float, max_distance: float = 10.0) -> list:
    """
    Trouve les centres de santé à proximité d'une position donnée.
    
    Args:
        latitude: Latitude de l'utilisateur
        longitude: Longitude de l'utilisateur
        max_distance: Distance maximale en km
        
    Returns:
        Liste des centres de santé triés par distance
    """
    if not latitude or not longitude:
        return HealthCenter.query.all()
    
    user_location = (latitude, longitude)
    centers = HealthCenter.query.all()
    centers_with_distance = []
    
    for center in centers:
        center_location = (center.latitude, center.longitude)
        distance = geodesic(user_location, center_location).kilometers
        centers_with_distance.append((center, distance))
    
    # Trier par distance
    centers_with_distance.sort(key=lambda x: x[1])
    
    # Filtrer par distance maximale
    nearby_centers = [c[0] for c in centers_with_distance if c[1] <= max_distance]
    
    return nearby_centers or [c[0] for c in centers_with_distance[:3]]  # Retourner au moins 3 centres