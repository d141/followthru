import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Contacts from "./pages/Contacts";
import "./index.css"; // Import Tailwind styles

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/contacts" element={<Contacts />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="*" element={"<h1>404 - Page Not Found</h1>"} /> {/* Handle unknown routes */}
      </Routes>
    </Router>
  );
};

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
