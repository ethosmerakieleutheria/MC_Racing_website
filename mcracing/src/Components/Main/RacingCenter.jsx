import Hero from '../Hero';
import Navigation from '../Navigation';
import Features from '../Features/Features';
import UpcomingRaces from '../Races/UpcomingRaces';
import InfoCard from '../Info/InfoCard';
import { useState } from 'react';
import { MapPin, Clock } from 'lucide-react';
import Button from '../../UI/Button';

const RacingCenter = () => {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="min-h-screen bg-gray-100">
      <Hero />
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="container mx-auto px-4 py-8">
        <Features />
        <UpcomingRaces />
        <div className="grid md:grid-cols-2 gap-6">
          <InfoCard Icon={MapPin} title="Location">
            <p className="text-gray-600 mb-2">123 Racing Street</p>
            <p className="text-gray-600">Racing City, RC 12345</p>
            <Button variant="link" className="mt-4 p-0">Get Directions</Button>
          </InfoCard>
          <InfoCard Icon={Clock} title="Hours">
            <p className="text-gray-600 mb-2">Monday - Friday: 10:00 AM - 10:00 PM</p>
            <p className="text-gray-600">Saturday - Sunday: 9:00 AM - 11:00 PM</p>
          </InfoCard>
        </div>
      </main>
    </div>
  );
};

export default RacingCenter;
