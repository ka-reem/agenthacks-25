import React, { createContext, useContext, useState } from 'react';

interface AppContextType {
  email: string;
  setEmail: (email: string) => void;
  selectedHackathon: string;
  setSelectedHackathon: (hackathon: string) => void;
  commitDate: string;
  setCommitDate: (date: string) => void;
  isProcessComplete: boolean;
  setIsProcessComplete: (complete: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [email, setEmail] = useState('');
  const [selectedHackathon, setSelectedHackathon] = useState('');
  const [commitDate, setCommitDate] = useState('');
  const [isProcessComplete, setIsProcessComplete] = useState(false);

  return (
    <AppContext.Provider
      value={{
        email,
        setEmail,
        selectedHackathon,
        setSelectedHackathon,
        commitDate,
        setCommitDate,
        isProcessComplete,
        setIsProcessComplete,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = (): AppContextType => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};