import React, { useState, useEffect } from 'react';

function Profile({ token, user, onUpdate }) {
  const [formData, setFormData] = useState({
    full_name: '',
    weight_kg: '',
    height_cm: '',
    fitness_level: '',
    fitness_goals: []
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        weight_kg: user.weight_kg || '',
        height_cm: user.height_cm || '',
        fitness_level: user.fitness_level || '',
        fitness_goals: user.fitness_goals || []
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleGoalsChange = (goal) => {
    const currentGoals = formData.fitness_goals || [];
    if (currentGoals.includes(goal)) {
      setFormData({
        ...formData,
        fitness_goals: currentGoals.filter(g => g !== goal)
      });
    } else {
      setFormData({
        ...formData,
        fitness_goals: [...currentGoals, goal]
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const updateData = {
        ...formData,
        weight_kg: formData.weight_kg ? parseFloat(formData.weight_kg) : null,
        height_cm: formData.height_cm ? parseFloat(formData.height_cm) : null,
        fitness_goals: formData.fitness_goals.length > 0 ? formData.fitness_goals : null
      };

      const response = await fetch('http://localhost:8000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        setMessage('Profile updated successfully!');
        onUpdate();
      } else {
        setMessage('Failed to update profile');
      }
    } catch (error) {
      setMessage('Error updating profile');
    }
  };

  const goalOptions = [
    'muscle_gain',
    'weight_loss',
    'endurance',
    'strength',
    'flexibility',
    'general_fitness'
  ];

  return (
    <div>
      <h1>Profile</h1>

      <div className="card" style={{ marginTop: '20px' }}>
        <h3 style={{ marginBottom: '20px' }}>Account Information</h3>
        <p><strong>Username:</strong> {user?.username}</p>
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>Member Since:</strong> {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}</p>
      </div>

      <div className="card" style={{ marginTop: '20px' }}>
        <h3 style={{ marginBottom: '20px' }}>Update Profile</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
            <div className="form-group">
              <label>Weight (kg)</label>
              <input
                type="number"
                step="0.1"
                name="weight_kg"
                value={formData.weight_kg}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Height (cm)</label>
              <input
                type="number"
                step="0.1"
                name="height_cm"
                value={formData.height_cm}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Fitness Level</label>
            <select name="fitness_level" value={formData.fitness_level} onChange={handleChange}>
              <option value="">Select level</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label>Fitness Goals</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '8px' }}>
              {goalOptions.map(goal => (
                <label key={goal} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={formData.fitness_goals.includes(goal)}
                    onChange={() => handleGoalsChange(goal)}
                    style={{ marginRight: '8px' }}
                  />
                  {goal.replace('_', ' ')}
                </label>
              ))}
            </div>
          </div>

          {message && (
            <div className={message.includes('success') ? 'success' : 'error'}>
              {message}
            </div>
          )}

          <button type="submit" className="btn btn-primary">Update Profile</button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
