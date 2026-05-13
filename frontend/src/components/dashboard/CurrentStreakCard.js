import React, { useState, useEffect } from 'react';

function CurrentStreakCard({ token }) {
  const [streak, setStreak] = useState(null);

  useEffect(() => {
    fetchStreak();
  }, [token]);

  const fetchStreak = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/current-streak', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setStreak(await response.json());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!streak) return null;

  return (
    <div className="card" style={{
      background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      color: 'white',
      textAlign: 'center'
    }}>
      <div style={{ fontSize: '72px' }}>
        {streak.current_streak > 0 ? '🔥' : '💤'}
      </div>
      <div style={{ fontSize: '56px', fontWeight: 'bold', marginTop: '8px' }}>
        {streak.current_streak}
      </div>
      <div style={{ fontSize: '20px', marginTop: '8px' }}>
        Day{streak.current_streak !== 1 ? 's' : ''} Streak
      </div>
      <div style={{ marginTop: '16px', fontSize: '14px', opacity: 0.9 }}>
        Personal Best: {streak.longest_streak} days
      </div>
    </div>
  );
}

export default CurrentStreakCard;
