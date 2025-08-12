// src/lib/api.js
import axios from "axios";

// Use env var if provided, else default local server
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export default api;
