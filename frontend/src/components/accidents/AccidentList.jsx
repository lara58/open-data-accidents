// src/components/accidents/AccidentList.jsx
import React, { useState, useEffect } from 'react';
import { Table, Button, Alert, Spinner, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { accidentService } from '../../services/accidentService';
import { toast } from 'react-toastify';
import AccidentMap from './AccidentMap';

const AccidentList = ({ showAll = true }) => {
  const [accidents, setAccidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchAccidents = async () => {
      try {
        const response = showAll 
          ? await accidentService.getAllAccidents()
          : await accidentService.getUserAccidents();
        
        setAccidents(response.accidents || []);
      } catch (err) {
        setError('Erreur lors du chargement des accidents');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAccidents();
  }, [showAll]);
  
  const handleDelete = async (id) => {
    if (window.confirm("Êtes-vous sûr de vouloir supprimer cet accident ?")) {
      try {
        await accidentService.deleteAccident(id);
        setAccidents(accidents.filter(accident => accident.id !== id));
        toast.success('Accident supprimé avec succès');
      } catch (err) {
        toast.error('Erreur lors de la suppression');
      }
    }
  };
  
  if (loading) {
    return (
      <div className="text-center p-5">
        <Spinner animation="border" role="status" />
        <p className="mt-3">Chargement des données...</p>
      </div>
    );
  }
  
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>{showAll ? 'Tous les accidents' : 'Mes accidents'}</h2>
        {!showAll && (
          <Link to="/accidents/new" className="btn btn-primary">
            Déclarer un accident
          </Link>
        )}
      </div>
      
      {error && <Alert variant="danger">{error}</Alert>}
      
      {/* Ajouter la carte avant la table des accidents */}
      {!loading && accidents.length > 0 && (
        <Card className="mb-4">
          <Card.Body>
            <AccidentMap accidents={accidents} />
          </Card.Body>
        </Card>
      )}
      
      {/* Votre table d'accidents existante... */}
      {accidents.length === 0 ? (
        <Alert variant="info">Aucun accident trouvé.</Alert>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Date</th>
              <th>Département</th>
              <th>Gravité</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {accidents.map(accident => (
              <tr key={accident.id}>
                <td>{accident.date_accident}</td>
                <td>{accident.lieu_departement}</td>
                <td>{accident.gravite_accident}</td>
                <td>
                  <Link to={`/accidents/${accident.id}`} className="btn btn-sm btn-info me-2">
                    Détails
                  </Link>
                  {!showAll && (
                    <>
                      <Link to={`/accidents/edit/${accident.id}`} className="btn btn-sm btn-warning me-2">
                        Modifier
                      </Link>
                      <Button 
                        variant="danger" 
                        size="sm"
                        onClick={() => handleDelete(accident.id)}
                      >
                        Supprimer
                      </Button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
};

export default AccidentList;