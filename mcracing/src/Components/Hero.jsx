import React, { useState } from 'react';
import Button from '../UI/Button';
import RacingGame from './Game/RacingGame';
import './Hero.css';

const Hero = () => {
  const [showGame, setShowGame] = useState(false);

  return (
    <div className="relative bg-gray-900 text-white">
      {/* Video Background */}
      <video
        className="absolute inset-0 w-full h-full object-cover video-container"
        autoPlay
        loop
        muted
        playsInline
      >
        <source src="/vid.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Overlay for dark effect */}
      <div className="absolute inset-0 bg-black/70" />

      {/* Hero Content */}
      <div className="relative z-10 container mx-auto px-4 h-96 flex flex-col justify-center">
        <h1 className="text-5xl font-bold mb-4">Ultimate Racing Experience</h1>
        <p className="text-xl mb-8">
          Experience the thrill of professional racing in our cutting-edge simulators
        </p>
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

      {/* Game Section */}
      {showGame && (
        <div className="relative">
          <RacingGame />
        </div>
      )}
    </div>
  );
};

export default Hero;
