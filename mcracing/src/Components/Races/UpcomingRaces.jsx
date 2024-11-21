import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../UI/Card';
import RaceCard from './RaceCard';
import { Calendar } from 'lucide-react';

const UpcomingRaces = () => {
  const races = [
    { id: 1, name: 'Sprint Championship', date: '2024-12-01', slots: 12 },
    { id: 2, name: 'Endurance Cup', date: '2024-12-15', slots: 8 },
    { id: 3, name: 'Rookie Race Day', date: '2024-12-22', slots: 15 }
  ];

  return (
    <Card className="mb-12">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calendar className="w-6 h-6" />
          Upcoming Races
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="divide-y">
          {races.map((race) => (
            <RaceCard key={race.id} {...race} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default UpcomingRaces;
