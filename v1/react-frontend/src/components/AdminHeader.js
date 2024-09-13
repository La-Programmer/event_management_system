import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import './Header.css'; // Import CSS for styling

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        EIMS
        {/* Replace  logo image or text */}
        <Link to="/" className="logo">
          <img src="/path/to/logo.png" alt="Logo" />
        </Link>
      </div>
      <nav className="header-nav">
        <ul>
          <li>
            <Link to="/login">Notificatins</Link>
          </li>
          <li>
            <Link to="/signup">Log out</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
