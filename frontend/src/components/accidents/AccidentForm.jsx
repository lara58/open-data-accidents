// src/components/accidents/AccidentForm.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import { accidentService } from '../../services/accidentService';
import { toast } from 'react-toastify';

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
                    <option value={1}>En agglomération</option>
                    <option value={2}>Hors agglomération</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Type de route*</Form.Label>
                  <Form.Control
                    type="number"
                    name="type_route"
                    value={formData.type_route}
                    onChange={handleChange}
                    required
                    min={1}
                  />
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
                        {option.label}
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
                        {option.label}
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
                  <Form.Control
                    type="number"
                    name="categorie_vehicule"
                    value={formData.categorie_vehicule}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Catégorie d'usager*</Form.Label>
                  <Form.Control
                    type="number"
                    name="categorie_usager"
                    value={formData.categorie_usager}
                    onChange={handleChange}
                    required
                    min={1}
                  />
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
                  <Form.Control
                    type="number"
                    name="motif_deplacement"
                    value={formData.motif_deplacement}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Équipement de sécurité*</Form.Label>
                  <Form.Control
                    type="number"
                    name="equipement_securite"
                    value={formData.equipement_securite}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Place de l'usager*</Form.Label>
                  <Form.Control
                    type="number"
                    name="place_usager"
                    value={formData.place_usager}
                    onChange={handleChange}
                    required
                    min={1}
                  />
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
                    <option value={1}>Homme</option>
                    <option value={2}>Femme</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Manœuvre principale*</Form.Label>
                  <Form.Control
                    type="number"
                    name="manoeuvre_principal_accident"
                    value={formData.manoeuvre_principal_accident}
                    onChange={handleChange}
                    required
                    min={1}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Type de moteur*</Form.Label>
                  <Form.Control
                    type="number"
                    name="type_moteur"
                    value={formData.type_moteur}
                    onChange={handleChange}
                    required
                    min={1}
                  />
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
              <Form.Control
                type="number"
                name="point_choc_initial"
                value={formData.point_choc_initial}
                onChange={handleChange}
                required
                min={1}
              />
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