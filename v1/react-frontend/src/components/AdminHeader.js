import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import './Header.css'; // Import CSS for styling

const deleteJWT = () => {
  localStorage.removeItem('token');
  console.log(localStorage.getItem('token'));
};

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
            <Link>Notifications</Link>
          </li>
          <li>
            <button onClick={deleteJWT}>
              <Link to="/login">Log out</Link>
            </button>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
