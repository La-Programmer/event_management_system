import React, { useState, useEffect } from 'react';
import './RSVPList.css'
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar';



const RSVPList = () => {
  const [rsvps, setRsvps] = useState([]);

  useEffect(() => {
    fetchRSVPs();
  }, []);

  const fetchRSVPs = async () => {
    try {
      // get data from api endpoint
      const response = await fetch('https://api.example.com/rsvps');
      const data = await response.json();
      setRsvps(data);
    } catch (error) {
      console.error('Error fetching RSVPs:', error);
      // using sample data for demonstarting purpose
      setRsvps([
        { name: 'Alice Johnson', status: 'yes', contact: 'alice@example.com' },
        { name: 'Bob Smith', status: 'no', contact: 'bob@example.com' },
        { name: 'Charlie Brown', status: 'maybe', contact: 'charlie@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
        { name: 'Diana Prince', status: 'yes', contact: 'diana@example.com' },
      ]);
    }
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
