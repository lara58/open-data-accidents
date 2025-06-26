import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';

import './App.css';

// Composants
import Navbar from './components/common/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import AccidentList from './components/accidents/AccidentList';
import AccidentForm from './components/accidents/AccidentForm';
import AccidentDetail from './components/accidents/AccidentDetail';
import ProtectedRoute from './components/common/ProtectedRoute';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          {/* Routes publiques */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Routes protégées */}
          <Route path="/accidents" element={
            <ProtectedRoute>
              <AccidentList showAll={true} />
            </ProtectedRoute>
          } />
          
          <Route path="/accidents/user" element={
            <ProtectedRoute>
              <AccidentList showAll={false} />
            </ProtectedRoute>
          } />
          
          <Route path="/accidents/new" element={
            <ProtectedRoute>
              <AccidentForm />
            </ProtectedRoute>
          } />
          
          <Route path="/accidents/edit/:id" element={
            <ProtectedRoute>
              <AccidentForm />
            </ProtectedRoute>
          } />
          
          <Route path="/accidents/:id" element={
            <ProtectedRoute>
              <AccidentDetail />
            </ProtectedRoute>
          } />
          
          {/* Redirection par défaut */}
          <Route path="/" element={<Navigate to="/accidents" />} />
        </Routes>
      </div>
      <ToastContainer position="top-right" />
    </Router>
  );
}

export default App;
