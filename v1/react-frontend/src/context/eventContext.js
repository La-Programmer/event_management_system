import React, { createContext, useState } from "react";

const EventContext = createContext();

export function EventProvider({ children }) {
  const [event, setEvent] = useState("defaultState");

  return (
    <EventContext.Provider value={{ event, setEvent }}>
      {children}
    </EventContext.Provider>
  )
}

export default EventContext;