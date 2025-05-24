import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Code, ArrowRight, Github } from 'lucide-react';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="fade-in">
      <div className="text-center max-w-3xl mx-auto">
        <div className="mb-8">
          <Code size={64} className="text-indigo-500 mx-auto" />
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold mb-6">Welcome to Cheatathon</h1>
        <p className="text-xl text-slate-300 mb-4">
          Create a winning hackathon project in minutes. No coding required.
        </p>
        <p className="text-md text-slate-400 mb-8">
          Logged in as <span className="text-indigo-400">ka-reem</span> via GitHub
        </p>
        <button
          onClick={() => navigate('/email')}
          className="btn btn-primary text-lg group"
        >
          Hack the Hackathon
          <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>

      <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="card">
          <h3 className="text-xl font-bold mb-3">Quick Setup</h3>
          <p className="text-slate-300">
            Enter your GitHub email, select a hackathon, and we'll handle the rest.
          </p>
        </div>
        <div className="card">
          <h3 className="text-xl font-bold mb-3">Realistic Commits</h3>
          <p className="text-slate-300">
            We generate a realistic commit history that looks like a genuine hackathon project.
          </p>
        </div>
        <div className="card">
          <h3 className="text-xl font-bold mb-3">Ready to Submit</h3>
          <p className="text-slate-300">
            Your repository will be ready to submit to the hackathon of your choice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;