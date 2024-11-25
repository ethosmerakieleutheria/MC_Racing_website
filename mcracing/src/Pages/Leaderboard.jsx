import React from 'react';
import { Trophy } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';

function Leaderboard() {
  const rankings = [
    { rank: 1, name: 'John Doe', points: 2500, races: 15 },
    { rank: 2, name: 'Jane Smith', points: 2350, races: 14 },
    { rank: 3, name: 'Mike Johnson', points: 2200, races: 13 }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Leaderboard</h1>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Trophy className="w-6 h-6 mr-2 text-yellow-500" />
            Top Racers
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-4">Rank</th>
                  <th className="text-left py-4">Name</th>
                  <th className="text-left py-4">Points</th>
                  <th className="text-left py-4">Races</th>
                </tr>
              </thead>
              <tbody>
                {rankings.map(({ rank, name, points, races }) => (
                  <tr key={rank} className="border-b">
                    <td className="py-4">{rank}</td>
                    <td className="py-4">{name}</td>
                    <td className="py-4">{points}</td>
                    <td className="py-4">{races}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default Leaderboard;