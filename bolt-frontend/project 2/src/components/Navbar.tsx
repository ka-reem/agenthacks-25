import React from 'react';
import { Link } from 'react-router-dom';
import { Code } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-slate-800 border-b border-slate-700 py-4">
      <div className="container-custom flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          <Code size={24} className="text-indigo-500" />
          <span className="text-xl font-bold">Cheatathon</span>
        </Link>
        <div className="flex space-x-4">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-slate-300 hover:text-white transition-colors duration-200"
          >
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;