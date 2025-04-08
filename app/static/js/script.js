// Script principal pour DiagMedic

// Fonction pour rendre les liens externes sécurisés
document.addEventListener('DOMContentLoaded', function() {
    // Sécuriser tous les liens externes
    const externalLinks = document.querySelectorAll('a[target="_blank"]');
    externalLinks.forEach(function(link) {
        link.setAttribute('rel', 'noopener noreferrer');
    });
    
    // Mise en évidence des éléments de liste dans les symptômes
    const symptomItems = document.querySelectorAll('.symptom-tag');
    symptomItems.forEach(function(item) {
        item.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#dee2e6';
        });
        item.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#e9ecef';
        });
    });
});