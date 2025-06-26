import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PredictionHistory.css';

const PredictionHistory = (props) => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const loadPredictions = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Essayer d'abord avec l'endpoint normal
      try {
        const response = await axios.get(`${props.apiUrl}/predictions`, {
          timeout: 5000
        });
        
        setPredictions(response.data || []);
      } catch (err) {
        console.log("Erreur avec l'endpoint principal, essai avec les données de démonstration");
        // Si l'endpoint normal échoue, essayer avec les données de démonstration
        const mockResponse = await axios.get('http://localhost:5000/mock-predictions', {
          timeout: 3000
        });
        
        setPredictions(mockResponse.data || []);
      }
    } catch (err) {
      console.error('Erreur:', err);
      let errorMessage = "Erreur lors du chargement de l'historique des prédictions";
      
      if (err.response) {
        errorMessage += ` (${err.response.status}: ${err.response.statusText})`;
        if (err.response.data && err.response.data.error) {
          errorMessage += ` - ${err.response.data.error}`;
        }
      } else if (err.request) {
        errorMessage = "Le serveur n'a pas répondu. Vérifiez que le backend est bien en cours d'exécution.";
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadPredictions();
  }, []);
  
  // Formatage de la date
  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('fr-FR');
    } catch (e) {
      return dateString;
    }
  };

  // Traduire les valeurs numériques en libellés compréhensibles
  const getTrajetLabel = (trajet) => {
    const labels = {
      0: 'Domicile-travail', 
      1: 'Domicile-école', 
      2: 'Course-achats', 
      3: 'Professionnel',
      4: 'Promenade-loisirs', 
      9: 'Autre'
    };
    return labels[trajet] || trajet;
  };

  const getCatvLabel = (catv) => {
    const labels = {
      7: 'VL', 
      33: 'PL', 
      2: '2 roues motorisé',
      1: 'Vélo',
      4: 'Piéton'
    };
    return labels[catv] || catv;
  };
  
  return (
    <div className="prediction-history">
      <h2>Historique des prédictions</h2>
      
      {loading && <p className="loading">Chargement de l'historique...</p>}
      
      {error && (
        <div className="error-container">
          <p>Erreur lors du chargement de l'historique des prédictions</p>
          <p className="error-details">{error}</p>
          <button className="retry-button" onClick={loadPredictions}>
            Réessayer
          </button>
        </div>
      )}
      
      {!loading && !error && predictions.length === 0 && (
        <p>Aucune prédiction enregistrée</p>
      )}
      
      {!loading && !error && predictions.length > 0 && (
        <table className="prediction-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Profil</th>
              <th>Véhicule</th>
              <th>Conditions</th>
              <th>Résultat</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map(pred => (
              <tr key={pred.id} className={pred.severity === 'Grave' ? 'grave' : 'leger'}>
                <td>{formatDate(pred.date_prediction)}</td>
                <td>
                  {pred.sexe === 1 ? 'Homme' : 'Femme'}, {pred.age} ans<br/>
                  Trajet: {getTrajetLabel(pred.trajet)}<br/>
                  Dépt: {pred.dep}
                </td>
                <td>
                  Type: {getCatvLabel(pred.catv)}<br/>
                  Place: {pred.place === 1 ? 'Conducteur' : 'Passager'}
                </td>
                <td>
                  {pred.agg === 1 ? 'En agglo' : 'Hors agglo'}<br/>
                  {pred.lum === 1 ? 'Jour' : 'Nuit'}<br/>
                  VMA: {pred.vma} km/h
                </td>
                <td className={pred.severity === 'Grave' ? 'result-severe' : 'result-light'}>
                  <strong>{pred.severity}</strong><br/>
                  <span className="probability">{Math.round(pred.probability * 100)}%</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default PredictionHistory;