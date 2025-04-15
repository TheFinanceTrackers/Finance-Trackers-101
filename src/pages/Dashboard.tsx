import React from "react";
import { useTheme } from "../ThemeContext";

const Dashboard: React.FC = () => {
  const { darkMode } = useTheme(); // ✅ Correct placement inside component

  return (
    <div className={`w-full h-screen ${darkMode ? "bg-gray-900" : "bg-gray-50"}`}>
      <iframe
        src="http://localhost:8050"
        width="100%"
        height="100%"
        style={{
          border: "none",
          backgroundColor: darkMode ? "#111827" : "#f9fafb", // Adjust iframe bg
        }}
      ></iframe>
    </div>
  );
};

export default Dashboard;
