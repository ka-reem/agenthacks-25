import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, Github, Home } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

const Completion: React.FC = () => {
  const { isProcessComplete, selectedHackathon } = useAppContext();
  const navigate = useNavigate();

  // Redirect to home if process is not complete
  React.useEffect(() => {
    if (!isProcessComplete) {
      navigate('/');
    }
  }, [isProcessComplete, navigate]);

  const getHackathonName = () => {
    switch (selectedHackathon) {
      case 'treehacks': return 'Tree Hacks';
      case 'calhacks': return 'Cal Hacks';
      case 'berkeley-ai': return 'UC Berkeley AI Hackathon 2024';
      case 'stanford-ai': return 'Stanford AI Hackathon';
      case 'mit-hack': return 'MIT Hack';
      case 'hackmit': return 'HackMIT';
      default: return 'the hackathon';
    }
  };

  return (
    <div className="max-w-xl mx-auto text-center scale-in">
      <div className="card">
        <CheckCircle size={64} className="text-green-500 mx-auto mb-4" />
        <h2 className="text-3xl font-bold mb-4">Success!</h2>
        <p className="text-lg mb-6">
          Your project for {getHackathonName()} has been successfully created and is ready for submission!
        </p>
        
        <div className="mb-8">
          <a
            href="https://github.com/ka-reem/agenthacks-25/tree/stolen_rewritten"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary"
          >
            <Github className="mr-2" />
            View Your Repository
          </a>
        </div>
        
        <div className="border-t border-slate-700 pt-6 mt-6">
          <h3 className="text-xl font-bold mb-4">What's Next?</h3>
          <p className="text-slate-300 mb-6">
            Your repository is now ready with a realistic commit history. You can submit it directly to {getHackathonName()} or make additional customizations.
          </p>
          
          <button onClick={() => navigate('/')} className="btn bg-slate-700 hover:bg-slate-600 text-white">
            <Home className="mr-2" />
            Return Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default Completion;