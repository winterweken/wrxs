import React, { useState, useEffect } from 'react';

function WorkoutPlans({ token }) {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    difficulty: 'beginner',
    duration_weeks: 4,
    days_per_week: 3
  });

  useEffect(() => {
    fetchPlans();
  }, [token]);

  const fetchPlans = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/workout-plans', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setPlans(data);
      }
    } catch (error) {
      console.error('Error fetching plans:', error);
    } finally {
      setLoading(false);
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

    try {
      const response = await fetch('http://localhost:8000/api/workout-plans', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          exercise_details: []
        })
      });

      if (response.ok) {
        setShowCreateForm(false);
        setFormData({
          name: '',
          description: '',
          difficulty: 'beginner',
          duration_weeks: 4,
          days_per_week: 3
        });
        fetchPlans();
      }
    } catch (error) {
      console.error('Error creating plan:', error);
    }
  };

  const handleDelete = async (planId) => {
    if (!window.confirm('Are you sure you want to delete this plan?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/workout-plans/${planId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        fetchPlans();
      }
    } catch (error) {
      console.error('Error deleting plan:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading workout plans...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <button
          className="btn btn-primary"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? 'Cancel' : 'Create New Plan'}
        </button>
      </div>

      {showCreateForm && (
        <div className="card" style={{ marginTop: '20px' }}>
          <h3 style={{ marginBottom: '20px' }}>Create New Workout Plan</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Plan Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows="3"
              />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
              <div className="form-group">
                <label>Difficulty</label>
                <select name="difficulty" value={formData.difficulty} onChange={handleChange}>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              <div className="form-group">
                <label>Duration (weeks)</label>
                <input
                  type="number"
                  name="duration_weeks"
                  value={formData.duration_weeks}
                  onChange={handleChange}
                  min="1"
                />
              </div>
              <div className="form-group">
                <label>Days per Week</label>
                <input
                  type="number"
                  name="days_per_week"
                  value={formData.days_per_week}
                  onChange={handleChange}
                  min="1"
                  max="7"
                />
              </div>
            </div>
            <button type="submit" className="btn btn-primary">Create Plan</button>
          </form>
        </div>
      )}

      {plans.length === 0 ? (
        <div className="card" style={{ marginTop: '20px', textAlign: 'center', padding: '40px' }}>
          <p style={{ color: '#666' }}>No workout plans yet. Create your first plan!</p>
        </div>
      ) : (
        <div className="grid">
          {plans.map((plan) => (
            <div key={plan.id} className="card">
              <h3 style={{ marginBottom: '8px' }}>{plan.name}</h3>
              <div style={{ marginBottom: '12px' }}>
                <span className="badge badge-primary">{plan.difficulty}</span>
                {plan.duration_weeks && (
                  <span className="badge badge-secondary">{plan.duration_weeks} weeks</span>
                )}
                {plan.days_per_week && (
                  <span className="badge badge-secondary">{plan.days_per_week} days/week</span>
                )}
              </div>
              {plan.description && (
                <p style={{ marginBottom: '16px', color: '#666' }}>{plan.description}</p>
              )}
              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  className="btn btn-danger"
                  onClick={() => handleDelete(plan.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default WorkoutPlans;
