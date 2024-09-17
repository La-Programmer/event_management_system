import React, { useState } from "react";
import PropTypes from "prop-types";
import "./InvitationForm.css";
import Sidebar from "./Sidebar";
import axios from "axios";
import { useEvent } from '../hooks/useEvent';
import AdminHeader from "./AdminHeader";
const baseUrl = require("../apiBaseUrl")

const InvitationForm = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const { event } = useEvent();

  console.log(event);

  const token = localStorage.getItem('token');

  const headers = {
    'Authorization': `Bearer ${token}`
  }

  const data = {
    event_id: event,
    recipient_name: name,
    recipient_number: phone,
    recipient_email: email,
    message: message
  }

  // send the data to the backend to send a message
  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${baseUrl}/invitations`, data, {headers: headers})
      .then((response) => {
        if (response.status === 200) {
          console.log("Successfully created invitation");
        } else {
          console.log(`Error: ${response}`);
        }
      })
      .catch((error) => {
        console.log(`Error catch: ${error}`);
      });
  };

  return (
    <>
      <div>
         <AdminHeader />
      </div>
      <div>
        <Sidebar></Sidebar>
      </div>
      <div className="invitation-form">
        <h2>Send Invitation</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="message">Phone: </label>
            <input
              type="number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            ></input>
          </div>
          <div className="form-group">
            <label htmlFor="message">Message: </label>
            <input
              type="text"
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            ></input>
          </div>
          <button type="submit">Create</button>
        </form>
      </div>
    </>
  );
};

InvitationForm.propTypes = {
  onSendInvitation: PropTypes.func.isRequired,
};

export default InvitationForm;
