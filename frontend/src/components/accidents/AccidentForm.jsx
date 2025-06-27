// src/components/accidents/AccidentForm.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import { accidentService } from '../../services/accidentService';
import { toast } from 'react-toastify';

// Constantes existantes
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

const MANOEUVRE_PRINCIPALE = [
  { value: -1, label: "Non renseigné" },
  { value: 0, label: "Inconnue" },
  // Sans changement de direction
  { value: 1, label: "Sans changement de direction" },
  { value: 2, label: "Même sens, même file" },
  { value: 3, label: "Entre 2 files" },
  { value: 4, label: "En marche arrière" },
  { value: 5, label: "A contresens" },
  { value: 6, label: "En franchissant le terre-plein central" },
  { value: 7, label: "Dans le couloir bus, dans le même sens" },
  { value: 8, label: "Dans le couloir bus, dans le sens inverse" },
  { value: 9, label: "En s'insérant" },
  { value: 10, label: "En faisant demi-tour sur la chaussée" },
  // Changeant de file
  { value: 11, label: "Changeant de file - A gauche" },
  { value: 12, label: "Changeant de file - A droite" },
  // Déporté
  { value: 13, label: "Déporté - A gauche" },
  { value: 14, label: "Déporté - A droite" },
  // Tournant
  { value: 15, label: "Tournant - A gauche" },
  { value: 16, label: "Tournant - A droite" },
  // Dépassant
  { value: 17, label: "Dépassant - A gauche" },
  { value: 18, label: "Dépassant - A droite" },
  // Divers
  { value: 19, label: "Traversant la chaussée" },
  { value: 20, label: "Manœuvre de stationnement" },
  { value: 21, label: "Manœuvre d'évitement" },
  { value: 22, label: "Ouverture de porte" },
  { value: 23, label: "Arrêté (hors stationnement)" },
  { value: 24, label: "En stationnement (avec occupants)" },
  { value: 25, label: "Circulant sur trottoir" },
  { value: 26, label: "Autres manœuvres" }
];

// Nouvelles constantes
const TYPE_ROUTE = [
  { value: 1, label: "Autoroute" },
  { value: 2, label: "Route nationale" },
  { value: 3, label: "Route départementale" },
  { value: 4, label: "Voie communale" },
  { value: 5, label: "Voie privée ouverte à la circulation" },
  { value: 6, label: "Parking ouvert à la circulation" },
  { value: 7, label: "Piste cyclable" },
  { value: 9, label: "Autre" }
];

const CATEGORIE_VEHICULE = [
  { value: 1, label: "Véhicule léger" },
  { value: 2, label: "Véhicule utilitaire" },
  { value: 3, label: "Poids lourd" },
  { value: 4, label: "Deux-roues motorisé" },
  { value: 5, label: "Vélo" },
  { value: 6, label: "Transport en commun" },
  { value: 7, label: "Autre" }
];

const CATEGORIE_USAGER = [
  { value: 1, label: "Conducteur" },
  { value: 2, label: "Passager" },
  { value: 3, label: "Piéton" }
];

const MOTIF_DEPLACEMENT = [
  { value: -1, label: "Non renseigné" },
  { value: 0, label: "Non renseigné" },
  { value: 1, label: "Domicile - travail" },
  { value: 2, label: "Domicile - école" },
  { value: 3, label: "Courses - achats" },
  { value: 4, label: "Utilisation professionnelle" },
  { value: 5, label: "Promenade - loisirs" },
  { value: 9, label: "Autre" }
];

const EQUIPEMENT_SECURITE = [
  { value: -1, label: "Non renseigné" },
  { value: 0, label: "Aucun équipement" },
  { value: 1, label: "Ceinture" },
  { value: 2, label: "Casque" },
  { value: 3, label: "Dispositif enfants" },
  { value: 4, label: "Gilet réfléchissant" },
  { value: 5, label: "Airbag (2RM/3RM)" },
  { value: 6, label: "Gants (2RM/3RM)" },
  { value: 7, label: "Gants + Airbag (2RM/3RM)" },
  { value: 8, label: "Non déterminable" },
  { value: 9, label: "Autre" }
];

const PLACE_USAGER = [
  { value: 1, label: "Conducteur" },
  { value: 2, label: "Passager avant" },
  { value: 3, label: "Passager arrière" },
  { value: 9, label: "Autre" }
];

