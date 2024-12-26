// src/Components/Hero/Hero.jsx
import React, { useState } from 'react';
import Button from '../UI/Button';
import RacingGame from './Game/RacingGame';

const Hero = () => {
  const [showGame, setShowGame] = useState(false);

  return (
    <div className="relative bg-gray-900 text-white">
      {/* Hero Content */}
      <div className="relative h-96">
        <div className="absolute inset-0 bg-black/60" />
        <div className="relative z-10 container mx-auto px-4 h-full flex flex-col justify-center">
          <h1 className="text-5xl font-bold mb-4">Ultimate Racing Experience</h1>
          <p className="text-xl mb-8">Experience the thrill of professional racing in our cutting-edge simulation center</p>
          <div className="flex gap-4">
            <Button className="w-40 bg-red-600 hover:bg-red-700">Book Now</Button>
            <Button 
              className="w-40 bg-blue-600 hover:bg-blue-700"
              onClick={() => setShowGame(!showGame)}
            >
              {showGame ? 'Hide Game' : 'Try Game'}
            </Button>
          </div>
        </div>
      </div>

      {/* Game Section */}
      {showGame && (
        <div className="relative">
          <div className="absolute top-2 right-2 z-20">
            <Button 
              className="bg-red-600 hover:bg-red-700"
              onClick={() => setShowGame(false)}
            >
              Close Game
            </Button>
          </div>
          <RacingGame />
        </div>
      )}
    </div>
  );
};

export default Hero;