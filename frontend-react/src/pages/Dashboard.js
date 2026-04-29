import { useEffect, useState, useCallback } from "react";
import API from "../services/api";

export default function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [doctorId, setDoctorId] = useState("");
  const [patientId, setPatientId] = useState("");
  const [booking, setBooking] = useState(false);

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token");
    window.location.href = "/";
  }, []);

  const fetchDoctors = useCallback(async () => {
    try {
      const res = await API.get("/doctor/search?specialization=");
      setDoctors(res.data.data || []);
    } catch (err) {
      if (err.response?.status === 401) handleLogout();
    }
  }, [handleLogout]);

  const fetchPatients = useCallback(async () => {
  try {
    // We change "name" to "query" to match your backend @router.get("/search")
    // We send an empty string "" so the backend doesn't throw a 422 Required error
    const res = await API.get("/patient/search", {
      params: { query: "" } 
    });
    
    console.log("PATIENT DATA:", res.data);

    // FastAPI usually returns the list directly or inside a 'data' key
    const data = res.data.data || res.data;
    setPatients(Array.isArray(data) ? data : []);
  } catch (err) {
    console.error("Fetch Patients Error:", err.response?.data || err);
    if (err.response?.status === 401) handleLogout();
  }
}, [handleLogout]);

useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return handleLogout();

    fetchDoctors();
    fetchPatients();

    const ws = new WebSocket("ws://127.0.0.1:8000/ws");
    ws.onmessage = (event) => {
      alert(`System Update: ${event.data}`);
      fetchDoctors();
    };
    return () => ws.close();
  }, [fetchDoctors, fetchPatients, handleLogout]);

  const handleBook = async () => {
    if (!doctorId || !patientId) return alert("Select a doctor and patient first!");
    setBooking(true);
    try {
      await API.post("/appointment/", {
        doctor_id: parseInt(doctorId),
        patient_id: parseInt(patientId),
        appointment_date: new Date().toISOString(),
        status: "Scheduled",
      });
      alert("✅ Appointment successfully booked!");
      setDoctorId("");
      setPatientId("");
    } catch (err) {
      alert(" Booking failed.");
    } finally {
      setBooking(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>Medical Dashboard</h1>
        <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
      </header>

      {/* 1. DOCTORS SECTION */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>1. Select a Doctor</h2>
        <div style={styles.listGrid}>
          {doctors.map((doc) => (
            <div 
              key={doc.id} 
              onClick={() => setDoctorId(doc.id)}
              style={{...styles.card, borderColor: doctorId === doc.id ? "#007bff" : "#eee"}}
            >
              <div style={styles.cardInfo}>
                <span style={styles.name}>{doc.name}</span>
                <span style={styles.subtext}>{doc.specialization}</span>
              </div>
              <input type="radio" checked={doctorId === doc.id} readOnly />
            </div>
          ))}
        </div>
      </section>

      {/* 2. PATIENTS SECTION */}
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>2. Select a Patient</h2>
        <div style={styles.listGrid}>
          {patients.map((p) => (
            <div 
              key={p.id} 
              onClick={() => setPatientId(p.id)}
              style={{...styles.card, borderColor: patientId === p.id ? "#28a745" : "#eee"}}
            >
              <div style={styles.cardInfo}>
                <span style={styles.name}>{p.name}</span>
                <span style={styles.subtext}>Age: {p.age} | {p.phone}</span>
              </div>
              <input type="radio" checked={patientId === p.id} readOnly />
            </div>
          ))}
        </div>
      </section>

      {/* 3. APPOINTMENT FORM */}
      <section style={styles.bookingSection}>
        <h2 style={styles.sectionTitle}>3. Book Appointment</h2>
        <div style={styles.formCard}>
          <div style={styles.formRow}>
            <span>Selected Doctor ID:</span> 
            <strong>{doctorId || "None"}</strong>
          </div>
          <div style={styles.formRow}>
            <span>Selected Patient ID:</span> 
            <strong>{patientId || "None"}</strong>
          </div>
          <button 
            disabled={booking || !doctorId || !patientId} 
            onClick={handleBook} 
            style={styles.bookBtn}
          >
            {booking ? "Booking..." : "Confirm Appointment"}
          </button>
        </div>
      </section>
    </div>
  );
}

const styles = {
  container: { maxWidth: "800px", margin: "0 auto", padding: "40px 20px", fontFamily: "sans-serif", backgroundColor: "#fff" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "2px solid #eee", paddingBottom: "20px", marginBottom: "30px" },
  logoutBtn: { padding: "8px 15px", borderRadius: "5px", border: "1px solid #dc3545", color: "#dc3545", backgroundColor: "transparent", cursor: "pointer", fontWeight: "bold" },
  section: { marginBottom: "40px" },
  sectionTitle: { fontSize: "20px", color: "#333", borderLeft: "4px solid #007bff", paddingLeft: "10px", marginBottom: "15px" },
  listGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" },
  card: { padding: "15px", border: "2px solid #eee", borderRadius: "8px", display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer", transition: "0.2s" },
  cardInfo: { display: "flex", flexDirection: "column" },
  name: { fontWeight: "bold", fontSize: "16px" },
  subtext: { fontSize: "13px", color: "#666" },
  bookingSection: { marginTop: "50px", padding: "30px", backgroundColor: "#f8f9fa", borderRadius: "12px" },
  formCard: { display: "flex", flexDirection: "column", gap: "15px" },
  formRow: { display: "flex", justifyContent: "space-between", fontSize: "16px" },
  bookBtn: { marginTop: "10px", padding: "15px", backgroundColor: "#007bff", color: "#white", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer", fontSize: "16px" }
};