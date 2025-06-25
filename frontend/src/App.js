import React, { useState, useEffect } from 'react';
import './App.css';
import AccidentMap from './components/AccidentMap';
import AccidentForm from './components/AccidentForm';
import PredictionHistory from './components/PredictionHistory';
import axios from 'axios';

function App() {
  const [accidents, setAccidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('map'); // 'map' ou 'predict' ou 'history'

  useEffect(() => {
    axios.get('http://localhost:5000/mock-predictions')  // ou le bon endpoint qui existe
      .then(res => {
        setAccidents(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Erreur API :", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="App">
      <h1>Analyse des accidents de la route</h1>
      
      <div className="tabs">
        <button 
          className={`tab-btn ${activeTab === 'map' ? 'active' : ''}`}
          onClick={() => setActiveTab('map')}
        >
          Carte des accidents
        </button>
        <button 
          className={`tab-btn ${activeTab === 'predict' ? 'active' : ''}`}
          onClick={() => setActiveTab('predict')}
        >
          Prédiction de gravité
        </button>
        <button 
          className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Historique des prédictions
        </button>
      </div>

      <div className="content-container">
        {activeTab === 'map' ? (
          loading ? (
            <p className="loading">Chargement des données...</p>
          ) : (
            <AccidentMap accidents={accidents} />
          )
        ) : activeTab === 'predict' ? (
          <AccidentForm />
        ) : (
          <PredictionHistory />
        )}
      </div>
    </div>
  );
}

export default App;
