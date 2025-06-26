# Dictionnaires de mapping entre valeurs textuelles et numériques

# Agglomération
AGGLOMERATION_MAP = {
    'En agglomération': 1,
    'Hors agglomération': 0
}

# Type de route
TYPE_ROUTE_MAP = {
    'A sens unique': 1,
    'Bidirectionnelle': 2,
    'A chaussées séparées': 3,
    'Avec voies d\'affectation variable': 4
}

# Conditions météo
METEO_MAP = {
    'Normale': 1,
    'Pluie légère': 2,
    'Pluie forte': 3,
    'Neige/Grêle': 4,
    'Brouillard/Fumée': 5,
    'Vent fort/Tempête': 6,
    'Temps éblouissant': 7,
    'Temps couvert': 8,
    'Autre': 9
}

# Luminosité
LUMINOSITE_MAP = {
    'Plein jour': 1,
    'Crépuscule ou aube': 2,
    'Nuit sans éclairage public': 3,
    'Nuit avec éclairage public non allumé': 4,
    'Nuit avec éclairage public allumé': 5
}

# Catégorie de véhicule
VEHICULE_MAP = {
    'Bicyclette': 1,
    'Cyclomoteur <50cm3': 2,
    'Voiturette': 4,
    'VL seul': 7,
    'VU seul 1,5T <= PTAC <= 3,5T': 10,
    'PL seul 3,5T <PTCA <= 7,5T': 13, 
    'PL seul > 7,5T': 14,
    'PL + remorque': 15,
    'Tracteur routier seul': 16,
    'Tracteur + semi-remorque': 17,
    'Scooter < 50 cm3': 30,
    'Motocyclette > 50 cm3 et <= 125 cm3': 31,
    'Scooter > 50 cm3 et <= 125 cm3': 32,
    'Motocyclette > 125 cm3': 33,
    'Scooter > 125 cm3': 34,
    'Quad léger <= 50 cm3': 35,
    'Quad lourd > 50 cm3': 36,
    'Autobus': 37,
    'Autocar': 38,
    'Train': 39,
    'Tramway': 40,
    'Engin spécial': 41,
    'Tracteur agricole': 42,
    'Vélo à assistance électrique': 80,
    'EDP à moteur': 50
}

# Type d'usager
USAGER_MAP = {
    'Conducteur': 1,
    'Passager': 2,
    'Piéton': 3
}

# Motif de déplacement
MOTIF_MAP = {
    'Non renseigné': 0,
    'Domicile – travail': 1,
    'Domicile – école': 2,
    'Courses – achats': 3,
    'Utilisation professionnelle': 4,
    'Promenade – loisirs': 5,
    'Autre': 9
}

# Équipement de sécurité
SECURITE_MAP = {
    'Non renseigné': -1,
    'Aucun équipement': 0,
    'Ceinture': 1,
    'Casque': 2,
    'Dispositif enfants': 3,
    'Gilet réfléchissant': 4,
    'Airbag': 5,
    'Gants': 6,
    'Gants + Vêtements motard': 7,
    'Autre': 9
}

# Place dans le véhicule
PLACE_MAP = {
    'Conducteur': 1,
    'Passager avant': 2,
    'Passager arrière': 3,
    'Passager': 4,
    'À l\'extérieur': 5,
    'Autre': 9
}

# Sexe
SEXE_MAP = {
    'Masculin': 1,
    'Féminin': 2
}

# Type de choc
CHOC_MAP = {
    'Aucun': 0,
    'Avant': 1,
    'Avant droit': 2,
    'Avant gauche': 3,
    'Arrière': 4,
    'Arrière droit': 5,
    'Arrière gauche': 6,
    'Côté droit': 7,
    'Côté gauche': 8,
    'Chocs multiples (tonneaux)': 9
}

# Manœuvre principale
MANOEUVRE_MAP = {
    'Inconnue': 0,
    'Sans changement de direction': 1,
    'Même sens, même file': 2,
    'Entre 2 files': 3,
    'En marche arrière': 4,
    'À contresens': 5,
    'En franchissant le terre-plein central': 6,
    'Dans le couloir bus, même sens': 7,
    'Dans le couloir bus, sens inverse': 8,
    'En s\'insérant': 9,
    'En faisant demi-tour': 10,
    'Changeant de file à gauche': 11,
    'Changeant de file à droite': 12,
    'Déporté à gauche': 13,
    'Déporté à droite': 14,
    'Tournant à gauche': 15,
    'Tournant à droite': 16,
    'Dépassant par la gauche': 17,
    'Dépassant par la droite': 18,
    'Traversant la chaussée': 19,
    'Manœuvre de stationnement': 20,
    'Manœuvre d\'évitement': 21,
    'Ouverture de porte': 22,
    'Arrêté (hors stationnement)': 23,
    'Autre': 24
}

# Type de moteur
MOTEUR_MAP = {
    'Inconnue': 0,
    'Hydrocarbures': 1,
    'Hybride électrique': 2,
    'Électrique': 3,
    'Hydrogène': 4,
    'Humaine': 5,
    'Autre': 6
}

