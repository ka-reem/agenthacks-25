import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal, UserCircle as LoaderCircle } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { buildLogData } from '../data/buildLogData';

const BuildLog: React.FC = () => {
  const [currentLine, setCurrentLine] = useState(-1);
  const [isComplete, setIsComplete] = useState(false);
  const { setIsProcessComplete } = useAppContext();
  const navigate = useNavigate();
  const terminalRef = useRef<HTMLDivElement>(null);

  const cloneLog = [
    "Cloning into 'DispatchAI'...",
    "remote: Enumerating objects: 2386, done.",
    "remote: Counting objects: 100% (129/129), done.",
    "remote: Compressing objects: 100% (51/51), done.",
    "remote: Total 2386 (delta 87), reused 102 (delta 76), pack-reused 2257 (from 1)",
    "Receiving objects: 100% (2386/2386), 6.00 MiB | 11.11 MiB/s, done.",
    "Resolving deltas: 100% (1365/1365), done."
  ];

  useEffect(() => {
    const showCloneLogs = async () => {
      // First show clone logs
      for (let i = 0; i < cloneLog.length; i++) {
        setCurrentLine(i);
        await new Promise(resolve => setTimeout(resolve, 200));
      }
      
      // Wait 2 seconds
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Then show build logs
      for (let i = 0; i < buildLogData.length; i++) {
        setCurrentLine(cloneLog.length + i);
        if (terminalRef.current) {
          terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
        await new Promise(resolve => setTimeout(resolve, 80));
      }
      
      setIsComplete(true);
      setIsProcessComplete(true);
      
      // Navigate to completion page after a delay
      setTimeout(() => {
        navigate('/complete');
      }, 2000);
    };

    showCloneLogs();
  }, [navigate, setIsProcessComplete]);

  const getAllLogs = () => {
    const logs = [...cloneLog];
    if (currentLine >= cloneLog.length) {
      logs.push(...buildLogData.slice(0, currentLine - cloneLog.length + 1));
    }
    return logs;
  };

  return (
    <div className="max-w-4xl mx-auto scale-in">
      <h2 className="text-2xl font-bold mb-6 flex items-center">
        <Terminal className="mr-2 text-green-400" />
        Building Your Project
      </h2>
      
      <div className="terminal" ref={terminalRef}>
        {getAllLogs().map((line, index) => (
          <div key={index} className="mb-1">
            {line}
          </div>
        ))}
        {!isComplete && (
          <div className="flex items-center text-indigo-400 mt-2">
            <LoaderCircle className="animate-spin mr-2" size={16} />
            <span>Processing...</span>
          </div>
        )}
        {isComplete && (
          <div className="text-green-500 font-bold mt-2">
            Success! You have successfully stolen someone else's hackathon project.
          </div>
        )}
      </div>
    </div>
  );
};

export default BuildLog;