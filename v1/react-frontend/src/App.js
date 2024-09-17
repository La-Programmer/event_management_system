import React from "react";
import {BrowserRouter, Route, Routes } from "react-router-dom";
import { EventProvider } from "./context/eventContext";
import RegistrationForm from "./components/register";
import LoginForm from "./components/Login";
import EventCreationForm from "./components/EventCreationForm";
import Dashboard from "./components/Dashboard";
import Home from "./components/Home"
import EventManagement from './components/EventManagement'
import InviteeRSVPPage from "./components/InviteeRSVPPage";
import RSVPList from "./components/RSVPList";
import InvitationForm from "./components/InvitationForm";


const App = () => {
  

  return (
    <>
      <EventProvider>
        <BrowserRouter>
          <Routes>

            <Route path="/" element={<Home />}></Route>

            <Route path="/event-create" element={<EventCreationForm />}></Route>
            <Route path="/admin" element={<Dashboard />}></Route>
            <Route path="/login" element={<LoginForm />}></Route>
            <Route path="/register" element={<RegistrationForm />}></Route>
            <Route path="/admin/eventmanage" element={<EventManagement />}></Route>
            <Route path="/rsvp" element={<InviteeRSVPPage />}></Route>
            <Route path="/rsvplist" element={<RSVPList />}></Route>

            <Route path="/invite" element={ <InvitationForm/> } />
          </Routes>
        </BrowserRouter>
      </EventProvider>
    </>
  );
} 

export default App;
