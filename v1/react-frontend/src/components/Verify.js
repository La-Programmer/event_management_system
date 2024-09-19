import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from "axios";
const baseUrl = require("../apiBaseUrl");

const token = localStorage.getItem('token');


const headers = {
  'Authorization': `Bearer ${token}`
}

const Verify = () => {
  const [showInvited, setShowInvited] = useState(false);
  const [showUninvited, setShowUninvited] = useState(false);
  const { invitationId, eventId } = useParams();
  
  const verifyInvitation = () => {
  axios(`${baseUrl}/verify_qrcode/${invitationId}/${eventId}`, {headers: headers})
    .then((response) => {
      if (response.status === 200) {
        console.log('User is invited')
        setShowInvited(true);
      } else {
        console.log('User is uninvited')
        setShowUninvited(true);
      }
    })
    .catch((error) => {
      console.log(`Error occurred in verification: ${error}`);
    });
  };

  useEffect(() => {
    verifyInvitation();
  }, [])

  return (
    <>
      <div>
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
  )
}

export default Verify