def accident_to_prediction_format(accident):
    """
    Convertit un objet accident (dict) avec des valeurs textuelles en format numérique pour la prédiction
    """
    return {
        'dep': int(accident['lieu_departement']) if accident['lieu_departement'] and accident['lieu_departement'].isdigit() else 0,
        'agg': AGGLOMERATION_MAP.get(accident['agglomeration'], 1),
        'circ': TYPE_ROUTE_MAP.get(accident['type_route'], 1),
        'atm': METEO_MAP.get(accident['condition_meteo'], 1),
        'lum': LUMINOSITE_MAP.get(accident['luminosite'], 1),
        'catv': VEHICULE_MAP.get(accident['categorie_vehicule'], 7),
        'catu': USAGER_MAP.get(accident['categorie_usager'], 1),
        'age': int(accident['age']) if accident['age'] else 30,
        'trajet': MOTIF_MAP.get(accident['motif_deplacement'], 0),
        'secu1': SECURITE_MAP.get(accident['equipement_securite'], 0),
        'place': PLACE_MAP.get(accident['place_usager'], 1),
        'sexe': SEXE_MAP.get(accident['sexe_usager'], 1),
        'manv': MANOEUVRE_MAP.get(accident['manoeuvre_principal_accident'], 0),
        'motor': MOTEUR_MAP.get(accident['type_moteur'], 1),
        'vma': int(accident['vitesse_max']) if accident['vitesse_max'] else 50,
        'choc': CHOC_MAP.get(accident['point_choc_initial'], 0),
        'latitude': accident.get('lieu_latitude'),
        'longitude': accident.get('lieu_longitude')
    }

# Les mappings inverses (de numérique à textuel) sont utiles pour l'interface
AGGLOMERATION_REVERSE = {v: k for k, v in AGGLOMERATION_MAP.items()}
TYPE_ROUTE_REVERSE = {v: k for k, v in TYPE_ROUTE_MAP.items()}
METEO_REVERSE = {v: k for k, v in METEO_MAP.items()}
LUMINOSITE_REVERSE = {v: k for k, v in LUMINOSITE_MAP.items()}
VEHICULE_REVERSE = {v: k for k, v in VEHICULE_MAP.items()}
USAGER_REVERSE = {v: k for k, v in USAGER_MAP.items()}
MOTIF_REVERSE = {v: k for k, v in MOTIF_MAP.items()}
SECURITE_REVERSE = {v: k for k, v in SECURITE_MAP.items()}
PLACE_REVERSE = {v: k for k, v in PLACE_MAP.items()}
SEXE_REVERSE = {v: k for k, v in SEXE_MAP.items()}
CHOC_REVERSE = {v: k for k, v in CHOC_MAP.items()}
MANOEUVRE_REVERSE = {v: k for k, v in MANOEUVRE_MAP.items()}
MOTEUR_REVERSE = {v: k for k, v in MOTEUR_MAP.items()}

def prediction_to_accident_format(prediction):
    """
    Convertit un objet prédiction (dict) avec des valeurs numériques en format textuel pour l'affichage
    """
    return {
        'mois': datetime.now().month,  # Valeur par défaut
        'jour': datetime.now().day,    # Valeur par défaut
        'lieu_departement': str(prediction['dep']),
        'agglomeration': AGGLOMERATION_REVERSE.get(prediction['agg'], 'En agglomération'),
        'type_route': TYPE_ROUTE_REVERSE.get(prediction['circ'], 'A sens unique'),
        'condition_meteo': METEO_REVERSE.get(prediction['atm'], 'Normale'),
        'luminosite': LUMINOSITE_REVERSE.get(prediction['lum'], 'Plein jour'),
        'categorie_vehicule': VEHICULE_REVERSE.get(prediction['catv'], 'VL seul'),
        'categorie_usager': USAGER_REVERSE.get(prediction['catu'], 'Conducteur'),
        'age': prediction['age'],
        'motif_deplacement': MOTIF_REVERSE.get(prediction['trajet'], 'Non renseigné'),
        'equipement_securite': SECURITE_REVERSE.get(prediction['secu1'], 'Aucun équipement'),
        'place_usager': PLACE_REVERSE.get(prediction['place'], 'Conducteur'),
        'sexe_usager': SEXE_REVERSE.get(prediction['sexe'], 'Masculin'),
        'manoeuvre_principal_accident': MANOEUVRE_REVERSE.get(prediction['manv'], 'Inconnue'),
        'type_moteur': MOTEUR_REVERSE.get(prediction['motor'], 'Hydrocarbures'),
        'vitesse_max': prediction['vma'],
        'point_choc_initial': CHOC_REVERSE.get(prediction['choc'], 'Aucun'),
        'lieu_latitude': prediction.get('latitude'),
        'lieu_longitude': prediction.get('longitude'),
        'gravite_accident': prediction['severity']
    }