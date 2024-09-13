import React, { useState } from "react";
import PropTypes from "prop-types";
import "./InvitationForm.css";
import Sidebar from "./Sidebar";
import AdminHeader from "./AdminHeader";

const InvitationForm = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  // send the data to the backend to send a message
  const handleSubmit = () => {};

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
          <button type="submit">Send</button>
        </form>
      </div>
    </>
  );
};

InvitationForm.propTypes = {
  onSendInvitation: PropTypes.func.isRequired,
};

export default InvitationForm;
