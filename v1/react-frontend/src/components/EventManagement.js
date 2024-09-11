import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import './EventManagement.css'
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar'

// fetching events from an API
const fetchEvents = async () => {
  // Replace with API call
  return [
    { id: 1, name: 'Event 1', date: '2024-09-10', location: 'Location 1' },
    { id: 2, name: 'Event 2', date: '2024-09-12', location: 'Location 2' },
  ];
};

const EventManagementPage = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const loadEvents = async () => {
      const eventData = await fetchEvents();
      setEvents(eventData);
    };

    loadEvents();
  }, []);

  const handleDelete = (eventId) => {
    // send a DELETE request to API
    console.log(`Deleting event with ID: ${eventId}`);
    setEvents(events.filter(event => event.id !== eventId));
  };

  return (
    <>
    <AdminHeader />
    <div className='sidebar'>
    <Sidebar />
    </div>
    <div className="event-management-page">
      <h2>Manage Events</h2>
      <Link to="/create-event" className="btn btn-primary">Create New Event</Link>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Location</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {events.map(event => (
            <tr key={event.id}>
              <td>{event.name}</td>
              <td>{event.date}</td>
              <td>{event.location}</td>
              <td>
                <Link to={`/events/${event.id}`} className="btn btn-info">View</Link>
                <Link to={`/edit-event/${event.id}`} className="btn btn-warning">Edit</Link>
                <button onClick={() => handleDelete(event.id)} className="btn btn-danger">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </>
  );
};

export default EventManagementPage;
