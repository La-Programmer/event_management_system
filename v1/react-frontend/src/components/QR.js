import React, { useState } from 'react';
import { Link } from "react-router-dom";
import QrScan from 'react-qr-reader';
import './QR.css';

function QRCodeScan() {
    const [qrscan, setQrscan] = useState('Scan');

    const handleScan = data => {
        if (data) {
            // send a request to the api
            
            setQrscan(data);
        }
    }

    const handleError = err => {
        console.error(err);
    }

    return (
        <div className="container">
            <div className="qr-header">
                <Link to="/" className="link">Go back</Link>
                <span>QR Scanner</span>
            </div>
            <div className="qr-reader">
                <QrScan
                    onError={handleError}
                    onScan={handleScan}
                />
            </div>
            <textarea
                className="textarea"
                readOnly
                value={qrscan}
            />
        </div>
    );
}

export default QRCodeScan;