const TYPE_MOTEUR = [
  { value: 1, label: "Essence" },
  { value: 2, label: "Diesel" },
  { value: 3, label: "Électrique" },
  { value: 4, label: "Hybride" },
  { value: 9, label: "Autre" }
];

const POINT_CHOC_INITIAL = [
  { value: 1, label: "Avant" },
  { value: 2, label: "Avant droit" },
  { value: 3, label: "Avant gauche" },
  { value: 4, label: "Arrière" },
  { value: 5, label: "Arrière droit" },
  { value: 6, label: "Arrière gauche" },
  { value: 7, label: "Côté droit" },
  { value: 8, label: "Côté gauche" },
  { value: 9, label: "Multiple" }
];

// Options supplémentaires pour les piétons (à utiliser si nécessaire)
const LOCALISATION_PIETON = [
  { value: -1, label: "Non renseigné" },
  { value: 0, label: "Sans objet" },
  // Sur chaussée
  { value: 1, label: "À + 50m du passage piéton" },
  { value: 2, label: "À - 50m du passage piéton" },
  // Sur passage piéton
  { value: 3, label: "Sans signalisation lumineuse" },
  { value: 4, label: "Avec signalisation lumineuse" },
  // Divers
  { value: 5, label: "Sur trottoir" },
  { value: 6, label: "Sur accotement" },
  { value: 7, label: "Sur refuge ou BAU" },
  { value: 8, label: "Sur contre allée" },
  { value: 9, label: "Inconnue" }
];

const ACTION_PIETON = [
  { value: -1, label: "Non renseigné" },
  { value: 0, label: "Non renseigné ou sans objet" },
  // Se déplaçant
  { value: 1, label: "Sens véhicule heurtant" },
  { value: 2, label: "Sens inverse du véhicule" },
  // Divers
  { value: 3, label: "Traversant" },
  { value: 4, label: "Masqué" },
  { value: 5, label: "Jouant - courant" },
  { value: 6, label: "Avec animal" },
  { value: 9, label: "Autre" },
  { value: "A", label: "Monte/descend du véhicule" },
  { value: "B", label: "Inconnue" }
];

function AccidentForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = !!id;
  
  const [loading, setLoading] = useState(isEditMode);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    date_accident: new Date().toISOString().split('T')[0],
    heure_accident: '',
    lieu_departement: '',
    lieu_commune: '',
    agglomeration: 1,
    type_route: 1,
    condition_meteo: 1,
    luminosite: 1,
    categorie_vehicule: 1,
    categorie_usager: 1,
    age: 30,
    motif_deplacement: 1,
    equipement_securite: 1,
    place_usager: 1,
    sexe_usager: 1,
    manoeuvre_principal_accident: 1,
    type_moteur: 1,
    vitesse_max: 50,
    point_choc_initial: 1,
    description: ''
  });
  
  useEffect(() => {
    if (isEditMode) {
      const fetchAccident = async () => {
        try {
          const data = await accidentService.getAccidentById(id);
          setFormData(data);
        } catch (err) {
          setError("Erreur lors du chargement des données de l'accident");
        } finally {
          setLoading(false);
        }
      };
      
      fetchAccident();
    }
  }, [id, isEditMode]);
  
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    
    // Convertir les valeurs numériques
    const fieldValue = (type === 'number' || [
      'lieu_departement', 'agglomeration', 'type_route', 'condition_meteo',
      'luminosite', 'categorie_vehicule', 'categorie_usager', 'age',
      'motif_deplacement', 'equipement_securite', 'place_usager',
      'sexe_usager', 'manoeuvre_principal_accident', 'type_moteur',
      'vitesse_max', 'point_choc_initial'
    ].includes(name)) ? Number(value) : value;
    
    setFormData({ ...formData, [name]: fieldValue });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      let result;
      if (isEditMode) {
        result = await accidentService.updateAccident(id, formData);
        toast.success('Accident mis à jour avec succès');
      } else {
        result = await accidentService.createAccident(formData);
        toast.success('Accident enregistré avec succès');
      }
      
      // Si la réponse contient une prédiction, rediriger vers la page de détails
      if (result && result.id) {
        navigate(`/accidents/${result.id}`);
      } else {
        navigate('/accidents/user');
      }
    } catch (err) {
      setError(err.response?.data?.error || "Erreur lors de l'enregistrement");
    } finally {
      setLoading(false);
    }
  };
  
  if (loading && isEditMode) {
    return <div className="text-center p-5">Chargement...</div>;
  }
  
  return (
    <Container>
      <Card className="shadow-sm my-4">
        <Card.Body>
          <h2 className="mb-4">Déclarer un accident</h2>
          {error && <div className="alert alert-danger">{error}</div>}
          
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Date de l'accident*</Form.Label>
                  <Form.Control
                    type="date"
                    name="date_accident"
                    value={formData.date_accident}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Heure de l'accident</Form.Label>
                  <Form.Control
                    type="time"
                    name="heure_accident"
                    value={formData.heure_accident || ''}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
            </Row>
            
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Département*</Form.Label>
                  <Form.Control
                    type="number"
                    name="lieu_departement"
                    value={formData.lieu_departement}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Commune</Form.Label>
                  <Form.Control
                    type="text"
                    name="lieu_commune"
                    value={formData.lieu_commune || ''}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Agglomération*</Form.Label>
                  <Form.Select
                    name="agglomeration"
                    value={formData.agglomeration}
                    onChange={handleChange}
                    required
                  >
                    <option value={1}>En agglomération (1)</option>
                    <option value={2}>Hors agglomération (2)</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Type de route*</Form.Label>
                  <Form.Select
                    name="type_route"
                    value={formData.type_route}
                    onChange={handleChange}
                    required
                  >
                    {TYPE_ROUTE.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Condition météo*</Form.Label>
                  <Form.Select
                    name="condition_meteo"
                    value={formData.condition_meteo}
                    onChange={handleChange}
                    required
                  >
                    {CONDITIONS_METEO.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Luminosité*</Form.Label>
                  <Form.Select
                    name="luminosite"
                    value={formData.luminosite}
                    onChange={handleChange}
                    required
                  >
                    {LUMINOSITE.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Catégorie de véhicule*</Form.Label>
                  <Form.Select
                    name="categorie_vehicule"
                    value={formData.categorie_vehicule}
                    onChange={handleChange}
                    required
                  >
                    {CATEGORIE_VEHICULE.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Catégorie d'usager*</Form.Label>
                  <Form.Select
                    name="categorie_usager"
                    value={formData.categorie_usager}
                    onChange={handleChange}
                    required
                  >
                    {CATEGORIE_USAGER.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Âge*</Form.Label>
                  <Form.Control
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Motif de déplacement*</Form.Label>
                  <Form.Select
                    name="motif_deplacement"
                    value={formData.motif_deplacement}
                    onChange={handleChange}
                    required
                  >
                    {MOTIF_DEPLACEMENT.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Équipement de sécurité*</Form.Label>
                  <Form.Select
                    name="equipement_securite"
                    value={formData.equipement_securite}
                    onChange={handleChange}
                    required
                  >
                    {EQUIPEMENT_SECURITE.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Place de l'usager*</Form.Label>
                  <Form.Select
                    name="place_usager"
                    value={formData.place_usager}
                    onChange={handleChange}
                    required
                  >
                    {PLACE_USAGER.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Sexe de l'usager*</Form.Label>
                  <Form.Select
                    name="sexe_usager"
                    value={formData.sexe_usager}
                    onChange={handleChange}
                    required
                  >
                    <option value={1}>Homme (1)</option>
                    <option value={2}>Femme (2)</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Manœuvre principale*</Form.Label>
                  <Form.Select
                    name="manoeuvre_principal_accident"
                    value={formData.manoeuvre_principal_accident}
                    onChange={handleChange}
                    required
                  >
                    {MANOEUVRE_PRINCIPALE.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Type de moteur*</Form.Label>
                  <Form.Select
                    name="type_moteur"
                    value={formData.type_moteur}
                    onChange={handleChange}
                    required
                  >
                    {TYPE_MOTEUR.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({option.value})
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Vitesse maximale*</Form.Label>
                  <Form.Control
                    type="number"
                    name="vitesse_max"
                    value={formData.vitesse_max}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Point de choc initial*</Form.Label>
              <Form.Select
                name="point_choc_initial"
                value={formData.point_choc_initial}
                onChange={handleChange}
                required
              >
                {POINT_CHOC_INITIAL.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label} ({option.value})
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                name="description"
                value={formData.description || ''}
                onChange={handleChange}
                rows={4}
              />
            </Form.Group>
            
            <div className="d-flex justify-content-between mt-4">
              <Button variant="secondary" onClick={() => navigate('/accidents/user')}>
                Annuler
              </Button>
              <Button type="submit" variant="primary" disabled={loading}>
                {loading ? 'Enregistrement...' : 'Enregistrer'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}

export default AccidentForm;