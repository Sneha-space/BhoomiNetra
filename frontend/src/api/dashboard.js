import api from "./client";

/**
 * Get dashboard data: status counts + needs_review + verified lists
 */
export const getDashboard = () => {
  return api.get("/dashboard");
};
