import axios from "axios";

const api = axios.create({
  baseURL: "https://esg-ingestion-platform.onrender.com/api",
});

export default api;