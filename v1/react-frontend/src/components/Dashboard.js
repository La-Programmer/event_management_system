import React from 'react';
import './Dashboard.css';
import Sidebar from './Sidebar';
import  AdminHeader from './AdminHeader'

const Dashboard = () => {
    return (
        <>
        <AdminHeader />
        <div>
        <div className='sidebar'>
            <Sidebar />
        </div>
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>Dashboard</h1>
                <p>Welcome to the Admin Dashboard. Here you can get an overview of your events, users, and more.</p>
            </header>
            <div className="dashboard-cards">
                <div className="dashboard-card">
                    <h2>Total Events</h2>
                    <p>35</p> {/* Replace with dynamic data */}
                </div>
                <div className="dashboard-card">
                    <h2>Upcoming Events</h2>
                    <p>12</p> {/* Replace with dynamic data */}
                </div>
                <div className="dashboard-card">
                    <h2>Total Users</h2>
                    <p>180</p> {/* Replace with dynamic data */}
                </div>
                <div className="dashboard-card">
                    <h2>Active Users</h2>
                    <p>120</p> {/* Replace with dynamic data */}
                </div>
            </div>
        </div>
        </div>

        </>
    );
};

export default Dashboard;
