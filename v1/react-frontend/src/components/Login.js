import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Login.css'
import axios from 'axios';
import event from './assets/event.png'
const baseUrl = require('../apiBaseUrl');

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const navigate = useNavigate();

  const goToDashboard = () => {
    navigate('/admin');
  };

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validateForm = () => {
    const { email, password } = formData;
    let formErrors = {};
    if (!email) formErrors.email = 'Email is required';
    if (!password) formErrors.password = 'Password is required';
    return formErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formErrors = validateForm();
    if (Object.keys(formErrors).length === 0) {
      // Handle form submission (e.g., send data to server)
      console.log('Form data submitted:', formData);
      axios.post(`${baseUrl}/users/auth`, formData)
        .then((response) => {
          console.log(response);
          console.log(response.data);
          if (response.status === 200) {
            const result = response.data;
            localStorage.setItem('token', result.token);
            const token = localStorage.getItem('token');
            console.log(`Local storage ${token}`);
            localStorage.setItem('user', result.result)
            goToDashboard();
          }
        })
        .catch((error) => {
          console.log(error);
          console.log(error.data);
        })
    } else {
      setErrors(formErrors);
    }
  };

  return (
    <div className="login-form">
      <img src={event} alt="Login" className="form-image" />
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.email}</p>}
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && <p className="error">{errors.password}</p>}
        </div>
        <div><Link>forget password</Link></div>
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
};

export default LoginForm;
