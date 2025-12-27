import React, { useState, useEffect } from 'react';

function Dashboard({ token, user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [todaysWorkout, setTodaysWorkout] = useState(null);
  const [loadingWorkout, setLoadingWorkout] = useState(true);

  useEffect(() => {
    fetchStats();
    fetchTodaysWorkout();
  }, [token]);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/workout-logs/stats?days=30', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTodaysWorkout = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/trainer/daily-workout', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setTodaysWorkout(data);
      }
    } catch (error) {
      console.error('Error fetching today\'s workout:', error);
    } finally {
      setLoadingWorkout(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div>
      <h1>Welcome back{user?.full_name ? `, ${user.full_name}` : ''}!</h1>

      <div className="grid" style={{ marginTop: '30px' }}>
        <div className="card">
          <h3 style={{ marginBottom: '16px' }}>Workout Summary (30 days)</h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#007bff', marginBottom: '8px' }}>
            {stats?.total_workouts || 0}
          </div>
          <p style={{ color: '#666' }}>Total Workouts</p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '16px' }}>Total Sets</h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#28a745', marginBottom: '8px' }}>
            {stats?.total_sets || 0}
          </div>
          <p style={{ color: '#666' }}>Sets Completed</p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '16px' }}>Fitness Level</h3>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#17a2b8', marginBottom: '8px' }}>
            {user?.fitness_level || 'Not Set'}
          </div>
          <p style={{ color: '#666' }}>Current Level</p>
        </div>
      </div>

      {stats?.most_performed_exercises && stats.most_performed_exercises.length > 0 && (
        <div className="card" style={{ marginTop: '30px' }}>
          <h3 style={{ marginBottom: '16px' }}>Most Performed Exercises</h3>
          <table>
            <thead>
              <tr>
                <th>Exercise</th>
                <th>Times Performed</th>
              </tr>
            </thead>
            <tbody>
              {stats.most_performed_exercises.map((exercise, index) => (
                <tr key={index}>
                  <td>{exercise.name}</td>
                  <td>{exercise.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="card" style={{ marginTop: '30px' }}>
        <h3 style={{ marginBottom: '16px' }}>Quick Actions</h3>

        {/* AI Trainer Workout Section */}
        {loadingWorkout ? (
          <div style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '8px', marginBottom: '20px' }}>
            <p>Loading today's workout...</p>
          </div>
        ) : todaysWorkout ? (
          <div style={{
            padding: '20px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            <h4 style={{ marginBottom: '12px', color: 'white' }}>Today's AI Workout: {todaysWorkout.workout_name}</h4>
            <p style={{ marginBottom: '12px', opacity: 0.95 }}>
              <strong>Focus:</strong> {todaysWorkout.focus_areas.join(', ')} | <strong>Duration:</strong> {todaysWorkout.estimated_duration_minutes} min
            </p>
            {todaysWorkout.exercises && todaysWorkout.exercises.length > 0 && (
              <div style={{ marginBottom: '16px' }}>
                <strong>Exercises:</strong>
                <ul style={{ marginTop: '8px', marginLeft: '20px' }}>
                  {todaysWorkout.exercises.slice(0, 3).map((ex, idx) => (
                    <li key={idx}>
                      {ex.exercise.name} - {ex.sets}x{Array.isArray(ex.reps) ? ex.reps.join(',') : ex.reps}
                    </li>
                  ))}
                  {todaysWorkout.exercises.length > 3 && (
                    <li>... and {todaysWorkout.exercises.length - 3} more exercises</li>
                  )}
                </ul>
              </div>
            )}
            <button
              className="btn"
              style={{
                background: 'white',
                color: '#667eea',
                fontWeight: '600',
                border: 'none'
              }}
              onClick={() => window.location.href = '/workouts'}
            >
              Start Workout
            </button>
          </div>
        ) : (
          <div style={{
            padding: '20px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: '8px',
            marginBottom: '20px',
            textAlign: 'center'
          }}>
            <h4 style={{ marginBottom: '12px', color: 'white' }}>No AI Training Program Yet</h4>
            <p style={{ marginBottom: '16px', opacity: 0.95 }}>
              Let our AI trainer create a personalized workout program for you
            </p>
            <button
              className="btn"
              style={{
                background: 'white',
                color: '#667eea',
                fontWeight: '600',
                border: 'none'
              }}
              onClick={() => window.location.href = '/workouts'}
            >
              Create Workout Plan
            </button>
          </div>
        )}

        {/* Regular Action Buttons */}
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => window.location.href = '/workouts'}>
            Add Workout
          </button>
          <button className="btn btn-secondary" onClick={() => window.location.href = '/exercises'}>
            Browse Exercises
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
