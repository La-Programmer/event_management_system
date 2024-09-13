import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
      <div>
        <Link to="/" className="logo">
          <span><span className='e'>E</span>IMS</span>
        </Link>
      </div>
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
