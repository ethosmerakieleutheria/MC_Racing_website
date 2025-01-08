import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../UI/Card';
import { Trophy, Car, GraduationCap } from 'lucide-react';
import Button from '../../UI/Button';
import { Link } from 'react-router-dom';

const BookingOption = ({ Icon, title, description, buttonText, to }) => (
  <Card className="hover:shadow-lg transition-shadow">
    <CardHeader>
      <Icon className="w-8 h-8 text-red-600 mb-2" />
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-gray-600 mb-4">{description}</p>
      <Link to={to}>
        <Button className="w-full">{buttonText}</Button>
      </Link>
    </CardContent>
  </Card>
);

const BookingOptions = () => {
  const options = [
    {
      Icon: Trophy,
      title: "Race Events",
      description: "Join competitive racing events and championships",
      buttonText: "View Races",
      to: "/races"
    },
    {
      Icon: Car,
      title: "Casual Driving",
      description: "Book a simulator for practice and casual driving",
      buttonText: "Book Time Slot",
      to: "/booking/casual"
    },
    {
      Icon: GraduationCap,
      title: "Practice Sessions",
      description: "Join structured practice sessions with instructors",
      buttonText: "View Sessions",
      to: "/booking/practice"
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Book Your Racing Experience</h1>
      <div className="grid md:grid-cols-3 gap-6">
        {options.map((option, index) => (
          <BookingOption key={index} {...option} />
        ))}
      </div>
    </div>
  );
};

export default BookingOptions;