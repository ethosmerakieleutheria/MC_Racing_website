import React from 'react';
import Button from '../UI/Button';

const Hero = () => (
  <div className="relative h-96 bg-gray-900 text-white">
    <div className="absolute inset-0 bg-black/60" />
    <div className="relative z-10 container mx-auto px-4 h-full flex flex-col justify-center">
      <h1 className="text-5xl font-bold mb-4">Ultimate Racing Experience</h1>
      <p className="text-xl mb-8">Experience the thrill of professional racing in our cutting-edge simulation center</p>
      <Button className="w-40 bg-red-600 hover:bg-red-700">Book Now</Button>
    </div>
  </div>
);

export default Hero;
