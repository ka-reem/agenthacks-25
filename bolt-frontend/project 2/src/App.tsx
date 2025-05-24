import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AppProvider } from './context/AppContext';
import Layout from './components/Layout';
import LandingPage from './pages/LandingPage';
import EmailForm from './pages/EmailForm';
import HackathonSelection from './pages/HackathonSelection';
import DateSelection from './pages/DateSelection';
import BuildLog from './pages/BuildLog';
import Completion from './pages/Completion';

function App() {
  return (
    <ThemeProvider>
      <AppProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/email" element={<EmailForm />} />
              <Route path="/select-hackathon" element={<HackathonSelection />} />
              <Route path="/select-date" element={<DateSelection />} />
              <Route path="/build" element={<BuildLog />} />
              <Route path="/complete" element={<Completion />} />
            </Routes>
          </Layout>
        </Router>
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;