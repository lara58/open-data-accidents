import React, { useState } from 'react';
import axios from 'axios';
import './AccidentForm.css';

const AccidentForm = (props) => {
  // 1. Modifier les valeurs par défaut pour qu'elles correspondent aux options disponibles
  const [formData, setFormData] = useState({
    // Champs obligatoires pour la prédiction
    dep: '75', // département (numérique)
    agg: '1', // agglomération (1 = En agglomération, 0 = Hors agglomération)
    circ: '1', // type de route (numérique)
    atm: '1', // condition météo (numérique)
    lum: '1', // luminosité (numérique)
    catv: '7', // catégorie de véhicule (numérique)
    catu: '1', // catégorie d'usager (numérique)
    age: '30', // âge (numérique)
    trajet: '0', // motif déplacement (numérique)
    secu1: '1', // équipement sécurité (numérique)
    place: '1', // place usager (numérique)
    sexe: '1', // sexe (1 = Homme, 2 = Femme)
    manv: '1', // manœuvre principale (numérique)
    motor: '1', // type de moteur (numérique)
    vma: '50', // vitesse maximale autorisée (numérique)
    choc: '1', // point de choc initial (numérique)
    
    // Champs facultatifs pour enregistrement plus complet
    mois: new Date().getMonth() + 1, // Mois actuel (1-12)
    jour: new Date().getDate(), // Jour actuel (1-31)
    lieu_commune: '',
    description: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Conversion des données
      const dataToSend = {
        ...formData,
        dep: parseInt(formData.dep) || 0, // Ajouter une valeur par défaut
        age: parseInt(formData.age),
        agg: parseInt(formData.agg),
        circ: parseInt(formData.circ),
        atm: parseInt(formData.atm),
        lum: parseInt(formData.lum),
        catv: parseInt(formData.catv),
        place: parseInt(formData.place),
        sexe: parseInt(formData.sexe),
        manv: parseInt(formData.manv),
        motor: parseInt(formData.motor),
        vma: parseInt(formData.vma),
        choc: parseInt(formData.choc),
        trajet: parseInt(formData.trajet),
        secu1: parseInt(formData.secu1),
        catu: parseInt(formData.catu),
        mois: parseInt(formData.mois),
        jour: parseInt(formData.jour),
      };

      console.log("Données envoyées pour prédiction:", dataToSend);
      
      // Utiliser l'URL de l'API correcte
      const response = await axios.post(`${props.apiUrl}/predictions`, dataToSend, {
        timeout: 10000 // 10 secondes
      });
      
      console.log("Réponse reçue:", response.data);
      setResult(response.data);
      
    } catch (err) {
      console.error('Erreur lors de la prédiction:', err);
      
      let errorMessage = "Erreur lors de la prédiction";
      
      if (err.response) {
        if (err.response.data && err.response.data.error) {
          errorMessage = err.response.data.error;
        } else {
          errorMessage = `Erreur ${err.response.status}: ${err.response.statusText}`;
        }
      } else if (err.request) {
        errorMessage = "Le serveur n'a pas répondu. Vérifiez que le backend est en cours d'exécution.";
      } else if (err.code === 'ECONNABORTED') {
        errorMessage = "La requête a pris trop de temps. Le serveur peut être surchargé.";
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="accident-form-container">
      <h2>Prédiction de gravité d'accident</h2>
      
      <form onSubmit={handleSubmit} className="accident-form">
        <div className="form-group">
          <h3>Informations personnelles</h3>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="sexe">Sexe</label>
              <select
                id="sexe"
                name="sexe"
                value={formData.sexe}
                onChange={handleChange}
                required
              >
                <option value="1">Homme</option>
                <option value="2">Femme</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="age">Âge</label>
              <input
                id="age"
                name="age"
                type="number"
                min="1"
                max="120"
                value={formData.age}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="place">Place dans le véhicule</label>
              <select
                id="place"
                name="place"
                value={formData.place}
                onChange={handleChange}
                required
              >
                <option value="1">Conducteur</option>
                <option value="2">Passager avant</option>
                <option value="3">Passager arrière</option>
                <option value="10">Piéton</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="secu1">Équipement de sécurité</label>
              <select
                id="secu1"
                name="secu1"
                value={formData.secu1}
                onChange={handleChange}
                required
              >
                <option value="0">Aucun équipement</option>
                <option value="1">Ceinture</option>
                <option value="2">Casque</option>
                <option value="3">Dispositif enfants</option>
                <option value="4">Gilet réfléchissant</option>
                <option value="9">Autre</option>
              </select>
            </div>
          </div>
          
          <div className="form-field">
            <label htmlFor="trajet">Motif du déplacement</label>
            <select
              id="trajet"
              name="trajet"
              value={formData.trajet}
              onChange={handleChange}
              required
            >
              <option value="0">Non renseigné</option>
              <option value="1">Domicile-travail</option>
              <option value="2">Domicile-école</option>
              <option value="3">Courses-achats</option>
              <option value="4">Utilisation professionnelle</option>
              <option value="5">Promenade-loisirs</option>
              <option value="9">Autre</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <h3>Véhicule</h3>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="catv">Type de véhicule</label>
              <select
                id="catv"
                name="catv"
                value={formData.catv}
                onChange={handleChange}
                required
              >
                <option value="7">Voiture (VL seul)</option>
                <option value="10">VU seul (&lt;=3,5T)</option>
                <option value="14">PL seul (&gt;7,5T)</option>
                <option value="33">Motocyclette &gt;125cm3</option>
                <option value="31">Motocyclette &gt;50cm3 et &lt;=125cm3</option>
                <option value="30">Scooter &lt;50cm3</option>
                <option value="1">Bicyclette</option>
                <option value="80">Vélo à assistance électrique (VAE)</option>
                <option value="4">Piéton</option>
                <option value="37">Autobus</option>
                <option value="38">Autocar</option>
                <option value="50">EDP à moteur</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="catu">Catégorie d'usager</label>
              <select
                id="catu"
                name="catu"
                value={formData.catu}
                onChange={handleChange}
                required
              >
                <option value="1">Conducteur</option>
                <option value="2">Passager</option>
                <option value="3">Piéton</option>
              </select>
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="motor">Type de motorisation</label>
              <select
                id="motor"
                name="motor"
                value={formData.motor}
                onChange={handleChange}
                required
              >
                <option value="0">Inconnue</option>
                <option value="1">Hydrocarbures</option>
                <option value="2">Hybride électrique</option>
                <option value="3">Électrique</option>
                <option value="4">Hydrogène</option>
                <option value="5">Humaine</option>
                <option value="6">Autre</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="manv">Manœuvre avant l'accident</label>
              <select
                id="manv"
                name="manv"
                value={formData.manv}
                onChange={handleChange}
                required
              >
                <option value="0">Inconnue</option>
                <option value="1">Sans changement de direction</option>
                <option value="2">Même sens, même file</option>
                <option value="15">Tournant à gauche</option>
                <option value="16">Tournant à droite</option>
                <option value="20">Manœuvre de stationnement</option>
                <option value="23">Arrêté (hors stationnement)</option>
              </select>
            </div>
          </div>
        </div>
        
        <div className="form-group">
          <h3>Conditions de l'accident</h3>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="mois">Mois</label>
              <input
                id="mois"
                name="mois"
                type="number"
                min="1"
                max="12"
                value={formData.mois}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-field">
              <label htmlFor="jour">Jour</label>
              <input
                id="jour"
                name="jour"
                type="number"
                min="1"
                max="31"
                value={formData.jour}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-field">
              <label htmlFor="dep">Département</label>
              <input
                id="dep"
                name="dep"
                type="text"
                maxLength="3"
                value={formData.dep}
                onChange={handleChange}
                required
                placeholder="ex: 75"
              />
            </div>
            
            <div className="form-field">
              <label htmlFor="agg">Agglomération</label>
              <select
                id="agg"
                name="agg"
                value={formData.agg}
                onChange={handleChange}
                required
              >
                <option value="1">En agglomération</option>
                <option value="0">Hors agglomération</option>
              </select>
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="lum">Luminosité</label>
              <select
                id="lum"
                name="lum"
                value={formData.lum}
                onChange={handleChange}
                required
              >
                <option value="1">Plein jour</option>
                <option value="2">Crépuscule ou aube</option>
                <option value="3">Nuit sans éclairage public</option>
                <option value="4">Nuit avec éclairage public non allumé</option>
                <option value="5">Nuit avec éclairage public allumé</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="atm">Conditions météo</label>
              <select
                id="atm"
                name="atm"
                value={formData.atm}
                onChange={handleChange}
                required
              >
                <option value="1">Normale</option>
                <option value="2">Pluie légère</option>
                <option value="3">Pluie forte</option>
                <option value="4">Neige/Grêle</option>
                <option value="5">Brouillard/Fumée</option>
                <option value="6">Vent fort/Tempête</option>
                <option value="7">Temps éblouissant</option>
                <option value="8">Temps couvert</option>
                <option value="9">Autre</option>
              </select>
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-field">
              <label htmlFor="circ">Type de route</label>
              <select
                id="circ"
                name="circ"
                value={formData.circ}
                onChange={handleChange}
                required
              >
                <option value="1">À sens unique</option>
                <option value="2">Bidirectionnelle</option>
                <option value="3">À chaussées séparées</option>
                <option value="4">Avec voies d'affectation variable</option>
              </select>
            </div>
            
            <div className="form-field">
              <label htmlFor="vma">Vitesse max autorisée (km/h)</label>
              <select
                id="vma"
                name="vma"
                value={formData.vma}
                onChange={handleChange}
                required
              >
                <option value="30">30 km/h</option>
                <option value="50">50 km/h</option>
                <option value="70">70 km/h</option>
                <option value="80">80 km/h</option>
                <option value="90">90 km/h</option>
                <option value="110">110 km/h</option>
                <option value="130">130 km/h</option>
              </select>
            </div>
          </div>
          
          <div className="form-field">
            <label htmlFor="choc">Point de choc initial</label>
            <select
              id="choc"
              name="choc"
              value={formData.choc}
              onChange={handleChange}
              required
            >
              <option value="0">Aucun</option>
              <option value="1">Avant</option>
              <option value="2">Avant droit</option>
              <option value="3">Avant gauche</option>
              <option value="4">Arrière</option>
              <option value="5">Arrière droit</option>
              <option value="6">Arrière gauche</option>
              <option value="7">Côté droit</option>
              <option value="8">Côté gauche</option>
              <option value="9">Chocs multiples (tonneaux)</option>
            </select>
          </div>
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Prédiction en cours...' : 'Prédire la gravité'}
          </button>
        </div>
      </form>
      
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}
      
      {result && !error && (
        <div className={`prediction-result ${result.severity === 'Grave' ? 'severe' : 'light'}`}>
          <h3>Résultat de la prédiction</h3>
          <p className="prediction">
            <strong>Gravité prédite:</strong> <span className="severity">{result.severity}</span>
          </p>
          <p className="probability">
            <strong>Probabilité:</strong> {Math.round(result.probability * 100)}%
          </p>
        </div>
      )}
    </div>
  );
};

export default AccidentForm;