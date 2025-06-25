# services/predictor.py

# Fonction temporaire de prédiction
def predire_gravite(data):
    # future: appel d'un modèle ML
    if data["vitesse_max"] > 70 or data["agglomeration"] == 0:
        return 1
    return 0
