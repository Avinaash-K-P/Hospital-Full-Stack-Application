import { useState, useEffect } from "react";
import API from "../services/api";

export default function Appointments() {
  const [doctorId, setDoctorId] = useState("");
  const [patientId, setPatientId] = useState("");

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = (event) => {
      console.log("WS MESSAGE:", event.data);
      alert(event.data);
    };

    return () => ws.close();
  }, []);

 const book = async () => {
  if (!doctorId || !patientId) {
    alert("Please enter Doctor ID and Patient ID");
    return;
  }

  try {
    await API.post("/appointment/", {
      doctor_id: parseInt(doctorId),
      patient_id: parseInt(patientId),
      appointment_date: new Date().toISOString(),
      status: "Scheduled"
    });

    alert("Appointment booked");
  } catch (err) {
    console.error("BOOK ERROR:", err.response?.data || err);
    alert("Booking failed");
  }
};

  return (
    <div>
      <h2>Book Appointment</h2>

      <input
        placeholder="Doctor ID"
        onChange={(e) => setDoctorId(e.target.value)}
      />

      <input
        placeholder="Patient ID"
        onChange={(e) => setPatientId(e.target.value)}
      />

      <button onClick={book}>Book</button>
    </div>
  );
}