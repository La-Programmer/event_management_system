import React, { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import axios from "axios";
import QrScan from 'react-qr-reader';
import "./Verify.css"






const baseUrl = require("../apiBaseUrl");

const Verify = () => {
  
  const token = localStorage.getItem('token');
  
  const headers = {
    'Authorization': `Bearer ${token}`
  };
  const [showInvited, setShowInvited] = useState(false);
  const [showUninvited, setShowUninvited] = useState(false);
  // const { invitationId, eventId } = useParams();
  const [qrscan, setQrscan] = useState('Scan');


const location = useLocation();
const params = new URLSearchParams(location.search);
const verifyInvitation = (scannedValue) => {
  const invitationId = params.get('invitationId');
  const eventId = params.get('eventId');
  console.log(invitationId);
  console.log(eventId);
  axios(`${baseUrl}/verify_qrcode/${invitationId}/${eventId}`, {
      headers: headers,
      data: { qr_code: scannedValue }  // Send the scanned value in the request body
    })
      .then((response) => {
        if (response.status === 200) {
        console.log('User is invited')
          setShowInvited(true);
          setShowUninvited(false);
        } else {
        console.log('User is uninvited')
          setShowUninvited(true);
          setShowInvited(false);
        }
      })
      .catch((error) => {
        console.log(`Error occurred in verification: ${error}`);
      });
  };

  const handleScan = (data) => {
    if (data) {
      setQrscan(data); // Set the scanned QR code value
      verifyInvitation(data); // Verify the scanned QR code
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <>
      <div>
        <div className="container">
          <div className="qr-header">
            <span>QR Scanner</span>
          </div>
          <div className="qr-reader">
            <QrScan
              onError={handleError} // Handle errors
              onScan={handleScan} // Use handleScan instead of verifyInvitation
            />
          </div>
          <textarea
            className="textarea"
            readOnly
            value={qrscan}
          />
        </div>
        {showInvited && (
          <div>
            This user is invited to this event
          </div>
        )}
        {showUninvited && (
          <div>
            This user is not invited to this event
          </div>
        )}
      </div>
    </>
  );
};

export default Verify;
