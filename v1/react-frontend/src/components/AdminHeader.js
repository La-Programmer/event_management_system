import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const deleteJWT = () => {
  localStorage.removeItem('token');
  console.log(localStorage.getItem('token'));
};

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
