import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const UserProfile: React.FC = () => {
  const [userData, setUserData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    const userId = localStorage.getItem('user_id');

    if (!userId) {
      navigate('/signin');
      return;
    }

    fetch(`/api/profile?user_id=${userId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
        } else {
          setUserData(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to load profile');
        setLoading(false);
      });
  }, [navigate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="profile-page">
      <h1>User Profile</h1>
      {userData.image_url && (
        <img src={userData.image_url} alt="User profile" className="profile-image" />
      )}
      <p><strong>Name:</strong> {userData.name}</p>
      <p><strong>Email:</strong> {userData.email}</p>

      {/* Display Skills */}
      <div>
        <strong>Skills:</strong>
        <ul>
          {userData.skills.length === 0 ? (
            <li>No skills listed</li>
          ) : (
            userData.skills.map((skill: string, index: number) => (
              <li key={index}>{skill}</li>
            ))
          )}
        </ul>
      </div>

      <button onClick={() => {
        localStorage.removeItem('user_id');
        navigate('/signin');
      }}>Log Out</button>
    </div>
  );
};

export default UserProfile;
