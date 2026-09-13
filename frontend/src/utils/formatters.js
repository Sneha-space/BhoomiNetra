export const formatConfidence = (value) => {
  if (value === null || value === undefined) return "—";
  return `${Math.round(value * 100)}%`;
};

export const formatStatus = (status) => {
  const map = {
    needs_review: "Needs Review",
    auto_approved: "Auto Approved",
    verified: "Verified",
  };
  return map[status] || status;
};
