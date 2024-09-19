import React, { useState, useEffect } from 'react';
import './RSVPList.css'
import axios from 'axios';
import AdminHeader from './AdminHeader'
import Sidebar from './Sidebar';
import { useEvent } from '../hooks/useEvent';
const baseUrl = require('../apiBaseUrl');


const token = localStorage.getItem('token');

const headers = {
  'Authorization': `Bearer ${token}`
}

const RSVPList = () => {
  const { event } = useEvent();
  const [rsvps, setRsvps] = useState([]);
  
  const data = {};

  const fetchRSVPs = () => {
    axios.get(`${baseUrl}/invitations`, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Invitations gotten successfully");
          console.log(response.data.result);
          setRsvps(response.data.result);
        } else if (response.status === 401) {
          console.log(`Failed to get invitations ${response.data.msg}`);
        }
      })
      .catch((error) => {
        console.log(`Failed to get invitations ${error}`);
      });
    };
    

  useEffect(() => {
    fetchRSVPs();
  }, []);
    
  const handleSendEmail = (email, invitationId) => {
    console.log(`Sending reminder to ${email}`);
    axios.post(`${baseUrl}/invitations/send_invitation/${invitationId}`, data, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Success sending invitation");
        } else {
          console.log("Error then", response);
        }
      })
      .catch((error) => {
        console.log("Error catch", error);
      })
  };

  const handleSendEmailToAll = () => {
    axios.post(`${baseUrl}/invitations/send_all_invitations/${event}`, data, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Success sending invitations");
        } else {
          console.log("Error then", response);
        }
      })
      .catch((error) => {
        console.log("Error catch", error);
      })
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
              <td>{rsvp.recipient_name}</td>
              <td>{rsvp.status}</td>
              <td>{rsvp.recipient_email}</td>
              <td>
                <button onClick={() => handleSendEmail(rsvp.recipient_email, rsvp.id)} className="btn btn-info">
                  Send Email
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

      <button onClick={handleSendEmailToAll} className="btn-send-all">Send Emails to All</button>
    </div>
    </>
  );
};

export default RSVPList;
