import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function FrequencyChart({ token }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, [token]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/dashboard/frequency-chart?weeks=12', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setData(await response.json());
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (!data || data.weeks.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
        <p style={{ color: '#666' }}>No workout data yet - start tracking to see your progress!</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>Workout Frequency (Last 12 Weeks)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data.weeks}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week_label" tick={{ fontSize: 12 }} />
          <YAxis label={{ value: 'Workouts', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Bar dataKey="workout_count" fill="#007bff" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>

      <div style={{ marginTop: '16px', textAlign: 'center' }}>
        <span style={{
          padding: '8px 16px',
          borderRadius: '16px',
          backgroundColor: data.trend === 'increasing' ? '#e8f5e9' : '#fff3e0',
          color: data.trend === 'increasing' ? '#388e3c' : '#f57c00',
          fontWeight: '500'
        }}>
          {data.trend === 'increasing' && '📈 Trending Up!'}
          {data.trend === 'stable' && '➡️ Staying Consistent'}
          {data.trend === 'decreasing' && '📉 Let\'s pick it back up!'}
        </span>
      </div>
    </div>
  );
}

export default FrequencyChart;
