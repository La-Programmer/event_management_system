import React from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router for navigation
import './Header.css'; // Import CSS for styling

const Header = () => {
  return (
    <header className="header">
      <div>
        <Link to="/" className="logo">
          <span><span className='e'>E</span>IMS</span>
        </Link>
      </div>
      <nav className="header-nav">
        <ul>
          <li> 
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/features">Features</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/register">Sign Up</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
