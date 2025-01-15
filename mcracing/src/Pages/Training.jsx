import React, { useState, useEffect } from 'react';
import { Calendar, Users, Clock } from 'lucide-react';
import Button from '../UI/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';
import { trainingAPI } from '../services/api';

function TrainingList() {
  const [trainingSlots, setTrainingSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrainingSlots = async () => {
      try {
        const response = await trainingAPI.getPrograms();
        if (response.data && Array.isArray(response.data.training_slots)) {
          setTrainingSlots(response.data.training_slots);
        } else {
          throw new Error("Invalid data format received from API");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTrainingSlots();
  }, []);

  if (loading) return <p>Loading training slots...</p>;
  if (error) return <p className="text-red-500">Error loading training slots: {error}</p>;
  if (trainingSlots.length === 0) return <p>No available training slots.</p>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Available Training Slots</h1>
      <div className="grid gap-6">
        {trainingSlots.map((slot) => (
          <Card key={slot.id}>
            <CardHeader>
              <CardTitle>{slot.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className="flex items-center text-gray-600 mb-2">
                    <Calendar className="w-4 h-4 mr-2" />
                    {slot.date}
                  </p>
                  <p className="flex items-center text-gray-600 mb-2">
                    <Users className="w-4 h-4 mr-2" />
                    Trainees: {slot.current_trainees}/{slot.max_trainees}
                  </p>
                  <p className="flex items-center text-gray-600 mb-2">
                    <Clock className="w-4 h-4 mr-2" />
                    Duration: {slot.duration || "N/A"}
                  </p>
                  <p className="text-gray-600">Level: {slot.level}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold mb-2">${slot.price}</p>
                  <Button variant="outline">Register</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default TrainingList;
