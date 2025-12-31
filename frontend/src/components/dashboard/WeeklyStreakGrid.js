import React, { useState, useEffect } from 'react';

function WeeklyStreakGrid({ token }) {
  const [weekData, setWeekData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWeeklyStreak();
  }, [token]);

  const fetchWeeklyStreak = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/weekly-streak', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setWeekData(await response.json());
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getIntensityColor = (count) => {
    if (count === 0) return '#ebedf0';
    if (count === 1) return '#9be9a8';
    if (count === 2) return '#40c463';
    return '#30a14e';
  };

  if (loading || !weekData) return <div className="loading">Loading...</div>;

  return (
    <div className="card">
      <h3>This Week's Activity ({weekData.week_start} to {weekData.week_end})</h3>
      <div style={{
        display: 'flex',
        gap: '8px',
        justifyContent: 'center',
        marginTop: '20px',
        flexWrap: 'wrap'
      }}>
        {weekData.days.map((day) => (
          <div
            key={day.date}
            style={{
              width: '60px',
              height: '60px',
              backgroundColor: getIntensityColor(day.workout_count),
              borderRadius: '6px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'transform 0.2s'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
          >
            <div style={{ fontSize: '11px', fontWeight: 'bold', marginBottom: '4px' }}>
              {day.day_name.slice(0, 3)}
            </div>
            {day.has_workout && <span style={{ fontSize: '20px' }}>✓</span>}
          </div>
        ))}
      </div>
      <p style={{ textAlign: 'center', marginTop: '16px', color: '#666' }}>
        {weekData.total_workout_days} workout days this week
      </p>
    </div>
  );
}

export default WeeklyStreakGrid;
