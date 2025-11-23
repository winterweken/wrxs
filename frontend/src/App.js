import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Exercises from './components/Exercises';
import WorkoutPlans from './components/WorkoutPlans';
import WorkoutLogs from './components/WorkoutLogs';
import Profile from './components/Profile';
import AISuggestions from './components/AISuggestions';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      fetchUserProfile();
    } else {
      localStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else {
        setToken(null);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
  };

  if (!token) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/register" element={<Register setToken={setToken} />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    );
  }

  return (
    <Router>
      <div className="navbar">
        <div className="container">
          <h1>WRXS</h1>
          <nav>
            <Link to="/">Dashboard</Link>
            <Link to="/exercises">Exercises</Link>
            <Link to="/workout-plans">Workout Plans</Link>
            <Link to="/workout-logs">Workout Logs</Link>
            <Link to="/ai-suggestions">AI Suggestions</Link>
            <Link to="/profile">Profile</Link>
            <button onClick={handleLogout} className="btn btn-secondary" style={{marginLeft: '20px'}}>
              Logout
            </button>
          </nav>
        </div>
      </div>

      <div className="container">
        <Routes>
          <Route path="/" element={<Dashboard token={token} user={user} />} />
          <Route path="/exercises" element={<Exercises token={token} />} />
          <Route path="/workout-plans" element={<WorkoutPlans token={token} />} />
          <Route path="/workout-logs" element={<WorkoutLogs token={token} />} />
          <Route path="/ai-suggestions" element={<AISuggestions token={token} />} />
          <Route path="/profile" element={<Profile token={token} user={user} onUpdate={fetchUserProfile} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
