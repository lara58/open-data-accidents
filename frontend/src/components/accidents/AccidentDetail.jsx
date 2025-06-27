import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, Row, Col, Button, Alert, Container, Spinner } from 'react-bootstrap';
import { accidentService } from '../../services/accidentService';
import { authService } from '../../services/authService';
import { toast } from 'react-toastify';

// Définition des constantes manquantes
const CONDITIONS_METEO = [
  { value: 1, label: "Normale" },
  { value: 2, label: "Pluie légère" },
  { value: 3, label: "Pluie forte" },
  { value: 4, label: "Neige/grêle" },
  { value: 5, label: "Brouillard/fumée" },
  { value: 6, label: "Vent fort/tempête" },
  { value: 7, label: "Temps éblouissant" },
  { value: 8, label: "Temps couvert" },
  { value: 9, label: "Autre" }
];

const LUMINOSITE = [
  { value: 1, label: "Plein jour" },
  { value: 2, label: "Crépuscule ou aube" },
  { value: 3, label: "Nuit sans éclairage public" },
  { value: 4, label: "Nuit avec éclairage public non allumé" },
  { value: 5, label: "Nuit avec éclairage public allumé" }
];

const TYPE_ROUTE = [
  { value: 1, label: "Autoroute" },
  { value: 2, label: "Route nationale" },
  { value: 3, label: "Route départementale" },
  { value: 4, label: "Voie communale" },
  { value: 9, label: "Autre" }
];

const SEXE_USAGER = [
  { value: 1, label: "Homme" },
  { value: 2, label: "Femme" }
];

function AccidentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [accident, setAccident] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  
  useEffect(() => {
    // Récupérer l'utilisateur connecté
    const user = authService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
    
    const fetchAccident = async () => {
      try {
        const data = await accidentService.getAccidentById(id);
        setAccident(data);
        setLoading(false);
      } catch (err) {
        setError("Erreur lors du chargement des détails de l'accident");
        setLoading(false);
      }
    };
    
    fetchAccident();
  }, [id]);
  
  // Fonction pour vérifier si l'utilisateur est le créateur de l'accident
  const isAccidentCreator = () => {
    if (!currentUser || !accident) return false;
    console.log("Current user:", currentUser);
    console.log("Accident user_id:", accident.user_id);
    
    return parseInt(currentUser.id) === parseInt(accident.user_id);
  };
  
  const handleDelete = async () => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer cet accident ?")) {
      try {
        await accidentService.deleteAccident(id);
        toast.success("Accident supprimé avec succès");
        navigate('/accidents/user');
      } catch (err) {
        toast.error("Erreur lors de la suppression");
        console.error(err);
      }
    }
  };
  
  // Affiche un spinner pendant le chargement
  if (loading) {
    return <div className="text-center my-5"><Spinner animation="border" /></div>;
  }
  
  // Gestion des erreurs
  if (error) {
    return <Alert variant="danger" className="my-3">{error}</Alert>;
  }
  
  // Si pas d'accident trouvé
  if (!accident) {
    return <Alert variant="info" className="my-3">Aucun accident trouvé.</Alert>;
  }
  
  return (
    <Container>
      <Card className="shadow-sm my-4">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <h2>Détails de l'accident du {new Date(accident.date_accident).toLocaleDateString()}</h2>
          
          {/* Afficher les boutons seulement si l'utilisateur est le créateur */}
          {isAccidentCreator() && (
            <div>
              <Button as={Link} to={`/accidents/edit/${id}`} variant="warning" className="me-2">
                Modifier
              </Button>
              <Button variant="danger" onClick={handleDelete}>
                Supprimer
              </Button>
            </div>
          )}
        </Card.Header>
        
        <Card.Body>
          {/* Section pour afficher la gravité prédite */}
          <Card className={`mb-4 ${accident.gravite_accident === 'Grave' ? 'border-danger' : 'border-success'}`}>
            <Card.Header as="h6" 
              className={`${accident.gravite_accident === 'Grave' ? 'bg-danger text-white' : 'bg-success text-white'}`}>
              Prédiction de gravité
            </Card.Header>
            <Card.Body>
              <h4>{accident.gravite_accident}</h4>
              {accident.gravite_accident_proba && (
                <p className="mb-0">Probabilité: {accident.gravite_accident_proba}</p>
              )}
            </Card.Body>
          </Card>
          
          <Row>
            <Col md={6}>
              <h5>Informations générales</h5>
              <table className="table table-bordered">
                <tbody>
                  <tr>
                    <th>Date</th>
                    <td>{new Date(accident.date_accident).toLocaleDateString()}</td>
                  </tr>
                  {accident.heure_accident && (
                    <tr>
                      <th>Heure</th>
                      <td>{accident.heure_accident}</td>
                    </tr>
                  )}
                  <tr>
                    <th>Département</th>
                    <td>{accident.lieu_departement}</td>
                  </tr>
                  {accident.lieu_commune && (
                    <tr>
                      <th>Commune</th>
                      <td>{accident.lieu_commune}</td>
                    </tr>
                  )}
                  <tr>
                    <th>Agglomération</th>
                    <td>{accident.agglomeration === 1 ? 'En agglomération' : 'Hors agglomération'}</td>
                  </tr>
                </tbody>
              </table>
            </Col>
            
            <Col md={6}>
              <h5>Conditions de l'accident</h5>
              <table className="table table-bordered">
                <tbody>
                  <tr>
                    <th>Type de route</th>
                    <td>
                      {TYPE_ROUTE.find(t => t.value === accident.type_route)?.label || accident.type_route}
                    </td>
                  </tr>
                  <tr>
                    <th>Condition météo</th>
                    <td>
                      {CONDITIONS_METEO.find(c => c.value === accident.condition_meteo)?.label || accident.condition_meteo}
                    </td>
                  </tr>
                  <tr>
                    <th>Luminosité</th>
                    <td>
                      {LUMINOSITE.find(l => l.value === accident.luminosite)?.label || accident.luminosite}
                    </td>
                  </tr>
                  <tr>
                    <th>Vitesse maximale</th>
                    <td>{accident.vitesse_max} km/h</td>
                  </tr>
                </tbody>
              </table>
            </Col>
          </Row>
          
          <Row className="mt-4">
            <Col md={6}>
              <h5>Informations sur l'usager</h5>
              <table className="table table-bordered">
                <tbody>
                  <tr>
                    <th>Catégorie d'usager</th>
                    <td>{accident.categorie_usager}</td>
                  </tr>
                  <tr>
                    <th>Âge</th>
                    <td>{accident.age} ans</td>
                  </tr>
                  <tr>
                    <th>Sexe</th>
                    <td>
                      {SEXE_USAGER.find(s => s.value === accident.sexe_usager)?.label || accident.sexe_usager}
                    </td>
                  </tr>
                  <tr>
                    <th>Équipement de sécurité</th>
                    <td>{accident.equipement_securite}</td>
                  </tr>
                </tbody>
              </table>
            </Col>
            
            <Col md={6}>
              <h5>Informations sur le véhicule</h5>
              <table className="table table-bordered">
                <tbody>
                  <tr>
                    <th>Catégorie de véhicule</th>
                    <td>{accident.categorie_vehicule}</td>
                  </tr>
                  <tr>
                    <th>Type de moteur</th>
                    <td>{accident.type_moteur}</td>
                  </tr>
                  <tr>
                    <th>Manœuvre principale</th>
                    <td>{accident.manoeuvre_principal_accident}</td>
                  </tr>
                  <tr>
                    <th>Point de choc initial</th>
                    <td>{accident.point_choc_initial}</td>
                  </tr>
                </tbody>
              </table>
            </Col>
          </Row>
          
          {accident.description && (
            <div className="mt-4">
              <h5>Description</h5>
              <p className="border p-3 bg-light rounded">{accident.description}</p>
            </div>
          )}
        </Card.Body>
        
        <Card.Footer>
          <Link to="/accidents/user" className="btn btn-secondary">
            Retour à la liste
          </Link>
        </Card.Footer>
      </Card>
    </Container>
  );
}

export default AccidentDetail;