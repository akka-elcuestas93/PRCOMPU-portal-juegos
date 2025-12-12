import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  withCredentials: true,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    // quítalo si tu backend NO usa API_KEY
    Authorization: `Bearer ${import.meta.env.VITE_API_KEY || "dev-123"}`,
  },
});

export default http;
