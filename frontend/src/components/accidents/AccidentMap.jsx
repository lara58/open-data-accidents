// src/components/accidents/AccidentMap.jsx
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Correction de l'icône par défaut de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Coordonnées approximatives des départements français
const DEPARTEMENTS_COORDS = {
  '1': [46.1324, 5.3497], // Ain
  '2': [49.5603, 3.6095], // Aisne
  '3': [46.3051, 3.4157], // Allier
  '4': [44.0778, 6.2375], // Alpes-de-Haute-Provence
  '5': [44.6568, 6.0830], // Hautes-Alpes
  '6': [43.9424, 7.0237], // Alpes-Maritimes
  '7': [44.7354, 4.5986], // Ardèche
  '8': [49.5134, 4.6791], // Ardennes
  '9': [42.9320, 1.4436], // Ariège
  '10': [48.3417, 4.1746], // Aube
  '11': [43.0667, 2.3500], // Aude
  '12': [44.3500, 2.5833], // Aveyron
  '13': [43.5333, 5.4333], // Bouches-du-Rhône
  '14': [49.1833, -0.3500], // Calvados
  '15': [45.0333, 2.6667], // Cantal
  '16': [45.7500, 0.3333], // Charente
  '17': [45.8333, -0.6667], // Charente-Maritime
  '18': [47.0833, 2.5000], // Cher
  '19': [45.2667, 1.7667], // Corrèze
  '20': [42.1500, 9.1500], // Corse
  '21': [47.3167, 5.0167], // Côte-d'Or
  '22': [48.5000, -2.7500], // Côtes-d'Armor
  '23': [46.0667, 2.0500], // Creuse
  '24': [45.0000, 0.7500], // Dordogne
  '25': [47.0000, 6.5000], // Doubs
  '26': [44.7500, 5.0000], // Drôme
  '27': [49.0500, 1.1667], // Eure
  '28': [48.4333, 1.5000], // Eure-et-Loir
  '29': [48.0000, -4.0000], // Finistère
  '30': [43.9946, 4.1630], // Gard
  '31': [43.6000, 1.4333], // Haute-Garonne
  '32': [43.6500, 0.5833], // Gers
  '33': [44.8333, -0.5667], // Gironde
  '34': [43.6167, 3.8833], // Hérault
  '35': [48.1667, -1.6667], // Ille-et-Vilaine
  '36': [46.8167, 1.7167], // Indre
  '37': [47.3833, 0.7000], // Indre-et-Loire
  '38': [45.1667, 5.7167], // Isère
  '39': [46.6728, 5.5592], // Jura
  '40': [43.8953, -0.5003], // Landes
  '41': [47.5833, 1.3333], // Loir-et-Cher
  '42': [45.7333, 4.2500], // Loire
  '43': [45.0333, 3.8833], // Haute-Loire
  '44': [47.2500, -1.5833], // Loire-Atlantique
  '45': [47.9000, 2.2000], // Loiret
  '46': [44.6000, 1.7500], // Lot
  '47': [44.3833, 0.5000], // Lot-et-Garonne
  '48': [44.5000, 3.5000], // Lozère
  '49': [47.4667, -0.5500], // Maine-et-Loire
  '50': [49.0500, -1.2500], // Manche
  '51': [49.0000, 4.0000], // Marne
  '52': [48.0000, 5.0000], // Haute-Marne
  '53': [48.0667, -0.7667], // Mayenne
  '54': [48.6833, 6.2000], // Meurthe-et-Moselle
  '55': [49.0000, 5.3333], // Meuse
  '56': [47.7500, -2.7500], // Morbihan
  '57': [49.1333, 6.1667], // Moselle
  '58': [47.0833, 3.5000], // Nièvre
  '59': [50.6333, 3.0667], // Nord
  '60': [49.4167, 2.4167], // Oise
  '61': [48.5833, 0.0833], // Orne
  '62': [50.4500, 2.7333], // Pas-de-Calais
  '63': [45.7667, 3.0833], // Puy-de-Dôme
  '64': [43.3000, -0.3667], // Pyrénées-Atlantiques
  '65': [43.0167, 0.1500], // Hautes-Pyrénées
  '66': [42.6000, 2.9000], // Pyrénées-Orientales
  '67': [48.5833, 7.7500], // Bas-Rhin
  '68': [47.7500, 7.3333], // Haut-Rhin
  '69': [45.7500, 4.8500], // Rhône
  '70': [47.6333, 6.0833], // Haute-Saône
  '71': [46.5000, 4.5000], // Saône-et-Loire
  '72': [48.0000, 0.2000], // Sarthe
  '73': [45.5667, 6.3000], // Savoie
  '74': [46.0000, 6.3333], // Haute-Savoie
  '75': [48.8566, 2.3522], // Paris
  '76': [49.4428, 1.0939], // Seine-Maritime
  '77': [48.6272, 2.9676], // Seine-et-Marne
  '78': [48.8043, 1.9722], // Yvelines
  '79': [46.5000, -0.3333], // Deux-Sèvres
  '80': [49.9000, 2.3000], // Somme
  '81': [43.9333, 2.1500], // Tarn
  '82': [44.0167, 1.3500], // Tarn-et-Garonne
  '83': [43.4167, 6.2667], // Var
  '84': [44.0500, 5.0500], // Vaucluse
  '85': [46.6667, -1.4333], // Vendée
  '86': [46.5833, 0.3333], // Vienne
  '87': [45.8333, 1.2500], // Haute-Vienne
  '88': [48.1667, 6.4500], // Vosges
  '89': [47.7992, 3.5667], // Yonne
  '90': [47.6333, 6.8667], // Territoire de Belfort
  '91': [48.5333, 2.2667], // Essonne
  '92': [48.8333, 2.2000], // Hauts-de-Seine
  '93': [48.9167, 2.4833], // Seine-Saint-Denis
  '94': [48.7833, 2.4667], // Val-de-Marne
  '95': [49.0809, 2.1301]  // Val-d'Oise
};

const AccidentMap = ({ accidents }) => {
  // Position centrée sur la France
  const center = [46.603354, 1.888334]; 
  const zoom = 6;

  // Fonction pour obtenir les coordonnées à partir du département
  const getCoordinates = (departement) => {
    const deptCode = departement.toString();
    return DEPARTEMENTS_COORDS[deptCode] || center;
  };

  return (
    <div className="mb-4">
      <h4 className="mb-3">Carte des accidents</h4>
      <div style={{ height: '500px', width: '100%' }}>
        <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {accidents.map(accident => (
            <Marker 
              key={accident.id} 
              position={getCoordinates(accident.lieu_departement)}
            >
              <Popup>
                <div>
                  <h6>Accident du {new Date(accident.date_accident).toLocaleDateString()}</h6>
                  <p>Département: {accident.lieu_departement}</p>
                  <p>Gravité: {accident.gravite_accident}</p>
                  <a href={`/accidents/${accident.id}`}>Voir les détails</a>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default AccidentMap;