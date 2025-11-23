import React, { useState, useEffect } from 'react';

function Exercises({ token }) {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    difficulty: '',
    muscle_group: ''
  });

  useEffect(() => {
    fetchExercises();
  }, [token, filters]);

  const fetchExercises = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.category) params.append('category', filters.category);
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.muscle_group) params.append('muscle_group', filters.muscle_group);

      const response = await fetch(`http://localhost:8000/api/exercises?${params}`, {
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
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'badge-success';
      case 'intermediate': return 'badge-warning';
      case 'advanced': return 'badge-danger';
      default: return 'badge-primary';
    }
  };

  if (loading) {
    return <div className="loading">Loading exercises...</div>;
  }

  return (
    <div>
      <h1>Exercise Library</h1>

      <div className="card" style={{ marginTop: '20px' }}>
        <h3 style={{ marginBottom: '16px' }}>Filters</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Category</label>
            <select name="category" value={filters.category} onChange={handleFilterChange}>
              <option value="">All Categories</option>
              <option value="strength">Strength</option>
              <option value="cardio">Cardio</option>
              <option value="flexibility">Flexibility</option>
            </select>
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Difficulty</label>
            <select name="difficulty" value={filters.difficulty} onChange={handleFilterChange}>
              <option value="">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Muscle Group</label>
            <select name="muscle_group" value={filters.muscle_group} onChange={handleFilterChange}>
              <option value="">All Muscles</option>
              <option value="chest">Chest</option>
              <option value="back">Back</option>
              <option value="legs">Legs</option>
              <option value="shoulders">Shoulders</option>
              <option value="arms">Arms</option>
              <option value="core">Core</option>
            </select>
          </div>
        </div>
      </div>

      <p style={{ marginTop: '20px', color: '#666' }}>
        Showing {exercises.length} exercises
      </p>

      <div className="grid">
        {exercises.map((exercise) => (
          <div key={exercise.id} className="exercise-card">
            <h3>{exercise.name}</h3>
            <div style={{ marginBottom: '12px' }}>
              <span className={`badge ${getDifficultyColor(exercise.difficulty)}`}>
                {exercise.difficulty}
              </span>
              <span className="badge badge-primary">{exercise.category}</span>
            </div>
            <p style={{ marginBottom: '12px', color: '#666', fontSize: '14px' }}>
              {exercise.description}
            </p>
            <div style={{ marginBottom: '8px' }}>
              <strong>Muscle Groups:</strong>
              <div>
                {exercise.muscle_groups.map((muscle, index) => (
                  <span key={index} className="badge badge-primary">
                    {muscle}
                  </span>
                ))}
              </div>
            </div>
            {exercise.equipment && exercise.equipment.length > 0 && (
              <div>
                <strong>Equipment:</strong> {exercise.equipment.join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Exercises;
