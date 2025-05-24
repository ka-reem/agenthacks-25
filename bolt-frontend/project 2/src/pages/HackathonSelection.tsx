import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trophy, ArrowRight, ArrowLeft } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { berkeleyProjects } from '../data/hackathonProjects';

const hackathons = [
  { id: 'treehacks', name: 'Tree Hacks' },
  { id: 'calhacks', name: 'Cal Hacks' },
  { id: 'berkeley-ai', name: 'UC Berkeley AI Hackathon 2024' },
  { id: 'stanford-ai', name: 'Stanford AI Hackathon' },
  { id: 'mit-hack', name: 'MIT Hack' },
  { id: 'hackmit', name: 'HackMIT' },
];

const HackathonSelection: React.FC = () => {
  const { selectedHackathon, setSelectedHackathon } = useAppContext();
  const [showProjects, setShowProjects] = useState(false);
  const [selectedProject, setSelectedProject] = useState('');
  const navigate = useNavigate();

  const handleSelect = (hackathon: string) => {
    setSelectedHackathon(hackathon);
    setShowProjects(hackathon === 'berkeley-ai');
    setSelectedProject('');
  };

  const handleProjectSelect = (projectId: string) => {
    setSelectedProject(projectId);
  };

  const handleContinue = () => {
    if (selectedHackathon && (!showProjects || selectedProject)) {
      navigate('/select-date');
    }
  };

  return (
    <div className="max-w-2xl mx-auto card scale-in">
      <h2 className="text-2xl font-bold mb-6 flex items-center">
        <Trophy className="mr-2 text-yellow-500" />
        Select a Hackathon
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {hackathons.map((hackathon) => (
          <button
            key={hackathon.id}
            className={`p-4 rounded-lg border text-left transition-all ${
              selectedHackathon === hackathon.id
                ? 'border-indigo-500 bg-indigo-500/20'
                : 'border-slate-600 hover:border-slate-500 bg-slate-700/50'
            }`}
            onClick={() => handleSelect(hackathon.id)}
          >
            <span className="block text-lg font-medium">{hackathon.name}</span>
          </button>
        ))}
      </div>

      {showProjects && (
        <div className="mt-8 mb-8">
          <h3 className="text-xl font-bold mb-4">Select a Project</h3>
          <div className="space-y-4 max-h-96 overflow-y-auto pr-4">
            {berkeleyProjects.map((project) => (
              <button
                key={project.id}
                className={`w-full p-4 rounded-lg border text-left transition-all ${
                  selectedProject === project.id
                    ? 'border-indigo-500 bg-indigo-500/20'
                    : 'border-slate-600 hover:border-slate-500 bg-slate-700/50'
                }`}
                onClick={() => handleProjectSelect(project.id)}
              >
                <h4 className="text-lg font-medium mb-2">{project.name}</h4>
                <p className="text-sm text-slate-300">{project.description}</p>
              </button>
            ))}
          </div>
        </div>
      )}
      
      <div className="flex justify-between">
        <button
          onClick={() => navigate('/email')}
          className="btn bg-slate-700 hover:bg-slate-600 text-white"
        >
          <ArrowLeft className="mr-2" />
          Back
        </button>
        
        <button
          onClick={handleContinue}
          disabled={!selectedHackathon || (showProjects && !selectedProject)}
          className={`btn btn-primary ${
            (!selectedHackathon || (showProjects && !selectedProject)) ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          Continue
          <ArrowRight className="ml-2" />
        </button>
      </div>
    </div>
  );
};

export default HackathonSelection;