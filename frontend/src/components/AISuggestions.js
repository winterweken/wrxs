import React, { useState } from 'react';

function AISuggestions({ token }) {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(null);
  const [formData, setFormData] = useState({
    current_fitness_level: 'intermediate',
    available_equipment: [],
    time_available_minutes: 60,
    target_muscle_groups: []
  });

  const equipmentOptions = ['barbell', 'dumbbells', 'bench', 'pull-up bar', 'cable machine'];
  const muscleGroupOptions = ['chest', 'back', 'legs', 'shoulders', 'arms', 'core'];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleCheckboxChange = (field, value) => {
    const current = formData[field];
    if (current.includes(value)) {
      setFormData({
        ...formData,
        [field]: current.filter(item => item !== value)
      });
    } else {
      setFormData({
        ...formData,
        [field]: [...current, value]
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuggestions(null);

    try {
      const requestData = {
        ...formData,
        time_available_minutes: parseInt(formData.time_available_minutes),
        available_equipment: formData.available_equipment.length > 0 ? formData.available_equipment : null,
        target_muscle_groups: formData.target_muscle_groups.length > 0 ? formData.target_muscle_groups : null
      };

      const response = await fetch('http://localhost:8000/api/ai/suggest-workout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        const data = await response.json();
        setSuggestions(data);
      } else {
        alert('Failed to get suggestions. Please try again.');
      }
    } catch (error) {
      console.error('Error getting suggestions:', error);
      alert('Error getting suggestions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h3 style={{ marginBottom: '20px' }}>Get Personalized Workout Recommendations</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Fitness Level</label>
            <select
              name="current_fitness_level"
              value={formData.current_fitness_level}
              onChange={handleChange}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label>Available Equipment</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '8px' }}>
              {equipmentOptions.map(equipment => (
                <label key={equipment} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={formData.available_equipment.includes(equipment)}
                    onChange={() => handleCheckboxChange('available_equipment', equipment)}
                    style={{ marginRight: '8px' }}
                  />
                  {equipment}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Target Muscle Groups</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '8px' }}>
              {muscleGroupOptions.map(muscle => (
                <label key={muscle} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={formData.target_muscle_groups.includes(muscle)}
                    onChange={() => handleCheckboxChange('target_muscle_groups', muscle)}
                    style={{ marginRight: '8px' }}
                  />
                  {muscle}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Time Available (minutes)</label>
            <input
              type="number"
              name="time_available_minutes"
              value={formData.time_available_minutes}
              onChange={handleChange}
              min="15"
              max="180"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Generating Suggestions...' : 'Get AI Suggestions'}
          </button>
        </form>
      </div>

      {suggestions && (
        <div className="card" style={{ marginTop: '20px' }}>
          <h3 style={{ marginBottom: '16px' }}>Recommended Workout</h3>

          <div style={{
            backgroundColor: '#e3f2fd',
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            <p style={{ margin: 0, color: '#1976d2' }}>
              <strong>Why these exercises:</strong> {suggestions.rationale}
            </p>
          </div>

          <h4 style={{ marginBottom: '16px' }}>Suggested Exercises</h4>

          {suggestions.suggested_exercises && suggestions.suggested_exercises.length > 0 ? (
            <div className="grid">
              {suggestions.suggested_exercises.map((exercise) => (
                <div key={exercise.id} className="exercise-card">
                  <h3>{exercise.name}</h3>
                  <div style={{ marginBottom: '12px' }}>
                    <span className="badge badge-primary">{exercise.difficulty}</span>
                    <span className="badge badge-success">{exercise.category}</span>
                  </div>
                  <p style={{ marginBottom: '12px', color: '#666', fontSize: '14px' }}>
                    {exercise.description}
                  </p>
                  <div>
                    <strong>Targets:</strong>
                    <div>
                      {exercise.muscle_groups.map((muscle, index) => (
                        <span key={index} className="badge badge-primary">
                          {muscle}
                        </span>
                      ))}
                    </div>
                  </div>
                  {exercise.instructions && (
                    <p style={{ marginTop: '12px', fontSize: '13px', fontStyle: 'italic', color: '#555' }}>
                      {exercise.instructions}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#666' }}>No exercises found. Try adjusting your filters.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default AISuggestions;
