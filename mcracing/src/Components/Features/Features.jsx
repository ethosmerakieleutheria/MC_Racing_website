import React from 'react';
import FeatureCard from './FeatureCard';
import { Car, Trophy, Users } from 'lucide-react';

const Features = () => {
  const features = [
    { Icon: Car, title: 'Pro Simulators', description: 'State-of-the-art racing simulators' },
    { Icon: Trophy, title: 'Championships', description: 'Regular tournaments and leagues' },
    { Icon: Users, title: 'Training', description: 'Professional racing instruction' }
  ];

  return (
    <div className="grid md:grid-cols-3 gap-6 mb-12">
      {features.map((feature, index) => (
        <FeatureCard key={index} {...feature} />
      ))}
    </div>
  );
};

export default Features;
