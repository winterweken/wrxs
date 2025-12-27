import React, { useState, useEffect } from 'react';

function WorkoutLogs({ token }) {
  const [logs, setLogs] = useState([]);
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showLogForm, setShowLogForm] = useState(false);
  const [formData, setFormData] = useState({
    exercise_id: '',
    sets_completed: 3,
    reps: '10,10,10',
    weight_kg: '',
    notes: '',
    difficulty_rating: 5
  });

  useEffect(() => {
    fetchLogs();
    fetchExercises();
  }, [token]);

  const fetchLogs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/workout-logs?limit=50', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setLogs(data);
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchExercises = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/exercises', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setExercises(data);
      }
    } catch (error) {
      console.error('Error fetching exercises:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reps = formData.reps.split(',').map(r => parseInt(r.trim()));
    const weight_kg = formData.weight_kg ?
      formData.weight_kg.split(',').map(w => parseFloat(w.trim())) : null;

    try {
      const response = await fetch('http://localhost:8000/api/workout-logs', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          exercise_id: parseInt(formData.exercise_id),
          sets_completed: parseInt(formData.sets_completed),
          reps: reps,
          weight_kg: weight_kg,
          notes: formData.notes || null,
          difficulty_rating: parseInt(formData.difficulty_rating)
        })
      });

      if (response.ok) {
        setShowLogForm(false);
        setFormData({
          exercise_id: '',
          sets_completed: 3,
          reps: '10,10,10',
          weight_kg: '',
          notes: '',
          difficulty_rating: 5
        });
        fetchLogs();
      }
    } catch (error) {
      console.error('Error logging workout:', error);
    }
  };

  const handleDelete = async (logId) => {
    if (!window.confirm('Delete this workout log?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/workout-logs/${logId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        fetchLogs();
      }
    } catch (error) {
      console.error('Error deleting log:', error);
    }
  };

  const getExerciseName = (exerciseId) => {
    const exercise = exercises.find(e => e.id === exerciseId);
    return exercise ? exercise.name : 'Unknown Exercise';
  };

  if (loading) {
    return <div className="loading">Loading workout logs...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <button
          className="btn btn-primary"
          onClick={() => setShowLogForm(!showLogForm)}
        >
          {showLogForm ? 'Cancel' : 'Log New Workout'}
        </button>
      </div>

      {showLogForm && (
        <div className="card" style={{ marginTop: '20px' }}>
          <h3 style={{ marginBottom: '20px' }}>Log Workout</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Exercise</label>
              <select
                name="exercise_id"
                value={formData.exercise_id}
                onChange={handleChange}
                required
              >
                <option value="">Select an exercise</option>
                {exercises.map(ex => (
                  <option key={ex.id} value={ex.id}>{ex.name}</option>
                ))}
              </select>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '16px' }}>
              <div className="form-group">
                <label>Sets Completed</label>
                <input
                  type="number"
                  name="sets_completed"
                  value={formData.sets_completed}
                  onChange={handleChange}
                  min="1"
                  required
                />
              </div>
              <div className="form-group">
                <label>Reps (comma-separated)</label>
                <input
                  type="text"
                  name="reps"
                  value={formData.reps}
                  onChange={handleChange}
                  placeholder="10,10,10"
                  required
                />
              </div>
            </div>
            <div className="form-group">
              <label>Weight (kg, comma-separated, optional)</label>
              <input
                type="text"
                name="weight_kg"
                value={formData.weight_kg}
                onChange={handleChange}
                placeholder="50,50,52.5"
              />
            </div>
            <div className="form-group">
              <label>Difficulty Rating (1-10)</label>
              <input
                type="number"
                name="difficulty_rating"
                value={formData.difficulty_rating}
                onChange={handleChange}
                min="1"
                max="10"
              />
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows="2"
              />
            </div>
            <button type="submit" className="btn btn-primary">Log Workout</button>
          </form>
        </div>
      )}

      {logs.length === 0 ? (
        <div className="card" style={{ marginTop: '20px', textAlign: 'center', padding: '40px' }}>
          <p style={{ color: '#666' }}>No workout logs yet. Start logging your workouts!</p>
        </div>
      ) : (
        <div className="card" style={{ marginTop: '20px' }}>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Exercise</th>
                <th>Sets x Reps</th>
                <th>Weight (kg)</th>
                <th>Rating</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td>{new Date(log.date).toLocaleDateString()}</td>
                  <td>{getExerciseName(log.exercise_id)}</td>
                  <td>{log.sets_completed} x {log.reps.join(', ')}</td>
                  <td>{log.weight_kg ? log.weight_kg.join(', ') : '-'}</td>
                  <td>{log.difficulty_rating || '-'}/10</td>
                  <td>
                    <button
                      className="btn btn-danger"
                      style={{ padding: '4px 12px', fontSize: '14px' }}
                      onClick={() => handleDelete(log.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default WorkoutLogs;
