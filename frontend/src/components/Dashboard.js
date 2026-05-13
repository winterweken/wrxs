import React, { useState, useEffect } from 'react';
import CurrentStreakCard from './dashboard/CurrentStreakCard';
import WeeklyStreakGrid from './dashboard/WeeklyStreakGrid';
import WeekComparisonCard from './dashboard/WeekComparisonCard';
import FrequencyChart from './dashboard/FrequencyChart';

function Dashboard({ token, user }) {
  const [todaysWorkout, setTodaysWorkout] = useState(null);
  const [loadingWorkout, setLoadingWorkout] = useState(true);

  useEffect(() => {
    fetchTodaysWorkout();
  }, [token]);

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

  return (
    <div>
      <h1>Welcome back{user?.full_name ? `, ${user.full_name}` : ''}!</h1>

      {/* Streak card - most prominent */}
      <div style={{ marginTop: '30px' }}>
        <CurrentStreakCard token={token} />
      </div>

      {/* Weekly streak grid */}
      <WeeklyStreakGrid token={token} />

      {/* Week comparison */}
      <WeekComparisonCard token={token} />

      {/* Frequency chart */}
      <FrequencyChart token={token} />

      {/* Today's workout section */}
      <div className="card" style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        marginTop: '30px'
      }}>
        <h2 style={{ marginBottom: '20px' }}>Today's Workout</h2>
        {!loadingWorkout && todaysWorkout ? (
          <div>
            <h3 style={{ fontSize: '24px', marginBottom: '12px' }}>{todaysWorkout.workout_name}</h3>
            <p style={{ opacity: 0.9, marginBottom: '8px' }}>
              Focus: {todaysWorkout.focus_areas.join(', ')}
            </p>
            <p style={{ opacity: 0.9, marginBottom: '16px' }}>
              Duration: ~{todaysWorkout.estimated_duration_minutes} minutes
            </p>
            {todaysWorkout.exercises && todaysWorkout.exercises.length > 0 && (
              <div style={{ marginBottom: '16px' }}>
                <strong>Exercises:</strong>
                <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                  {todaysWorkout.exercises.slice(0, 3).map((ex, idx) => (
                    <li key={idx}>{ex.exercise.name} - {ex.sets} sets</li>
                  ))}
                  {todaysWorkout.exercises.length > 3 && (
                    <li>...and {todaysWorkout.exercises.length - 3} more</li>
                  )}
                </ul>
              </div>
            )}
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <button
                className="btn"
                style={{
                  backgroundColor: 'white',
                  color: '#667eea',
                  fontWeight: '600',
                  border: 'none'
                }}
                onClick={() => window.location.href = '/performance'}
              >
                Start Workout
              </button>
              <button
                className="btn"
                style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  fontWeight: '600',
                  border: '1px solid white'
                }}
                onClick={() => window.location.href = '/performance'}
              >
                Add Workout
              </button>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                className="btn"
                style={{
                  backgroundColor: 'white',
                  color: '#667eea',
                  fontWeight: '600',
                  border: 'none'
                }}
                onClick={() => window.location.href = '/performance'}
              >
                Add Workout
              </button>
              <button
                className="btn"
                style={{
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  fontWeight: '600',
                  border: '1px solid white'
                }}
                onClick={() => window.location.href = '/performance#trainer'}
              >
                Create Workout Plan
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
