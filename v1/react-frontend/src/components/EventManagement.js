import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './EventManagement.css'
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar'
import { useEvent } from '../hooks/useEvent';
const baseUrl = require('../apiBaseUrl');

// fetching events from an API

const token = localStorage.getItem('token');
const headers = {
  'Authorization': `Bearer ${token}`
}


const EventManagementPage = () => {

  const { event, setEvent } = useEvent();
  const [events, setEvents] = useState([]);

  const fetchEvents = () => {
    axios.get(`${baseUrl}/events/your_events`, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Events gotten successfully");
          setEvents(response.data.result);
        } else if (response.status === 401) {
          console.log(`Error getting events ${response.data.msg}`);
        }
      })
      .catch((error) => {
        console.log(`Error getting events catch ${error}`);
      })
    };

  useEffect(() => {
    const loadEvents = () => {
      fetchEvents();
      console.log(events);
    };
    loadEvents();
  }, []);

  const handleDelete = (eventId) => {
    // send a DELETE request to API
    console.log(`Deleting event with ID: ${eventId}`);
    axios.delete(`${baseUrl}/events/${eventId}`, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Event deleted successfully");
          setEvents(events.filter(event => event.id !== eventId));
        } else {
          console.log('Error deleting event');
        }
      })
  };

  return (
    <>
    <AdminHeader />
    <div className='sidebar'>
    <Sidebar />
    </div>
    <div className="event-management-page">
      <h2>Manage Events</h2>
      <Link to="/event-create" className="btn btn-primary">Create New Event</Link>
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
              <td>{event.event_name}</td>
              <td>{event.date_time}</td>
              <td>{event.event_location}</td>
              <td>
                <button className="btn btn-info p-0" onClick={() => setEvent(event.id)}>
                  <Link to={`/invite`} className="btn">Create IVs</Link>
                </button>
                <button className='btn btn-warning p-0' onClick={() => setEvent(event.id)}>
                  <Link to={`/rsvplist`} className="btn">View IVs</Link>
                </button>
                <button className='btn btn-secondary p-0' onClick={() => setEvent(event.id)}>
                  <Link to={`/verification/${event.id}`} className='btn'>
                    Verify Invitations
                  </Link>
                </button>
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
