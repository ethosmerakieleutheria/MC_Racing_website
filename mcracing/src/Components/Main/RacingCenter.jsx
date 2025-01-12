import Hero from '../Hero';
import Features from '../Features/Features';
import UpcomingRaces from '../Races/UpcomingRaces';
import InfoCard from '../Info/InfoCard';
import { MapPin, Clock } from 'lucide-react';
import React from 'react';

const RacingCenter = () => {
  const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
  const location = {
    address: "701 S Clinton St Suite 709",
    city: "Fort Wayne, IN 46802",
    directionsLink:
      "https://www.google.com/maps/place/MC+Racing/@41.0802971,-85.1406338,17z/data=!3m2!4b1!5s0x8815e48d7df5393f:0xbb8126f7c6dd34b2!4m6!3m5!1s0x8815e59ff433cddd:0xd31403685da5f34a!8m2!3d41.0802971!4d-85.1380589!16s%2Fg%2F11y245lj75?entry=ttu&g_ep=EgoyMDI1MDEwOC4wIKXMDSoASAFQAw%3D%3D",
    staticMap:
      `https://maps.googleapis.com/maps/api/staticmap?center=701+S+Clinton+St+Suite+709,Fort+Wayne,IN+46802&zoom=15&size=400x200&markers=color:red%7C701+S+Clinton+St+Suite+709,Fort+Wayne,IN+46802&key=${apiKey}`
  };

  const hours = [
    { day: "Monday", time: "Closed" },
    { day: "Tuesday - Thursday", time: "3:00 PM - 12:00 AM" },
    { day: "Friday - Saturday", time: "2:00 PM - 2:00 AM" },
    { day: "Sunday", time: "2:00 PM - 12:00 AM" }
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Hero />
      <main className="container mx-auto px-4 py-8">
        <Features />
        <UpcomingRaces />

        <div className="grid sm:grid-cols-1 md:grid-cols-2 gap-6">
          {/* Location Card */}
          <InfoCard Icon={MapPin} title="Location">
            <div className="mb-4">
              {/* Make the map clickable */}
              <a href={location.directionsLink} target="_blank" rel="noopener noreferrer">
                <img
                  src={location.staticMap}
                  alt="Map of Location"
                  className="w-full h-40 object-cover rounded-md hover:brightness-75 transition-all"
                />
              </a>
            </div>
            <p className="text-gray-700 mb-1 text-lg">
              <strong>{location.address}</strong>
            </p>
            <p className="text-gray-700 text-lg">
              {location.city}
            </p>
            <button
              className="mt-4 px-4 py-2 bg-blue-500 text-white font-bold rounded-md transition-transform transform hover:scale-105 hover:shadow-lg hover:bg-blue-700 active:scale-95 active:bg-blue-900"
              onClick={() => window.open(location.directionsLink, "_blank")}
            >
              View on Google Maps
            </button>
          </InfoCard>

          {/* Hours Card */}
          <InfoCard Icon={Clock} title="Hours">
            <div className="grid grid-cols-2 gap-4">
              {hours.map((hour, index) => (
                <React.Fragment key={index}>
                  <p className="text-gray-800 font-semibold text-xl">{hour.day}</p>
                  <p className="text-gray-600 text-lg">{hour.time}</p>
                </React.Fragment>
              ))}
            </div>
          </InfoCard>
        </div>
      </main>
    </div>
  );
};

export default RacingCenter;
