import axios from "axios";
import config from "../config";

// Central API client - all requests go through here
const api = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: config.timeout,
  headers: {
    "Content-Type": "application/json",
  },
});

// Global error logging (helpful during development)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Something went wrong";
    console.error("API Error:", message);
    return Promise.reject(error);
  }
);

export default api;
