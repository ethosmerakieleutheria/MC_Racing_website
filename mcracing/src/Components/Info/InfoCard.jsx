import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../UI/Card';


const InfoCard = ({ Icon, title, children }) => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center gap-2">
        <Icon className="w-6 h-6" />
        {title}
      </CardTitle>
    </CardHeader>
    <CardContent>{children}</CardContent>
  </Card>
);

export default InfoCard;
