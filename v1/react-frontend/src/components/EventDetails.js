import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './EventDetails.css'
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar';


const sampleEventData = {
    title: 'Sample Event',
    date: '2024-09-30T18:00:00Z',
    location: 'Sample Location, City, Country',
    description: 'This is a sample event description. Please check back later for real details.',
    organizer: 'Sample Organizer'
  };

const EventDetails = ({ eventId }) => {
  const [eventData, setEventData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchEventData = async () => {
      try {
        const response = await axios.get(`/api/events/${eventId}`); // api end point
        setEventData(response.data);
      } catch (err) {
        setEventData(sampleEventData)
        // setError('Failed to fetch event details. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchEventData();
  }, [eventId]);

  if (isLoading) return <div>Loading...</div>;

  if (!eventData) return <div>No event details available.</div>;

  return (
    <>
    <AdminHeader />
    <div>
      <Sidebar />
    </div>
    <div className="event-details">
      <h1>{eventData.title}</h1>
      <p><strong>Date:</strong> {new Date(eventData.date).toLocaleDateString()}</p>
      <p><strong>Location:</strong> {eventData.location}</p>
      <p><strong>Description:</strong> {eventData.description}</p>
      <p><strong>Organizer:</strong> {eventData.organizer}</p>
    </div>
  </>
  );
};

EventDetails.propTypes = {
  eventId: PropTypes.string.isRequired,
};

export default EventDetails;
