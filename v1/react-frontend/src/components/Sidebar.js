import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css'; // Import the CSS file for Sidebar

const Sidebar = () => {
    return (
        <nav className="sidebar">
            <h2 className="sidebar-title">Event Management</h2>
            <hr></hr>
            <ul className="sidebar-menu">
                <li><Link to="/admin/dashboard" className="sidebar-link">Dashboard</Link></li>
                <li><Link to="/admin/events" className="sidebar-link">Manage Events</Link></li>
                <li><Link to="/admin/users" className="sidebar-link">Manage Users</Link></li>
                <li><Link to="/admin/reports" className="sidebar-link">Reports</Link></li>
                <li><Link to="/admin/settings" className="sidebar-link">Settings</Link></li>
            </ul>
        </nav>
    );
};

export default Sidebar;
