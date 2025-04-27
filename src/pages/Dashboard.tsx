import React from "react";
import { useTheme } from "../ThemeContext";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

const Dashboard: React.FC = () => {
  const { darkMode } = useTheme();
  const { userId, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/signin");
  };

  return (
    <div className={`w-full h-screen flex flex-col ${darkMode ? "bg-gray-900" : "bg-gray-50"}`}>
      {/* Optional Header */}
      <div className="p-4 flex justify-between items-center bg-opacity-80 backdrop-blur-md shadow-md">
        <h1 className="text-xl font-semibold text-white">
          Dashboard {userId ? `(User ${userId})` : ""}
        </h1>
        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-md"
        >
          Log Out
        </button>
      </div>

      {/* Dash App iframe */}
      <iframe
        src="http://localhost:8050"
        className="flex-1"
        style={{
          border: "none",
          backgroundColor: darkMode ? "#111827" : "#f9fafb",
        }}
      />
    </div>
  );
};

export default Dashboard;
