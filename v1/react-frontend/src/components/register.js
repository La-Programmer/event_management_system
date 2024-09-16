import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './register.css';
import { useNavigate } from 'react-router-dom';
const baseUrl = require('../apiBaseUrl');

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phoneNo: '',
    password: '',
    passwordConfirm: ''
  });

  const navigate = useNavigate();

  const goToLogin = () => {
    navigate('/login');
  }

  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validateForm = () => {
    const { name, email, phoneNo, password, passwordConfirm } = formData;
    let formErrors = {};
    if (!name) formErrors.name = 'Name is required';
    if (!email) formErrors.email = 'Email is required';
    if (!phoneNo) formErrors.phoneNo = 'Phone number is required';
    if (!password) formErrors.password = 'Password is required';
    if (password !== passwordConfirm) formErrors.passwordConfirm = 'Passwords do not match';
    return formErrors;
  };

  const formatFormData = (data) => {
    const fullName = data['name'].split(' ');
    const firstName = fullName[0];
    const lastName = fullName[1];
    const validFormat = {
      first_name: firstName,
      last_name: lastName,
      email: data.email,
      phoneNo: data.phoneNo,
      password: data.password,
    }
    return validFormat;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formErrors = validateForm();
    if (Object.keys(formErrors).length === 0) {
      // Handle form submission (e.g., send data to server)
      const data = formatFormData(formData);
      console.log('Form data submitted:', data);
      axios.post(`${baseUrl}/users/register`, data)
        .then((response) => {
          console.log(response);
          console.log(response.data);
          if (response.status === 200) {
            goToLogin();
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
    <div className="registration-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
          {errors.name && <p className="error">{errors.name}</p>}
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder='ex: example@site.com'
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.email}</p>}
        </div>
        <div>
          <label htmlFor="phoneNo">Phone Number (WhatsApp)</label>
          <input
            type="string"
            id="phoneNo"
            name="phoneNo"
            placeholder='ex: +234 90888432'
            value={formData.phoneNo}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.phoneNo}</p>}
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder='Password'
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && <p className="error">{errors.password}</p>}
        </div>
        <div>
          <label htmlFor="passwordConfirm">Confirm Password</label>
          <input
            type="password"
            id="passwordConfirm"
            name="passwordConfirm"
            placeholder='Confirm Password'
            value={formData.passwordConfirm}
            onChange={handleChange}
          />
          {errors.passwordConfirm && <p className="error">{errors.passwordConfirm}</p>}
        </div>
        <p>By registering, you agree to the privacy policy and terms of service.</p>
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
};

export default RegistrationForm;
