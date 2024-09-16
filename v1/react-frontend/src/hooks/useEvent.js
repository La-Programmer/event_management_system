import { useContext } from "react";
import EventContext from "../context/eventContext";

export function useEvent() {
    return useContext(EventContext);
}