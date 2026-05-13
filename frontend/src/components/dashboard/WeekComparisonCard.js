import React, { useState, useEffect } from 'react';

function WeekComparisonCard({ token }) {
  const [comparison, setComparison] = useState(null);

  useEffect(() => {
    fetchComparison();
  }, [token]);

  const fetchComparison = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/week-comparison', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setComparison(await response.json());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!comparison) return null;

  const StatComparison = ({ label, current, change, percent }) => {
    const isPositive = change > 0;
    const isNeutral = change === 0;

    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>{label}</div>
        <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#333' }}>
          {current}
        </div>
        <div style={{
          fontSize: '14px',
          color: isNeutral ? '#666' : isPositive ? '#28a745' : '#f57c00',
          marginTop: '4px'
        }}>
          {isPositive && '↑ '}
          {!isPositive && !isNeutral && '↓ '}
          {Math.abs(change)} ({Math.abs(percent)}%)
        </div>
      </div>
    );
  };

  return (
    <div className="card">
      <h3>This Week vs Last Week</h3>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
        gap: '20px',
        marginTop: '20px'
      }}>
        <StatComparison
          label="Workouts"
          current={comparison.current_week.total_workouts}
          change={comparison.comparison.workouts.change}
          percent={comparison.comparison.workouts.percent}
        />
        <StatComparison
          label="Sets"
          current={comparison.current_week.total_sets}
          change={comparison.comparison.sets.change}
          percent={comparison.comparison.sets.percent}
        />
        <StatComparison
          label="Volume (kg)"
          current={comparison.current_week.total_volume_kg}
          change={comparison.comparison.volume.change}
          percent={comparison.comparison.volume.percent}
        />
        <StatComparison
          label="Days Active"
          current={comparison.current_week.workout_days}
          change={comparison.comparison.workout_days.change}
          percent={comparison.comparison.workout_days.percent}
        />
      </div>
    </div>
  );
}

export default WeekComparisonCard;
