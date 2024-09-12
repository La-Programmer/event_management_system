import React, { useState } from 'react';
import "./InviteeRSVPPage.css"
import qr from "./assets/gr_code.png"

const InviteeRSVPPage = () => {
  const [rsvpStatus, setRsvpStatus] = useState('');
  const [showQRCode, setShowQRCode] = useState(false);

  const handleRSVPChange = (e) => {
    setRsvpStatus(e.target.value);
  };

  const handleRSVPSubmit = (e) => {
    e.preventDefault();

    if (rsvpStatus === 'yes')
      setShowQRCode(true);
  };

  const handleDownloadQrCode = () => {
    // handle QR code download
    console.log('Download QR Code');
  };

  return (
    <div className="body">
      <h1>RSVP for the Eventqqq</h1>
      <form onSubmit={handleRSVPSubmit}>
        <div className="form-group">
          <label htmlFor="rsvp">Will you attend the event?</label>
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
          <img src={qr} alt="QR Code" className="qrcode" />
          <div> <button onClick={handleDownloadQrCode} className="btn-download">Download</button>
          </div>
          </div>

      )}
    </div>
  );
};

export default InviteeRSVPPage;
