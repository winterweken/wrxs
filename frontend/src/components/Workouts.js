import React, { useState, useEffect } from 'react';
import WorkoutPlans from './WorkoutPlans';
import WorkoutLogs from './WorkoutLogs';
import PersonalTrainer from './PersonalTrainer';
import PRHighlights from './PRHighlights';
import BodyMeasurements from './BodyMeasurements';
import ProgressPhotos from './ProgressPhotos';
import WeightProgressionChart from './WeightProgressionChart';

function Workouts({ token, user }) {
  const [activeTab, setActiveTab] = useState('logs');
  const [insights, setInsights] = useState([]);
  const [loadingInsights, setLoadingInsights] = useState(true);

  useEffect(() => {
    // Check for hash in URL to set initial tab
    const hash = window.location.hash.replace('#', '');
    if (hash && ['logs', 'plans', 'trainer', 'progress'].includes(hash)) {
      setActiveTab(hash);
    }
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/trainer/insights?limit=3', {
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
    } finally {
      setLoadingInsights(false);
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: '24px' }}>Workouts</h1>

      {/* Insights Section */}
      {!loadingInsights && insights.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ marginBottom: '16px' }}>Training Insights</h3>
          {insights.map(insight => (
            <div key={insight.id} className="card" style={{ marginBottom: '12px', backgroundColor: '#f8f9fa' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                <div style={{ flex: 1 }}>
                  <span className={`badge badge-${insight.insight_type.includes('plateau') || insight.insight_type.includes('recovery') ? 'warning' : 'primary'}`}>
                    {insight.insight_type.replace('_', ' ')}
                  </span>
                  <p style={{ marginTop: '8px', marginBottom: '8px', fontWeight: '500' }}>{insight.insight_text}</p>
                  {insight.recommendation && (
                    <p style={{ padding: '8px 12px', backgroundColor: '#d4edda', borderRadius: '4px', fontSize: '14px', marginTop: '8px' }}>
                      <strong>Recommendation:</strong> {insight.recommendation}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{
          display: 'flex',
          gap: '8px',
          borderBottom: '2px solid #e0e0e0',
          marginBottom: '24px'
        }}>
          <button
            onClick={() => setActiveTab('logs')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'logs' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'logs' ? '#007bff' : '#666',
              fontWeight: activeTab === 'logs' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            History
          </button>
          <button
            onClick={() => setActiveTab('plans')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'plans' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'plans' ? '#007bff' : '#666',
              fontWeight: activeTab === 'plans' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            Plans
          </button>
          <button
            onClick={() => setActiveTab('trainer')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'trainer' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'trainer' ? '#007bff' : '#666',
              fontWeight: activeTab === 'trainer' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            AI Trainer
          </button>
          <button
            onClick={() => setActiveTab('progress')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'progress' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'progress' ? '#007bff' : '#666',
              fontWeight: activeTab === 'progress' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            Progress
          </button>
        </div>
      </div>

      {activeTab === 'logs' && <WorkoutLogs token={token} />}
      {activeTab === 'plans' && <WorkoutPlans token={token} />}
      {activeTab === 'trainer' && <PersonalTrainer token={token} user={user} />}
      {activeTab === 'progress' && (
        <div>
          <PRHighlights token={token} />
          <WeightProgressionChart token={token} />
          <BodyMeasurements token={token} user={user} />
          <ProgressPhotos token={token} />
        </div>
      )}
    </div>
  );
}

export default Workouts;
