import React from 'react';
import Button from '../../UI/Button';
import { Calendar } from 'lucide-react';

const RaceCard = ({ name, date, slots }) => (
  <div className="py-4 flex items-center justify-between">
    <div>
      <h3 className="font-semibold">{name}</h3>
      <p className="text-sm text-gray-600 flex items-center gap-2">
        <Calendar className="w-4 h-4" />
        {date}
      </p>
    </div>
    <div className="text-right">
      <p className="text-sm text-gray-600">{slots} slots available</p>
      <Button variant="outline" size="sm">Register</Button>
    </div>
  </div>
);

export default RaceCard;
