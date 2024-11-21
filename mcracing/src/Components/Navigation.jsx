import React from 'react';
import Button from '../UI/Button';

const Navigation = ({ activeTab, setActiveTab }) => {
  const tabs = ['home', 'races', 'training', 'leaderboard', 'contact'];

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex space-x-4 py-4">
          {tabs.map((tab) => (
            <Button
              key={tab}
              variant={activeTab === tab ? 'default' : 'ghost'}
              onClick={() => setActiveTab(tab)}
              className="capitalize"
            >
              {tab}
            </Button>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
