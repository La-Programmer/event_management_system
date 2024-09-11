import React from "react";
import {BrowserRouter, Route, Routes } from "react-router-dom";

import RegistrationForm from "./components/register";
import LoginForm from "./components/Login";
import EventCreationForm from "./components/EventCreationForm";
import Dashboard from "./components/Dashboard";
import Home from "./components/Home"
import EventManagement from './components/EventManagement'


const App = () => {
  return (
    <>
    <BrowserRouter>
    <Routes>

      <Route path="/" element={<Home />}></Route>

      <Route path="/event" element={<EventCreationForm />}></Route>
      <Route path="/admin" element={<Dashboard />}></Route>
      <Route path="/login" element={<LoginForm />}></Route>
      <Route path="/register" element={<RegistrationForm />}></Route>
      <Route path="/eventmanage" element={<EventManagement />}></Route>
    </Routes>
    </BrowserRouter>
    </>
  );
} 

export default App;
