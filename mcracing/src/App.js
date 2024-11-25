import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './Components/Navigation';
import Races from './Pages/Races';
import Training from './Pages/Training';
import Leaderboard from './Pages/Leaderboard';
import Contact from './Pages/Contact';
import RacingCenter from './Components/Main/RacingCenter';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<RacingCenter />} />
        <Route path="/races/*" element={<Races />} />
        <Route path="/training" element={<Training />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;