import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useParams, useNavigate } from 'react-router-dom';
import { Calendar as IconCalendar, Clock, Users, ArrowLeft, DollarSign } from 'lucide-react';
import Button from '../UI/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';
import { raceAPI } from '../services/api';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment-timezone';

// Set the default timezone
moment.tz.setDefault('UTC');
const localizer = momentLocalizer(moment);

function RacesList() {
  const [races, setRaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRaces = async () => {
      try {
        const response = await raceAPI.get_all_races();
        if (response.data && Array.isArray(response.data.races)) {
          setRaces(response.data.races);

          // Format races data for the calendar
          const formattedEvents = response.data.races.map((race) => ({
            title: race.name,
            start: new Date(race.date),
            end: new Date(race.date),
            id: race._id, // Ensure this matches the MongoDB _id
          }));

          setEvents(formattedEvents);
        } else {
          throw new Error("Invalid data format received from API");
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRaces();
  }, []);

  const handleSelectEvent = (event) => {
    if (event.id) {
      console.log("Navigating to event:", event.id); // Debugging log
      navigate(`/races/${event.id}`);
    } else {
      console.error("Event ID is missing:", event);
    }
  };

  if (loading) return <p>Loading races...</p>;
  if (error) return <p className="text-red-500">Error loading races: {error}</p>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Upcoming Races</h1>

      {/* Calendar Component */}
      <div className="mb-8">
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
          onSelectEvent={handleSelectEvent}
        />
      </div>

      {/* Existing List of Races */}
      <div className="grid gap-6">
        {races.map((race) => (
          <Card key={race._id}>
            <CardHeader>
              <CardTitle>{race.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div>
                  <p className="flex items-center text-gray-600 mb-2">
                    <IconCalendar className="w-4 h-4 mr-2" />
                    {race.date}
                  </p>
                  <p className="text-gray-600">Level: {race.level}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold mb-2">${race.price}</p>
                  <Link to={`/races/${race._id}`}>
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

function RaceDetails() {
  const { raceId } = useParams();
  const navigate = useNavigate();
  const [raceData, setRaceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRaceDetails = async () => {
      try {
        const response = await raceAPI.getRaceById(raceId);
        if (response.data) {
          setRaceData(response.data);
        } else {
          throw new Error("Race details not found");
        }
      } catch (err) {
        setError(err.message || "Failed to fetch race details");
      } finally {
        setLoading(false);
      }
    };

    fetchRaceDetails();
  }, [raceId]);

  if (loading) return <p className="text-gray-600">Loading race details...</p>;
  if (error) return <p className="text-red-600">Error: {error}</p>;
  if (!raceData) return <p className="text-gray-600">Race not found.</p>;

  return (
    <div className="container mx-auto px-4 py-8">
      <Button variant="ghost" className="mb-6" onClick={() => navigate('/races')}>
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
                  <IconCalendar className="w-4 h-4 mr-2" />
                  {raceData.date}
                </p>
                <p className="flex items-center text-gray-600">
                  <Clock className="w-4 h-4 mr-2" />
                  Duration: {raceData.duration || "N/A"}
                </p>
                <p className="flex items-center text-gray-600">
                  <Users className="w-4 h-4 mr-2" />
                  Max Participants: {raceData.max_participants || "N/A"}
                </p>
                <p className="flex items-center text-gray-600">
                  <DollarSign className="w-4 h-4 mr-2" />
                  Price: ${raceData.price}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Races() {
  return (
    <Routes>
      <Route path="/" element={<RacesList />} />
      <Route path="/:raceId" element={<RaceDetails />} />
    </Routes>
  );
}

export default Races;
