import React, { useEffect, useRef, useState } from "react";
import QrScanner from "qr-scanner";
import "./Verify2.css";

const EventCheckIn = () => {
  const videoElementRef = useRef(null);
  const [scanned, setScannedText] = useState("");
  const [isScanning, setIsScanning] = useState(false);

  const HandleScannedResult = () => {
    // send data to the api
  };

  useEffect(() => {
    const video = videoElementRef.current;
    const qrScanner = new QrScanner(
      video,
      (result) => {
        console.log("decoded qr code:", result);
        setScannedText(result.data);
        // logic to handle scanned data
        HandleScannedResult(result.data);
      },
      {
        returnDetailedScanResult: true,
        highlightScanRegion: true,
        highlightCodeOutline: true,
      }
    );

    if (isScanning) {
      qrScanner.start();
    } else {
      qrScanner.stop();
    }

    return () => {
      qrScanner.stop();
      qrScanner.destroy();
    };
  }, [isScanning]);

  const toggleScanning = () => {
    setIsScanning((prev) => !prev);
  };

  return (
    <div className="appContainer">
      <div className="main">
        <button className="my-btn" onClick={toggleScanning}>
          {isScanning ? "Stop Scanning" : "Start Scanning"}
        </button>
      </div>
      <div className="videoWrapper">
        <video className="qrVideo" ref={videoElementRef} />
      </div>
      <p className="scannedText">SCANNED: {scanned}</p>
    </div>
  );
};

export default EventCheckIn;
