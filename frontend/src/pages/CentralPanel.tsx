import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { faceApi, backendApi } from '../api/axios';
import type { Student } from '../types';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const WebcamComponent = Webcam as any;

const CentralPanel: React.FC = () => {
  const webcamRef = useRef<Webcam>(null);
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [match, setMatch] = useState<{ student: Student; confidence: number; attendance?: any; error?: string } | null>(null);
  const [error, setError] = useState('');

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImgSrc(imageSrc);
      handleRecognize(imageSrc);
    }
  }, [webcamRef]);

  const handleRecognize = async (base64Image: string | null) => {
    if (!base64Image) return;
    setLoading(true);
    setMatch(null);
    setError('');

    try {
      // Convert base64 to blob
      const res = await fetch(base64Image);
      const blob = await res.blob();
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });

      const formData = new FormData();
      formData.append('file', file);

      const { data } = await faceApi.post('/recognize', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (data.matches && data.matches.length > 0) {
        const bestMatch = data.matches[0]; // { student_id: int, confidence: float }
        
        // Mark Attendance in Backend
        try {
          const { data: attendanceData } = await backendApi.post('/api/v1/attendance/mark', {
            student_id: bestMatch.student_id,
            confidence: bestMatch.confidence
          });
          
           // Fetch student details for display
          const { data: student } = await backendApi.get<Student>(`/api/v1/students/${bestMatch.student_id}`);
          setMatch({ student, confidence: bestMatch.confidence, attendance: attendanceData });
          
        } catch (attendanceErr: any) {
           console.error("Attendance marking failed", attendanceErr);
           // Still show the student but maybe with a warning
           const { data: student } = await backendApi.get<Student>(`/api/v1/students/${bestMatch.student_id}`);
           setMatch({ 
             student, 
             confidence: bestMatch.confidence, 
             error: attendanceErr.response?.data?.detail || "Attendance marking failed" 
            });
        }

      } else {
        setError('No match found');
      }
    } catch (err: any) {
      console.error(err);
      if (err.response && err.response.status === 404) {
        setError('No face matched');
      } else {
        setError('Recognition failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setImgSrc(null);
    setMatch(null);
    setError('');
  };

  return (
    <div className="container mt-4 text-center">
      <h2>Central Attendance Panel</h2>
      <p className="text-muted">Please look at the camera to mark your attendance.</p>

      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-lg">
            <div className="card-body p-0 position-relative">
              {!imgSrc ? (
                <WebcamComponent
                  audio={false}
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  width="100%"
                  videoConstraints={{ facingMode: "user" }}
                />
              ) : (
                <img src={imgSrc} alt="Captured" className="img-fluid" />
              )}
              
              {loading && (
                <div className="position-absolute top-50 start-50 translate-middle">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
              )}
            </div>
            <div className="card-footer bg-white">
              {!imgSrc ? (
                <button className="btn btn-primary btn-lg px-5" onClick={capture}>Scan Face</button>
              ) : (
                <button className="btn btn-secondary" onClick={reset}>Scan Again</button>
              )}
            </div>
          </div>

          {match && (
            <div className={`alert ${match.error ? 'alert-warning' : 'alert-success'} mt-4`}>
              <h4 className="alert-heading">{match.error ? 'Recognized but Attendance Failed' : 'Attendance Marked!'}</h4>
              <p className="mb-0">Welcome, <strong>{match.student.full_name}</strong></p>
              <small>Student ID: {match.student.student_id} | Confidence: {(match.confidence * 100).toFixed(1)}%</small>
              {match.attendance && (
                <div className="mt-2">
                  <strong>Class:</strong> {match.attendance.class_name} <br/>
                  <strong>Subject:</strong> {match.attendance.subject_name} <br/>
                  <strong>Time:</strong> {new Date(match.attendance.time_in).toLocaleTimeString()}
                </div>
              )}
              {match.error && (
                <div className="mt-2 text-danger">
                  <strong>Error:</strong> {match.error}
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="alert alert-danger mt-4">
              {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CentralPanel;
