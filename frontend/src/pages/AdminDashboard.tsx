import React, { useEffect, useState } from 'react';
import { backendApi, faceApi } from '../api/axios';
import type { Student } from '../types';

const AdminDashboard: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [activeTab, setActiveTab] = useState('students');
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    student_id: '',
    full_name: '',
    email: '',
    phone: '',
    department: '',
    class_name: '',
    year: '',
    division: '',
    roll_number: '',
  });
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const { data } = await backendApi.get<Student[]>('/api/v1/students/');
      setStudents(data);
    } catch (err) {
      console.error('Failed to fetch students', err);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiles(e.target.files);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // 1. Create Student in Backend
      const { data: newStudent } = await backendApi.post<Student>('/api/v1/students/', formData);
      
      // 2. Register Face in Face Service
      if (files && files.length > 0) {
        const faceFormData = new FormData();
        faceFormData.append('student_id', newStudent.id.toString());
        Array.from(files).forEach((file) => {
          faceFormData.append('files', file);
        });

        await faceApi.post('/register', faceFormData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      }

      alert('Student added successfully!');
      setShowAddModal(false);
      fetchStudents();
      setFormData({
        student_id: '',
        full_name: '',
        email: '',
        phone: '',
        department: '',
        class_name: '',
        year: '',
        division: '',
        roll_number: '',
      });
      setFiles(null);
    } catch (err) {
      console.error('Error adding student', err);
      alert('Failed to add student. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure?')) return;
    try {
      await backendApi.delete(`/api/v1/students/${id}`);
      fetchStudents();
    } catch (err) {
      console.error(err);
      alert('Failed to delete student');
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Admin Dashboard</h2>
      
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'students' ? 'active' : ''}`}
            onClick={() => setActiveTab('students')}
          >
            Students
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'timetable' ? 'active' : ''}`}
            onClick={() => setActiveTab('timetable')}
          >
            Timetable
          </button>
        </li>
      </ul>

      {activeTab === 'students' && (
        <div>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h4>Student List</h4>
            <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>Add Student</button>
          </div>

          {showAddModal && (
            <div className="card mb-4 p-4 bg-light">
              <h5>Add New Student</h5>
              <form onSubmit={handleSubmit}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Full Name</label>
                    <input name="full_name" className="form-control" required onChange={handleInputChange} value={formData.full_name} />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label className="form-label">Email</label>
                    <input name="email" type="email" className="form-control" required onChange={handleInputChange} value={formData.email} />
                  </div>
                  <div className="col-md-4 mb-3">
                    <label className="form-label">Student ID (Roll No/Unique)</label>
                    <input name="student_id" className="form-control" required onChange={handleInputChange} value={formData.student_id} />
                  </div>
                  <div className="col-md-4 mb-3">
                    <label className="form-label">Department</label>
                    <input name="department" className="form-control" onChange={handleInputChange} value={formData.department} />
                  </div>
                  <div className="col-md-4 mb-3">
                    <label className="form-label">Class</label>
                    <input name="class_name" className="form-control" onChange={handleInputChange} value={formData.class_name} />
                  </div>
                   <div className="col-md-12 mb-3">
                    <label className="form-label">Face Images (Required for Recognition)</label>
                    <input type="file" multiple className="form-control" onChange={handleFileChange} accept="image/*" required />
                    <div className="form-text">Upload clear photos of the student's face.</div>
                  </div>
                </div>
                <button type="submit" className="btn btn-success" disabled={loading}>
                  {loading ? 'Saving...' : 'Save Student'}
                </button>
                <button type="button" className="btn btn-secondary ms-2" onClick={() => setShowAddModal(false)}>Cancel</button>
              </form>
            </div>
          )}

          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Dept</th>
                <th>Class</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.id}>
                  <td>{student.student_id}</td>
                  <td>{student.full_name}</td>
                  <td>{student.email}</td>
                  <td>{student.department}</td>
                  <td>{student.class_name}</td>
                  <td>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(student.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'timetable' && (
        <div className="alert alert-info">
          Timetable management functionality is coming soon.
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
