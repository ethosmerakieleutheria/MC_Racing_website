import React from 'react';
import Button from '../../src/UI/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';

function Training() {
  const programs = [
    {
      title: 'Beginner Course',
      description: 'Learn the basics of racing simulation',
      duration: '4 weeks',
      price: '$299'
    },
    {
      title: 'Advanced Techniques',
      description: 'Master advanced racing strategies',
      duration: '6 weeks',
      price: '$499'
    },
    {
      title: 'Pro Racing Program',
      description: 'Professional-level race training',
      duration: '8 weeks',
      price: '$799'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Training Programs</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {programs.map((program, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle>{program.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">{program.description}</p>
              <p className="text-gray-600 mb-2">Duration: {program.duration}</p>
              <p className="text-2xl font-bold mb-4">{program.price}</p>
              <Button className="w-full">Enroll Now</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default Training;