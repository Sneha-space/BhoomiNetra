// ============================================================
// CONFIGURATION - Easy to change for the real/production model
// ============================================================
// All user-configurable values live here or in the .env file.
// In the original model, users can simply edit .env or this file.

const config = {
  // Backend base URL (change in .env for different environments)
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",

  // Request timeout in milliseconds
  timeout: 30000,

  // Max file size in MB (matches backend limit)
  maxFileSizeMB: 25,

  // Accepted file types
  acceptedFileTypes: ["application/pdf", "image/jpeg", "image/png"],

  // App name (can be changed later)
  appName: "BhoomiNetra",
  appTagline: "Land Records Intelligence",
};

export default config;
