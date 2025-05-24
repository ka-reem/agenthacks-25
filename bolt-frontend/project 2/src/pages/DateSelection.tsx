import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, ArrowRight, ArrowLeft, Clock } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

const DateSelection: React.FC = () => {
  const { setCommitDate } = useAppContext();
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const [startDate, setStartDate] = useState('2025-05-23');
  const [startTime, setStartTime] = useState('18:55');
  const [endDate, setEndDate] = useState('2025-05-24');
  const [endTime, setEndTime] = useState('11:00');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!startDate || !endDate || !startTime || !endTime) {
      setError('All fields are required');
      return;
    }
    
    const start = new Date(`${startDate}T${startTime}`);
    const end = new Date(`${endDate}T${endTime}`);
    
    if (end <= start) {
      setError('End date/time must be after start date/time');
      return;
    }
    
    setCommitDate(JSON.stringify({ start: start.toISOString(), end: end.toISOString() }));
    navigate('/build');
  };

  return (
    <div className="max-w-md mx-auto card scale-in">
      <h2 className="text-2xl font-bold mb-6 flex items-center">
        <Calendar className="mr-2 text-green-400" />
        Select Commit Time Range
      </h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <div className="mb-6">
            <h3 className="text-lg font-medium mb-4 flex items-center">
              <Clock className="mr-2" size={20} />
              Start Date/Time
            </h3>
            <input
              type="date"
              value={startDate}
              onChange={(e) => {
                setStartDate(e.target.value);
                setError('');
              }}
              className="form-input w-full mb-2"
            />
            <input
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              className="form-input w-full"
            />
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-medium mb-4 flex items-center">
              <Clock className="mr-2" size={20} />
              End Date/Time
            </h3>
            <input
              type="date"
              value={endDate}
              onChange={(e) => {
                setEndDate(e.target.value);
                setError('');
              }}
              className="form-input w-full mb-2"
            />
            <input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="form-input w-full"
            />
          </div>
          
          {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
          <p className="mt-2 text-sm text-slate-400">
            Commits will be distributed across this time range.
          </p>
        </div>
        
        <div className="flex justify-between">
          <button
            type="button"
            onClick={() => navigate('/select-hackathon')}
            className="btn bg-slate-700 hover:bg-slate-600 text-white"
          >
            <ArrowLeft className="mr-2" />
            Back
          </button>
          
          <button type="submit" className="btn btn-primary">
            Generate Project
            <ArrowRight className="ml-2" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default DateSelection;