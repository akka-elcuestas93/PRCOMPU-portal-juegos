import axios from "axios";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  withCredentials: true,      // ← Cookies on!
  timeout: 10000,
});

export default http;
