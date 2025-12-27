import React, { useState, useEffect } from 'react';
import AISuggestions from './AISuggestions';

function Profile({ token, user, onUpdate, onLogout }) {
  const [activeTab, setActiveTab] = useState('preferences');
  const [preferencesData, setPreferencesData] = useState({
    weight_unit: 'kg',
    distance_unit: 'km',
    measurement_unit: 'cm',
    age: '',
    height_cm: '',
    fitness_level: '',
    sex: ''
  });
  const [accountData, setAccountData] = useState({
    username: '',
    email: '',
    location: ''
  });
  const [gymProfiles, setGymProfiles] = useState([]);
  const [showGymForm, setShowGymForm] = useState(false);
  const [editingGymId, setEditingGymId] = useState(null);
  const [gymFormData, setGymFormData] = useState({
    name: '',
    gym_chain: '',
    equipment: []
  });
  const [editingUsername, setEditingUsername] = useState(false);
  const [editingEmail, setEditingEmail] = useState(false);
  const [editingLocation, setEditingLocation] = useState(false);
  const [message, setMessage] = useState('');

  const canadianGyms = [
    'Goodlife Fitness',
    'Hone Fitness',
    'Vive Fitness',
    'Fit4Less',
    'Anytime Fitness',
    'Planet Fitness',
    'YMCA',
    'Community Center',
    'Other'
  ];

  const equipmentOptions = [
    'Barbell',
    'Dumbbells',
    'Bench Press',
    'Squat Rack',
    'Pull-up Bar',
    'Cable Machine',
    'Leg Press',
    'Leg Extension',
    'Leg Curl',
    'Chest Press Machine',
    'Lat Pulldown',
    'Rowing Machine',
    'Treadmill',
    'Elliptical',
    'Stationary Bike',
    'Resistance Bands',
    'Kettlebells',
    'Smith Machine',
    'Dip Station',
    'Battle Ropes',
    'TRX/Suspension Trainer',
    'Medicine Balls',
    'Foam Roller'
  ];

  useEffect(() => {
    if (user) {
      setPreferencesData({
        weight_unit: user.weight_unit || 'kg',
        distance_unit: user.distance_unit || 'km',
        measurement_unit: user.measurement_unit || 'cm',
        age: user.age || '',
        height_cm: user.height_cm || '',
        fitness_level: user.fitness_level || '',
        sex: user.sex || ''
      });
      setAccountData({
        username: user.username || '',
        email: user.email || '',
        location: user.location || ''
      });
    }
    fetchGymProfiles();
  }, [user]);

  const fetchGymProfiles = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/gym-profiles', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setGymProfiles(data);
      }
    } catch (error) {
      console.error('Error fetching gym profiles:', error);
    }
  };

  const handlePreferencesChange = (e) => {
    setPreferencesData({
      ...preferencesData,
      [e.target.name]: e.target.value
    });
  };

  const handleAccountChange = (e) => {
    setAccountData({
      ...accountData,
      [e.target.name]: e.target.value
    });
  };

  const handleGymFormChange = (e) => {
    setGymFormData({
      ...gymFormData,
      [e.target.name]: e.target.value
    });
  };

  const handleEquipmentToggle = (equipment) => {
    const currentEquipment = gymFormData.equipment || [];
    if (currentEquipment.includes(equipment)) {
      setGymFormData({
        ...gymFormData,
        equipment: currentEquipment.filter(e => e !== equipment)
      });
    } else {
      setGymFormData({
        ...gymFormData,
        equipment: [...currentEquipment, equipment]
      });
    }
  };

  const handlePreferencesSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const updateData = {
        ...preferencesData,
        age: preferencesData.age ? parseInt(preferencesData.age) : null,
        height_cm: preferencesData.height_cm ? parseFloat(preferencesData.height_cm) : null
      };

      const response = await fetch('http://localhost:8000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        setMessage('Preferences updated successfully!');
        onUpdate();
      } else {
        setMessage('Failed to update preferences');
      }
    } catch (error) {
      setMessage('Error updating preferences');
    }
  };

  const handleUsernameSubmit = async () => {
    setMessage('');
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: accountData.username })
      });

      if (response.ok) {
        setMessage('Username updated successfully!');
        setEditingUsername(false);
        onUpdate();
      } else {
        setMessage('Failed to update username');
      }
    } catch (error) {
      setMessage('Error updating username');
    }
  };

  const handleEmailSubmit = async () => {
    setMessage('');
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: accountData.email })
      });

      if (response.ok) {
        setMessage('Email updated successfully!');
        setEditingEmail(false);
        onUpdate();
      } else {
        setMessage('Failed to update email');
      }
    } catch (error) {
      setMessage('Error updating email');
    }
  };

  const handleLocationSubmit = async () => {
    setMessage('');
    try {
      const response = await fetch('http://localhost:8000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location: accountData.location })
      });

      if (response.ok) {
        setMessage('Location updated successfully!');
        setEditingLocation(false);
        onUpdate();
      } else {
        setMessage('Failed to update location');
      }
    } catch (error) {
      setMessage('Error updating location');
    }
  };

  const handleGymFormSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const url = editingGymId
        ? `http://localhost:8000/api/gym-profiles/${editingGymId}`
        : 'http://localhost:8000/api/gym-profiles';

      const method = editingGymId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(gymFormData)
      });

      if (response.ok) {
        setMessage(editingGymId ? 'Gym profile updated!' : 'Gym profile created!');
        setShowGymForm(false);
        setEditingGymId(null);
        setGymFormData({ name: '', gym_chain: '', equipment: [] });
        fetchGymProfiles();
      } else {
        setMessage('Failed to save gym profile');
      }
    } catch (error) {
      setMessage('Error saving gym profile');
    }
  };

  const handleEditGym = (gym) => {
    setEditingGymId(gym.id);
    setGymFormData({
      name: gym.name,
      gym_chain: gym.gym_chain || '',
      equipment: gym.equipment || []
    });
    setShowGymForm(true);
  };

  const handleDeleteGym = async (gymId) => {
    if (!window.confirm('Delete this gym profile?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/gym-profiles/${gymId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok || response.status === 204) {
        setMessage('Gym profile deleted!');
        fetchGymProfiles();
      } else {
        setMessage('Failed to delete gym profile');
      }
    } catch (error) {
      setMessage('Error deleting gym profile');
    }
  };

  const experienceLevelOptions = [
    { value: 'complete_beginner', label: 'Complete Beginner (0-6 months)' },
    { value: 'beginner', label: 'Beginner (6-12 months)' },
    { value: 'novice', label: 'Novice (1-2 years)' },
    { value: 'intermediate', label: 'Intermediate (2-4 years)' },
    { value: 'advanced', label: 'Advanced (4+ years)' },
    { value: 'expert', label: 'Expert/Athlete (Professional)' }
  ];

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ marginBottom: '16px' }}>Profile</h1>
        <div style={{
          display: 'flex',
          gap: '8px',
          borderBottom: '2px solid #e0e0e0',
          marginBottom: '24px'
        }}>
          <button
            onClick={() => setActiveTab('preferences')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'preferences' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'preferences' ? '#007bff' : '#666',
              fontWeight: activeTab === 'preferences' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            Preferences
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'settings' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'settings' ? '#007bff' : '#666',
              fontWeight: activeTab === 'settings' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            Settings
          </button>
          <button
            onClick={() => setActiveTab('ai')}
            style={{
              padding: '12px 24px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'ai' ? '3px solid #007bff' : '3px solid transparent',
              color: activeTab === 'ai' ? '#007bff' : '#666',
              fontWeight: activeTab === 'ai' ? '600' : '400',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '-2px'
            }}
          >
            AI Suggestions
          </button>
        </div>
      </div>

      {activeTab === 'preferences' && (
        <div>
          <div className="card">
            <h3 style={{ marginBottom: '20px' }}>Preferences</h3>
            <form onSubmit={handlePreferencesSubmit}>
              <div className="form-group">
                <label>Weight Units</label>
                <select
                  name="weight_unit"
                  value={preferencesData.weight_unit}
                  onChange={handlePreferencesChange}
                >
                  <option value="kg">Kilograms (kg)</option>
                  <option value="lbs">Pounds (lbs)</option>
                </select>
              </div>

              <div className="form-group">
                <label>Distance Units</label>
                <select
                  name="distance_unit"
                  value={preferencesData.distance_unit}
                  onChange={handlePreferencesChange}
                >
                  <option value="km">Kilometers (km)</option>
                  <option value="miles">Miles</option>
                </select>
              </div>

              <div className="form-group">
                <label>Body Measurement Units</label>
                <select
                  name="measurement_unit"
                  value={preferencesData.measurement_unit}
                  onChange={handlePreferencesChange}
                >
                  <option value="cm">Centimeters (cm)</option>
                  <option value="in">Inches (in)</option>
                </select>
              </div>

              <div className="form-group">
                <label>Age</label>
                <input
                  type="number"
                  name="age"
                  value={preferencesData.age}
                  onChange={handlePreferencesChange}
                  min="1"
                  max="120"
                />
              </div>

              <div className="form-group">
                <label>Height ({preferencesData.measurement_unit})</label>
                <input
                  type="number"
                  step="0.1"
                  name="height_cm"
                  value={preferencesData.height_cm}
                  onChange={handlePreferencesChange}
                />
              </div>

              <div className="form-group">
                <label>Sex</label>
                <select
                  name="sex"
                  value={preferencesData.sex}
                  onChange={handlePreferencesChange}
                >
                  <option value="">Select</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>

              <div className="form-group">
                <label>Experience Level</label>
                <select
                  name="fitness_level"
                  value={preferencesData.fitness_level}
                  onChange={handlePreferencesChange}
                >
                  <option value="">Select level</option>
                  {experienceLevelOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              {message && (
                <div className={message.includes('success') ? 'success' : 'error'} style={{ marginBottom: '16px' }}>
                  {message}
                </div>
              )}

              <button type="submit" className="btn btn-primary">Save Preferences</button>
            </form>
          </div>

          {/* Gyms and Equipment Section */}
          <div className="card" style={{ marginTop: '24px' }}>
            <h3 style={{ marginBottom: '20px' }}>Gyms and Equipment</h3>

            {!showGymForm && (
              <button
                className="btn btn-primary"
                onClick={() => {
                  setShowGymForm(true);
                  setEditingGymId(null);
                  setGymFormData({ name: '', gym_chain: '', equipment: [] });
                }}
                style={{ marginBottom: '20px' }}
              >
                Add Equipment
              </button>
            )}

            {showGymForm && (
              <div className="card" style={{ backgroundColor: '#f8f9fa', marginBottom: '20px' }}>
                <h4 style={{ marginBottom: '16px' }}>{editingGymId ? 'Edit' : 'Add'} Gym Profile</h4>
                <form onSubmit={handleGymFormSubmit}>
                  <div className="form-group">
                    <label>Name</label>
                    <input
                      type="text"
                      name="name"
                      value={gymFormData.name}
                      onChange={handleGymFormChange}
                      required
                      placeholder="e.g., My Home Gym, Downtown Goodlife"
                    />
                  </div>

                  <div className="form-group">
                    <label>Gym Chain (Optional)</label>
                    <select
                      name="gym_chain"
                      value={gymFormData.gym_chain}
                      onChange={handleGymFormChange}
                    >
                      <option value="">Select gym chain</option>
                      {canadianGyms.map(gym => (
                        <option key={gym} value={gym}>{gym}</option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Available Equipment</label>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                      gap: '8px',
                      marginTop: '8px',
                      maxHeight: '300px',
                      overflowY: 'auto',
                      padding: '8px',
                      border: '1px solid #ddd',
                      borderRadius: '4px'
                    }}>
                      {equipmentOptions.map(equipment => (
                        <label key={equipment} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                          <input
                            type="checkbox"
                            checked={gymFormData.equipment.includes(equipment)}
                            onChange={() => handleEquipmentToggle(equipment)}
                            style={{ marginRight: '8px' }}
                          />
                          {equipment}
                        </label>
                      ))}
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button type="submit" className="btn btn-primary">
                      {editingGymId ? 'Update' : 'Save'} Profile
                    </button>
                    <button
                      type="button"
                      className="btn btn-secondary"
                      onClick={() => {
                        setShowGymForm(false);
                        setEditingGymId(null);
                        setGymFormData({ name: '', gym_chain: '', equipment: [] });
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}

            {gymProfiles.length > 0 ? (
              <div>
                {gymProfiles.map(gym => (
                  <div key={gym.id} className="card" style={{ backgroundColor: '#f8f9fa', marginBottom: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                      <div style={{ flex: 1 }}>
                        <h4 style={{ marginBottom: '8px' }}>{gym.name}</h4>
                        {gym.gym_chain && (
                          <p style={{ color: '#666', marginBottom: '8px' }}>{gym.gym_chain}</p>
                        )}
                        <p style={{ fontSize: '14px', color: '#666' }}>
                          <strong>Equipment:</strong> {gym.equipment.join(', ')}
                        </p>
                      </div>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '4px 12px', fontSize: '14px' }}
                          onClick={() => handleEditGym(gym)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '4px 12px', fontSize: '14px' }}
                          onClick={() => handleDeleteGym(gym.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : !showGymForm && (
              <p style={{ color: '#666', textAlign: 'center', padding: '20px' }}>
                No gym profiles yet. Add your first gym to track available equipment.
              </p>
            )}
          </div>
        </div>
      )}

      {activeTab === 'settings' && (
        <div>
          <div className="card">
            <h3 style={{ marginBottom: '20px' }}>Account Info</h3>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <strong>Username</strong>
                {!editingUsername && (
                  <button
                    onClick={() => setEditingUsername(true)}
                    className="btn btn-secondary"
                    style={{ padding: '4px 12px', fontSize: '14px' }}
                  >
                    Edit
                  </button>
                )}
              </div>
              {editingUsername ? (
                <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                  <input
                    type="text"
                    name="username"
                    value={accountData.username}
                    onChange={handleAccountChange}
                    style={{ flex: 1 }}
                  />
                  <button onClick={handleUsernameSubmit} className="btn btn-primary" style={{ padding: '8px 16px' }}>
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setEditingUsername(false);
                      setAccountData({ ...accountData, username: user?.username || '' });
                    }}
                    className="btn btn-secondary"
                    style={{ padding: '8px 16px' }}
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <p>{user?.username || 'Not set'}</p>
              )}
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <strong>Location</strong>
                {!editingLocation && (
                  <button
                    onClick={() => setEditingLocation(true)}
                    className="btn btn-secondary"
                    style={{ padding: '4px 12px', fontSize: '14px' }}
                  >
                    Edit
                  </button>
                )}
              </div>
              {editingLocation ? (
                <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                  <input
                    type="text"
                    name="location"
                    value={accountData.location}
                    onChange={handleAccountChange}
                    placeholder="e.g., Toronto, ON"
                    style={{ flex: 1 }}
                  />
                  <button onClick={handleLocationSubmit} className="btn btn-primary" style={{ padding: '8px 16px' }}>
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setEditingLocation(false);
                      setAccountData({ ...accountData, location: user?.location || '' });
                    }}
                    className="btn btn-secondary"
                    style={{ padding: '8px 16px' }}
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <p>{user?.location || 'Not set'}</p>
              )}
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <strong>Email</strong>
                {!editingEmail && (
                  <button
                    onClick={() => setEditingEmail(true)}
                    className="btn btn-secondary"
                    style={{ padding: '4px 12px', fontSize: '14px' }}
                  >
                    Edit
                  </button>
                )}
              </div>
              {editingEmail ? (
                <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                  <input
                    type="email"
                    name="email"
                    value={accountData.email}
                    onChange={handleAccountChange}
                    style={{ flex: 1 }}
                  />
                  <button onClick={handleEmailSubmit} className="btn btn-primary" style={{ padding: '8px 16px' }}>
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setEditingEmail(false);
                      setAccountData({ ...accountData, email: user?.email || '' });
                    }}
                    className="btn btn-secondary"
                    style={{ padding: '8px 16px' }}
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <p>{user?.email || 'Not set'}</p>
              )}
            </div>

            <div style={{ marginBottom: '24px' }}>
              <strong>Joined</strong>
              <p>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Not available'}</p>
            </div>

            {message && (
              <div className={message.includes('success') ? 'success' : 'error'} style={{ marginBottom: '16px' }}>
                {message}
              </div>
            )}

            <button
              className="btn btn-secondary"
              style={{ marginBottom: '12px', width: '100%' }}
              onClick={() => alert('Apple Health sync coming soon!')}
            >
              Sync with Apple Health
            </button>

            <button onClick={onLogout} className="btn btn-danger" style={{ width: '100%' }}>
              Sign Out
            </button>
          </div>
        </div>
      )}

      {activeTab === 'ai' && <AISuggestions token={token} />}
    </div>
  );
}

export default Profile;
