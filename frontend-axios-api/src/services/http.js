// src/services/http.js
// Servicio Axios para la API externa de DummyJSON (usuarios)
// Parte 1 de la práctica

import axios from "axios";

export const http = axios.create({
  baseURL: "https://dummyjson.com",
  headers: {
    "Content-Type": "application/json",
  },
});
