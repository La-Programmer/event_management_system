import React, { useState, useEffect } from 'react';
import "./InviteeRSVPPage.css";
import QRCode from "react-qr-code";
import axios from "axios";
import { useParams } from 'react-router-dom';
const baseUrl = require("../apiBaseUrl");

const InviteeRSVPPage = () => {
  const [invitation, setInvitation] = useState({});
  const [rsvpStatus, setRsvpStatus] = useState('');
  const [showQRCode, setShowQRCode] = useState(false);

  const { invitationId, eventId } = useParams();
  console.log(invitationId);

  const handleRSVPChange = (e) => {
    setRsvpStatus(e.target.value);
  };

  const handleRSVPSubmit = (e) => {
    e.preventDefault();
    let data = {};
    if (rsvpStatus === "yes") {
      data.status = "true";
    } else {
      data.status = "false";
    }
    axios.post(`${baseUrl}/rsvp/${invitationId}`, data)
      .then((response) => {
        if (response.status == 200) {
          console.log("Response to invitation successful");
          if (rsvpStatus === "yes") {
            setShowQRCode(true);
          }
        } else {
          console.log("Unexpected error occurred");
        }
      })
      .catch((error) => {
        console.log(`Error occurred ${error}`);
      });
  };

  const getInvitationDetails = () => {
    axios.get(`${baseUrl}/rsvp/${invitationId}`)
      .then((response) => {
        if (response.status === 200) {
          console.log("Invitation data gotten successfully");
          setInvitation(response.data.result);
        } else {
          console.log(`Unexpected error: ${response}`);
        }
      })
      .catch((error) => {
        console.log(`Error occurred: ${error}`);
      })
  };

  const handleDownloadQrCode = () => {
    // handle QR code download
    console.log('Download QR Code');
  };

  useEffect(() => {
    getInvitationDetails();
  }, [])
  

  return (
    <div className="body">
      <h1>RSVP for the Event</h1>
      <form onSubmit={handleRSVPSubmit}>
        <div className="form-group">
          <p>{invitation.message}</p>
          <label htmlFor="rsvp">Will you attend the event: {invitation.event_name}?</label>
          <select id="rsvp" value={rsvpStatus} onChange={handleRSVPChange} required>
            <option value="">Select</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
            <option value="maybe">Maybe</option>
          </select>
        </div>
        <button type="submit" className="btn-submit">Submit RSVP</button>
      </form>
      
      {showQRCode && (
        <div className="qrcode-container">
          <QRCode
            size={256}
            style={{ height: "auto", maxWidth: "30%", width: "30%" }}
            value={`http://localhost:3000/verification/${invitationId}/${eventId}`}
            viewBox={`0 0 256 256`}
          />
        </div>

      )}
    </div>
  );
};

export default InviteeRSVPPage;
