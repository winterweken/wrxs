import React, { useState, useEffect } from 'react';

function PersonalTrainer({ token, user }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [activeProgram, setActiveProgram] = useState(null);
  const [todaysWorkout, setTodaysWorkout] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [generating, setGenerating] = useState(false);

  // Form state for program generation
  const [programType, setProgramType] = useState('multi_week');
  const [formData, setFormData] = useState({
    duration_weeks: 4,
    days_per_week: 3,
    fitness_level: user?.fitness_level || 'intermediate',
    fitness_goals: user?.fitness_goals || [],
    available_equipment: [],
    time_per_session_minutes: 60,
    preferences: {}
  });

  const equipmentOptions = ['barbell', 'dumbbells', 'bench', 'pull-up bar', 'cable machine', 'resistance bands'];
  const goalOptions = ['muscle_gain', 'weight_loss', 'endurance', 'strength', 'general_fitness'];

  useEffect(() => {
    fetchActiveProgram();
    fetchInsights();
  }, []);

  useEffect(() => {
    if (activeProgram) {
      fetchTodaysWorkout();
    }
  }, [activeProgram]);

  const fetchActiveProgram = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/trainer/active-program', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setActiveProgram(data);
      }
    } catch (error) {
      console.error('Error fetching active program:', error);
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
    }
  };

  const fetchInsights = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/trainer/insights', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setInsights(data);
      }
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  const handleGenerateProgram = async (e) => {
    e.preventDefault();
    setGenerating(true);

    try {
      const requestData = {
        program_type: programType,
        ...formData,
        duration_weeks: programType === 'multi_week' ? parseInt(formData.duration_weeks) : null
      };

      const response = await fetch('http://localhost:8000/api/trainer/generate-program', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        const program = await response.json();
        alert('Program generated successfully! Review it below and click Accept to activate.');
        setActiveProgram(program);
        setShowGenerateForm(false);
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error generating program:', error);
      alert('Failed to generate program. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const handleAcceptProgram = async (programId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/trainer/accept-program/${programId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert('Program accepted and activated!');
        fetchActiveProgram();
      }
    } catch (error) {
      console.error('Error accepting program:', error);
      alert('Failed to accept program');
    }
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

  const renderTabs = () => (
    <div style={{
      display: 'flex',
      gap: '8px',
      borderBottom: '2px solid #e0e0e0',
      marginBottom: '24px'
    }}>
      <button
        onClick={() => setActiveTab('overview')}
        style={{
          padding: '12px 24px',
          background: 'none',
          border: 'none',
          borderBottom: activeTab === 'overview' ? '3px solid #667eea' : '3px solid transparent',
          color: activeTab === 'overview' ? '#667eea' : '#666',
          fontWeight: activeTab === 'overview' ? '600' : '400',
          fontSize: '16px',
          cursor: 'pointer',
          marginBottom: '-2px'
        }}
      >
        Overview
      </button>
      {activeProgram && (
        <>
          <button
            onClick={() => setActiveTab('today')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'today' ? '3px solid #667eea' : '3px solid transparent',
              color: activeTab === 'today' ? '#667eea' : '#666',
              fontWeight: activeTab === 'today' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              marginBottom: '-2px'
            }}
          >
            Today's Workout
          </button>
          <button
            onClick={() => setActiveTab('program')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'program' ? '3px solid #667eea' : '3px solid transparent',
              color: activeTab === 'program' ? '#667eea' : '#666',
              fontWeight: activeTab === 'program' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              marginBottom: '-2px'
            }}
          >
            Full Program
          </button>
        </>
      )}
      <button
        onClick={() => setActiveTab('insights')}
        style={{
          padding: '12px 24px',
          background: 'none',
          border: 'none',
          borderBottom: activeTab === 'insights' ? '3px solid #667eea' : '3px solid transparent',
          color: activeTab === 'insights' ? '#667eea' : '#666',
          fontWeight: activeTab === 'insights' ? '600' : '400',
          fontSize: '16px',
          cursor: 'pointer',
          marginBottom: '-2px'
        }}
      >
        Insights
      </button>
    </div>
  );

  const renderOverviewTab = () => (
    <div>
      {!activeProgram && !showGenerateForm && (
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <h2 style={{ marginBottom: '16px' }}>Welcome to Your AI Personal Trainer</h2>
          <p style={{ marginBottom: '32px', color: '#666' }}>
            Get customized training programs designed by AI, tailored to your goals, equipment, and experience level.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => setShowGenerateForm(true)}
            style={{ fontSize: '18px', padding: '12px 32px' }}
          >
            Generate Your First Program
          </button>
        </div>
      )}

      {showGenerateForm && (
        <div className="card">
          <h3 style={{ marginBottom: '20px' }}>Generate Training Program</h3>

          <form onSubmit={handleGenerateProgram}>
            <div className="form-group">
              <label>Program Type</label>
              <select
                value={programType}
                onChange={(e) => setProgramType(e.target.value)}
                className="form-control"
              >
                <option value="multi_week">Multi-Week Program</option>
                <option value="daily">Daily Workout</option>
              </select>
            </div>

            {programType === 'multi_week' && (
              <div className="form-group">
                <label>Program Duration (weeks)</label>
                <input
                  type="number"
                  min="1"
                  max="16"
                  value={formData.duration_weeks}
                  onChange={(e) => setFormData({ ...formData, duration_weeks: e.target.value })}
                  className="form-control"
                />
              </div>
            )}

            <div className="form-group">
              <label>Training Days per Week</label>
              <input
                type="number"
                min="1"
                max="7"
                value={formData.days_per_week}
                onChange={(e) => setFormData({ ...formData, days_per_week: e.target.value })}
                className="form-control"
              />
            </div>

            <div className="form-group">
              <label>Fitness Level</label>
              <select
                value={formData.fitness_level}
                onChange={(e) => setFormData({ ...formData, fitness_level: e.target.value })}
                className="form-control"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className="form-group">
              <label>Fitness Goals</label>
              <div>
                {goalOptions.map(goal => (
                  <label key={goal} style={{ display: 'inline-block', marginRight: '16px' }}>
                    <input
                      type="checkbox"
                      checked={formData.fitness_goals.includes(goal)}
                      onChange={() => handleCheckboxChange('fitness_goals', goal)}
                    />
                    {' '}{goal.replace('_', ' ')}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Available Equipment</label>
              <div>
                {equipmentOptions.map(equipment => (
                  <label key={equipment} style={{ display: 'inline-block', marginRight: '16px' }}>
                    <input
                      type="checkbox"
                      checked={formData.available_equipment.includes(equipment)}
                      onChange={() => handleCheckboxChange('available_equipment', equipment)}
                    />
                    {' '}{equipment}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Time per Session (minutes)</label>
              <input
                type="range"
                min="15"
                max="120"
                value={formData.time_per_session_minutes}
                onChange={(e) => setFormData({ ...formData, time_per_session_minutes: parseInt(e.target.value) })}
                className="form-control"
              />
              <span>{formData.time_per_session_minutes} minutes</span>
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
              <button type="submit" className="btn btn-primary" disabled={generating}>
                {generating ? 'Generating...' : 'Generate Program'}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => setShowGenerateForm(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {activeProgram && !showGenerateForm && (
        <div className="card">
          <h2>{activeProgram.name}</h2>
          <p>{activeProgram.description}</p>

          <div style={{ marginTop: '20px', padding: '16px', backgroundColor: '#e8f4f8', borderRadius: '8px' }}>
            <strong>AI Rationale:</strong>
            <p style={{ marginTop: '8px' }}>{activeProgram.ai_rationale}</p>
          </div>

          <div style={{ marginTop: '20px' }}>
            <p><strong>Type:</strong> {activeProgram.program_type === 'multi_week' ? 'Multi-Week Program' : 'Daily Workout'}</p>
            {activeProgram.duration_weeks && <p><strong>Duration:</strong> {activeProgram.duration_weeks} weeks</p>}
            <p><strong>Training Days:</strong> {activeProgram.days_per_week} days/week</p>
            <p><strong>Difficulty:</strong> {activeProgram.difficulty}</p>
            <p><strong>Status:</strong> <span className={`badge badge-${activeProgram.status === 'active' ? 'success' : 'primary'}`}>{activeProgram.status}</span></p>
          </div>

          <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
            {activeProgram.status === 'draft' && (
              <button
                className="btn btn-primary"
                onClick={() => handleAcceptProgram(activeProgram.id)}
              >
                Accept & Start Program
              </button>
            )}
            <button
              className="btn btn-secondary"
              onClick={() => setShowGenerateForm(true)}
            >
              Generate New Program
            </button>
          </div>
        </div>
      )}
    </div>
  );

  const renderTodayTab = () => {
    if (!todaysWorkout) {
      return (
        <div className="card">
          <p>No workout scheduled for today.</p>
        </div>
      );
    }

    return (
      <div className="card">
        <h2>{todaysWorkout.workout_name}</h2>
        <p><strong>Focus:</strong> {todaysWorkout.focus_areas.join(', ')}</p>
        <p><strong>Estimated Duration:</strong> {todaysWorkout.estimated_duration_minutes} minutes</p>

        {todaysWorkout.notes && (
          <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
            <strong>Coach's Notes:</strong> {todaysWorkout.notes}
          </div>
        )}

        <h3 style={{ marginTop: '24px', marginBottom: '16px' }}>Exercises</h3>

        {todaysWorkout.exercises && todaysWorkout.exercises.map((ex, idx) => (
          <div key={idx} className="card" style={{ marginBottom: '16px' }}>
            <h4>{idx + 1}. {ex.exercise.name}</h4>
            <p><strong>Sets:</strong> {ex.sets} | <strong>Reps:</strong> {Array.isArray(ex.reps) ? ex.reps.join(', ') : ex.reps} | <strong>Rest:</strong> {ex.rest_seconds}s</p>
            {ex.intensity_level && <p><strong>Intensity:</strong> {ex.intensity_level}</p>}
            {ex.notes && <p style={{ color: '#666', fontStyle: 'italic' }}>{ex.notes}</p>}
            <p style={{ marginTop: '8px' }}><strong>Target:</strong> {ex.exercise.muscle_groups.join(', ')}</p>
          </div>
        ))}
      </div>
    );
  };

  const renderProgramTab = () => {
    if (!activeProgram) return null;

    if (activeProgram.program_type === 'daily') {
      return renderTodayTab();
    }

    return (
      <div>
        <h2>{activeProgram.name}</h2>
        <p>{activeProgram.description}</p>

        {activeProgram.weekly_plans && activeProgram.weekly_plans.map(week => (
          <div key={week.id} className="card" style={{ marginTop: '20px' }}>
            <h3>Week {week.week_number}: {week.theme}</h3>
            {week.notes && <p style={{ color: '#666' }}>{week.notes}</p>}

            {week.daily_workouts && week.daily_workouts.map(workout => (
              <div key={workout.id} style={{ marginTop: '16px', padding: '12px', border: '1px solid #ddd', borderRadius: '4px' }}>
                <h4>Day {workout.day_number}: {workout.workout_name}</h4>
                <p><strong>Focus:</strong> {workout.focus_areas.join(', ')}</p>
                <p><strong>Duration:</strong> {workout.estimated_duration_minutes} min</p>

                {workout.exercises && workout.exercises.length > 0 && (
                  <ul style={{ marginTop: '8px' }}>
                    {workout.exercises.map((ex, idx) => (
                      <li key={idx}>
                        {ex.exercise.name} - {ex.sets}x{Array.isArray(ex.reps) ? ex.reps.join(',') : ex.reps} ({ex.rest_seconds}s rest)
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  const renderInsightsTab = () => (
    <div>
      <h2>Training Insights</h2>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        AI-powered analysis of your workout history and recommendations for improvement.
      </p>

      {insights.length === 0 ? (
        <div className="card">
          <p>No insights available yet. Keep logging workouts to get personalized recommendations!</p>
        </div>
      ) : (
        insights.map(insight => (
          <div key={insight.id} className="card" style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <span className={`badge badge-${insight.insight_type.includes('plateau') ? 'warning' : 'primary'}`}>
                  {insight.insight_type.replace('_', ' ')}
                </span>
                <h3 style={{ marginTop: '8px' }}>{insight.insight_text}</h3>
                {insight.recommendation && (
                  <p style={{ marginTop: '12px', padding: '12px', backgroundColor: '#d4edda', borderRadius: '4px' }}>
                    <strong>Recommendation:</strong> {insight.recommendation}
                  </p>
                )}
                <p style={{ marginTop: '12px', fontSize: '12px', color: '#999' }}>
                  {new Date(insight.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );

  if (loading) {
    return <div>Loading your training program...</div>;
  }

  return (
    <div>
      <h1>AI Personal Trainer</h1>
      {renderTabs()}

      {activeTab === 'overview' && renderOverviewTab()}
      {activeTab === 'today' && renderTodayTab()}
      {activeTab === 'program' && renderProgramTab()}
      {activeTab === 'insights' && renderInsightsTab()}
    </div>
  );
}

export default PersonalTrainer;
