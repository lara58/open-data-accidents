import React, { useEffect, useState } from 'react';

function App() {
  const [accidents, setAccidents] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/accidents")
      .then(res => res.json())
      .then(data => setAccidents(data))
      .catch(err => console.error("Erreur API :", err));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>🚗 Liste des accidents (2023)</h1>
      {accidents.length === 0 ? (
        <p>Chargement des données...</p>
      ) : (
        <table border="1" cellPadding="8" style={{ borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Ville</th>
              <th>Gravité</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {accidents.map((accident, index) => (
              <tr key={index}>
                <td>{accident.id || accident.num_acc || index}</td>
                <td>{accident.ville || '-'}</td>
                <td>{accident.gravite || '-'}</td>
                <td>{accident.date || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
