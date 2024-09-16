import React, { useState, useEffect } from 'react';
import './RSVPList.css'
import axios from 'axios';
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar';
import { useEvent } from '../hooks/useEvent';
const baseUrl = require('../apiBaseUrl');


const RSVPList = () => {
  const { eventId } = useEvent();
  const [rsvps, setRsvps] = useState([]);

  useEffect(() => {
    fetchRSVPs(`${baseUrl}/invitations/event/`);
  }, []);

  const fetchRSVPs = () => {
    axios.get(`${baseUrl}/invitations/event/${eventId}`)
      .then((response) => {
        if (response.status == 200) {
          console.log("Invitations gotten successfully");
          setRsvps(response.data.result);
        } else if (response.status == 401) {
          console.log(`Failed to get invitations ${response.data.msg}`);
        }
      })
      .catch((error) => {
        console.log(`Failed to get invitations ${error.data.exception}`);
      });
  };


  const handleSendReminder = (email) => {
    console.log(`Sending reminder to ${email}`);
    // Implement reminder logic here
  };

  const handleSendRemindersToAll = () => {
    rsvps.forEach(rsvp => handleSendReminder(rsvp.contact));
  };

  const counts = rsvps.reduce((acc, rsvp) => {
acc[rsvp.status] = (acc[rsvp.status] || 0) + 1;
return acc;
}, {});
  return (
    <>
    <AdminHeader className='header'> </AdminHeader>
    <div className='sidebar'>
    <Sidebar />
    </div>
    <div className="app">
      <h1>Event RSVP Tracker</h1>
    <div className="rsvp-summary">
      <h2>RSVP Summary</h2>
      <ul>
        <li>Yes: {counts.yes || 0}</li>
        <li>No: {counts.no || 0}</li>
        <li>Maybe: {counts.maybe || 0}</li>
      </ul>
    </div>

    {/* rsvp List ... */}
    <div className="rsvp-list">
      <h2>RSVP List</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Contact</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rsvps.map((rsvp, index) => (
            <tr key={index}>
              <td>{rsvp.name}</td>
              <td>{rsvp.status}</td>
              <td>{rsvp.contact}</td>
              <td>
                <button onClick={() => handleSendReminder(rsvp.contact)} className="btn-send-reminder">
                  Send Reminder
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

      <button onClick={handleSendRemindersToAll} className="btn-send-all">Send Reminders to All</button>
    </div>
    </>
  );
};

export default RSVPList;
