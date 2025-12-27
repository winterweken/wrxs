import React, { useState } from 'react';
import WorkoutPlans from './WorkoutPlans';
import WorkoutLogs from './WorkoutLogs';

function Workouts({ token }) {
  const [activeTab, setActiveTab] = useState('logs');

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ marginBottom: '16px' }}>Workouts</h1>
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
        </div>
      </div>

      {activeTab === 'logs' && <WorkoutLogs token={token} />}
      {activeTab === 'plans' && <WorkoutPlans token={token} />}
    </div>
  );
}

export default Workouts;
