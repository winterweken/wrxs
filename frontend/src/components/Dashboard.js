import React, { useState, useEffect } from 'react';

function Dashboard({ token, user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
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
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => window.location.href = '/workout-logs'}>
            Log New Workout
          </button>
          <button className="btn btn-secondary" onClick={() => window.location.href = '/workout-plans'}>
            View Workout Plans
          </button>
          <button className="btn btn-secondary" onClick={() => window.location.href = '/ai-suggestions'}>
            Get AI Suggestions
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
