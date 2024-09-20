import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
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
  const [showScanner, setShowScanner] = useState(true);
  const [qrscan, setQrscan] = useState('Scan');
  const { eventId } = useParams();


// const location = useLocation();
// const params = new URLSearchParams(location.search);
const verifyInvitation = (scannedValue) => {
  console.log(eventId);
  axios(`${baseUrl}/verify_qrcode/${scannedValue}/${eventId}`, {headers: headers})
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
      setShowScanner(false);
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <>
      <div>
        <div className="container">
          {showInvited && (
          <div className='container text-lg'>
            <h1>This user is invited to this event</h1>
          </div>
          )}
          {showUninvited && (
            <div className='container text-lg'>
              <h1>This user is not invited to this event</h1>
            </div>
          )}
          <div className="qr-header">
            <span>QR Scanner</span>
          </div>
          {showScanner &&(
            <div className="qr-reader">
             <QrScan
              onError={handleError} // Handle errors
              onScan={handleScan} // Use handleScan instead of verifyInvitation
            />
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Verify;
