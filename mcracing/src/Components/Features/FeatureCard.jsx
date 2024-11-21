import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../UI/Card';

const FeatureCard = ({ Icon, title, description }) => (
  <Card className="hover:shadow-lg transition-shadow">
    <CardHeader>
      <Icon className="w-8 h-8 text-red-600 mb-2" />
      <CardTitle>{title}</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-gray-600">{description}</p>
    </CardContent>
  </Card>
);

export default FeatureCard;
