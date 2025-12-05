import React, { useEffect, useState } from 'react';
import { backendApi } from '../api/axios';
import type { User } from '../types';

const StudentDashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const { data: userData } = await backendApi.get<User>('/api/v1/auth/me');
      setUser(userData);
      // Ideally fetch student details linked to this user.
      // Since the backend 'me' endpoint might not return student details directly,
      // we might need another endpoint or assume the user is linked.
      // For now, we just show the user info.
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Student Dashboard</h2>
      {user && (
        <div className="card mt-3">
          <div className="card-body">
            <h5 className="card-title">Welcome, {user.email}</h5>
            <p className="card-text">
              Role: <span className="badge bg-secondary">{user.role}</span>
            </p>
            <hr />
            <h5>My Attendance</h5>
            <div className="alert alert-warning">
              Attendance records are not yet available.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentDashboard;
