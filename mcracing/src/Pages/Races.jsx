import React from 'react';
import { Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { Calendar, Clock, Users, ArrowLeft, DollarSign } from 'lucide-react';
import Button from '../UI/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';

// RacesList Component
function RacesList() {
  const races = [
    { 
      id: 1, 
      name: 'Sprint Championship', 
      date: '2024-12-01', 
      price: '$99', 
      level: 'Advanced',
      description: 'High-intensity sprint racing for experienced drivers.',
      duration: '2 hours',
      maxParticipants: 12
    },
    { 
      id: 2, 
      name: 'Endurance Cup', 
      date: '2024-12-15', 
      price: '$149', 
      level: 'Professional',
      description: 'Test your endurance in this long-format racing event.',
      duration: '4 hours',
      maxParticipants: 8
    },
    { 
      id: 3, 
      name: 'Rookie Race Day', 
      date: '2024-12-22', 
      price: '$49', 
      level: 'Beginner',
      description: 'Perfect for newcomers to racing simulation.',
      duration: '1.5 hours',
      maxParticipants: 15
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Upcoming Races</h1>
      <div className="grid gap-6">
        {races.map(race => (
          <Card key={race.id}>
            <CardHeader>
              <CardTitle>{race.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className="flex items-center text-gray-600 mb-2">
                    <Calendar className="w-4 h-4 mr-2" />
                    {race.date}
                  </p>
                  <p className="text-gray-600">Level: {race.level}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold mb-2">{race.price}</p>
                  <Link to={`/races/${race.id}`}>
                    <Button variant="outline">View Details</Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

// RaceDetails Component
function RaceDetails() {
  const { raceId } = useParams();
  const navigate = useNavigate();

  // Mock race data - in a real app, this would come from an API
  const raceData = {
    id: raceId,
    name: 'Sprint Championship',
    date: '2024-12-01',
    price: '$99',
    level: 'Advanced',
    description: 'High-intensity sprint racing for experienced drivers. Test your skills against the best in our state-of-the-art simulators.',
    duration: '2 hours',
    maxParticipants: 12,
    requirements: [
      'Previous racing experience required',
      'Valid membership',
      'Age 18+'
    ],
    schedule: [
      'Practice session: 30 minutes',
      'Qualifying: 30 minutes',
      'Race: 1 hour'
    ]
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Button 
        variant="ghost" 
        className="mb-6"
        onClick={() => navigate('/races')}
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Races
      </Button>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{raceData.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="font-semibold mb-4">Event Details</h3>
              <div className="space-y-4">
                <p className="flex items-center text-gray-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  {raceData.date}
                </p>
                <p className="flex items-center text-gray-600">
                  <Clock className="w-4 h-4 mr-2" />
                  Duration: {raceData.duration}
                </p>
                <p className="flex items-center text-gray-600">
                  <Users className="w-4 h-4 mr-2" />
                  Max Participants: {raceData.maxParticipants}
                </p>
                <p className="flex items-center text-gray-600">
                  <DollarSign className="w-4 h-4 mr-2" />
                  Price: {raceData.price}
                </p>
              </div>

              <div className="mt-6">
                <h3 className="font-semibold mb-2">Description</h3>
                <p className="text-gray-600">{raceData.description}</p>
              </div>
            </div>

            <div>
              <div className="mb-6">
                <h3 className="font-semibold mb-2">Requirements</h3>
                <ul className="list-disc pl-5 space-y-1 text-gray-600">
                  {raceData.requirements.map((req, index) => (
                    <li key={index}>{req}</li>
                  ))}
                </ul>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">Schedule</h3>
                <ul className="list-disc pl-5 space-y-1 text-gray-600">
                  {raceData.schedule.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <Button className="w-full mt-4">Register Now</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Main Races Component
function Races() {
  return (
    <Routes>
      <Route path="/" element={<RacesList />} />
      <Route path="/:raceId" element={<RaceDetails />} />
    </Routes>
  );
}

export default Races;