import React from "react";

const statusStyles = {
  needs_review: "bg-amber-50 text-amber-800 border-amber-200",
  auto_approved: "bg-sky-50 text-sky-800 border-sky-200",
  verified: "bg-emerald-50 text-emerald-800 border-emerald-200",
};

const statusLabels = {
  needs_review: "Needs Review",
  auto_approved: "Auto Approved",
  verified: "Verified",
};

export default function Badge({ status, className = "" }) {
  const style = statusStyles[status] || "bg-gray-50 text-gray-700 border-gray-200";
  const label = statusLabels[status] || status;

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${style} ${className}`}
    >
      {label}
    </span>
  );
}
