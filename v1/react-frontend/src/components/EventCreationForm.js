import React, { useState } from 'react';
import './EventCreationForm.css'
import Sidebar from './Sidebar';
import AdminHeader from './AdminHeader'

const EventCreationForm = () => {
  // Helper function to get today's date
  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const [formData, setFormData] = useState({
    name: '',
    date: getTodayDate(), // Default date is today in YYYY-MM-DD format
    location: '',
    description: '',
    privacy: 'public' // Default to public
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handlePrivacyChange = (e) => {
    setFormData({
      ...formData,
      privacy: e.target.value
    });
  };

  const validateForm = () => {
    const { name, date, location } = formData;
    let formErrors = {};
    if (!name) formErrors.name = 'Event name is required';
    if (!date) formErrors.date = 'Event date is required';
    if (!location) formErrors.location = 'Event location is required';
    return formErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formErrors = validateForm();
    if (Object.keys(formErrors).length === 0) {
      // Handle form submission (e.g., send data to server)
      console.log('Event data submitted:', formData);
      // Optionally, reset form or navigate to another page
    } else {
      setErrors(formErrors);
    }
  };

  const handleCancel = () => {
    // Reset form data or navigate away
    setFormData({
      name: '',
      date: getTodayDate(), // Reset to today’s date in YYYY-MM-DD format
      location: '',
      description: '',
      privacy: 'public'
    });
    setErrors({});
  };

  return (
    <>
      <AdminHeader />
      <div>
        <Sidebar />
      </div>
      <div className="event-creation-form">
        <h2>Create Event</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="name">Event Name</label>
            <input
              type="text"
              id="name"
              name="name"
              placeholder='name'
              value={formData.name}
              onChange={handleChange}
            />
            {errors.name && <p className="error">{errors.name}</p>}
          </div>
          <div>
            <label htmlFor="date">Event Date</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
            />
            {errors.date && <p className="error">{errors.date}</p>}
          </div>
          <div>
            <label htmlFor="location">Event Location</label>
            <input
              type="text"
              id="location"
              name="location"
              placeholder='location'
              value={formData.location}
              onChange={handleChange}
            />
            {errors.location && <p className="error">{errors.location}</p>}
          </div>
          <div>
            <label htmlFor="description">Event Description</label>
            <textarea
              id="description"
              name="description"
              placeholder='description...'
              value={formData.description}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Privacy</label>
            <div>
              <label>
                <input
                  type="radio"
                  name="privacy"
                  value="public"
                  checked={formData.privacy === 'public'}
                  onChange={handlePrivacyChange}
                />
                Public
              </label>
              <label>
                <input
                  type="radio"
                  name="privacy"
                  value="private"
                  checked={formData.privacy === 'private'}
                  onChange={handlePrivacyChange}
                />
                Private
              </label>
            </div>
          </div>
          <button type="submit">Save</button>
          <button type="button" onClick={handleCancel}>Cancel</button>
        </form>
      </div>
    </>
  );
};

export default EventCreationForm;
