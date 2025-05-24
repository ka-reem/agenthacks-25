import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Github, ArrowRight, ArrowLeft } from 'lucide-react';

const EmailForm: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-md mx-auto card scale-in">
      <div className="flex items-center justify-center mb-6">
        <Github className="text-indigo-400 mr-2" size={24} />
        <h2 className="text-2xl font-bold">GitHub Account</h2>
      </div>
      
      <div className="text-center mb-8">
        <p className="text-lg mb-2">Logged in as</p>
        <p className="text-2xl font-bold text-indigo-400 mb-4">ka-reem</p>
        <p className="text-sm text-slate-400">via GitHub</p>
      </div>
      
      <div className="flex justify-between">
        <button
          onClick={() => navigate('/')}
          className="btn bg-slate-700 hover:bg-slate-600 text-white"
        >
          <ArrowLeft className="mr-2" />
          Back
        </button>
        
        <button 
          onClick={() => navigate('/select-hackathon')} 
          className="btn btn-primary"
        >
          Continue
          <ArrowRight className="ml-2" />
        </button>
      </div>
      
      <button 
        onClick={() => alert('Change account functionality coming soon!')}
        className="w-full mt-4 text-sm text-slate-400 hover:text-slate-300 transition-colors"
      >
        Change account
      </button>
    </div>
  );
};

export default EmailForm;