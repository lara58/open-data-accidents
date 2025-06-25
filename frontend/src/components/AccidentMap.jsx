import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './AccidentMap.css';

// Correction pour les icônes Leaflet qui ne s'affichent pas correctement
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

const AccidentMap = ({ accidents }) => {
  const [mapAccidents, setMapAccidents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Ajouter des coordonnées GPS si elles n'existent pas
    if (accidents && accidents.length > 0) {
      const accidentsWithCoordinates = accidents.map((accident, index) => {
        // Si les coordonnées existent déjà et sont valides, les utiliser
        if (accident.latitude && accident.longitude && 
            !isNaN(parseFloat(accident.latitude)) && 
            !isNaN(parseFloat(accident.longitude))) {
          return accident;
        } 
        
        // Sinon, générer des coordonnées basées sur le département
        // Paris (centre de la France) comme point de départ
        const baseLat = 48.856614;
        const baseLng = 2.3522219;
        
        // Créer un décalage basé sur l'ID ou département pour disperser les points
        const dep = parseInt(accident.dep) || 75;
        const latOffset = ((dep - 75) * 0.05) + (Math.random() * 0.02);
        const lngOffset = ((dep - 75) * 0.05) + (Math.random() * 0.02);
        
        return {
          ...accident,
          latitude: baseLat + latOffset,
          longitude: baseLng + lngOffset
        };
      });
      
      setMapAccidents(accidentsWithCoordinates);
    } else {
      setMapAccidents([]);
    }
    
    setIsLoading(false);
  }, [accidents]);
  
  // Calculer le centre de la carte
  const getMapCenter = () => {
    // Utiliser Paris comme centre par défaut
    return [48.856614, 2.3522219];
  };

  // Afficher un message de chargement si nécessaire
  if (isLoading) {
    return <div className="loading-container">Chargement de la carte...</div>;
  }
  
  // Afficher un message si pas d'accidents
  if (mapAccidents.length === 0) {
    return <div className="no-data">Aucun accident à afficher sur la carte</div>;
  }
  
  return (
    <div className="map-container">
      <MapContainer 
        center={getMapCenter()} 
        zoom={6} 
        style={{ height: '600px', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {mapAccidents.map((accident) => (
          <Marker 
            key={accident.id} 
            position={[
              parseFloat(accident.latitude),
              parseFloat(accident.longitude)
            ]}
          >
            <Popup>
              <div className="accident-popup">
                <h3 className={accident.severity === 'Grave' ? 'severe' : 'light'}>
                  Accident {accident.severity}
                </h3>
                <p><strong>Département:</strong> {accident.dep}</p>
                <p><strong>Véhicule:</strong> {accident.catv}</p>
                <p><strong>Conditions:</strong> {accident.atm === 1 ? 'Normales' : 'Dégradées'}</p>
                <p><strong>Probabilité:</strong> {Math.round(accident.probability * 100)}%</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default AccidentMap;