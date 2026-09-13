/**
 * Returns Tailwind classes based on confidence score (0-1)
 */
export const getConfidenceClasses = (confidence) => {
  if (confidence === null || confidence === undefined) {
    return {
      bg: "bg-gray-100",
      text: "text-gray-600",
      border: "border-gray-200",
      label: "N/A",
    };
  }

  if (confidence >= 0.9) {
    return {
      bg: "bg-emerald-50",
      text: "text-emerald-700",
      border: "border-emerald-200",
      label: "High",
    };
  }

  if (confidence >= 0.7) {
    return {
      bg: "bg-amber-50",
      text: "text-amber-700",
      border: "border-amber-200",
      label: "Medium",
    };
  }

  return {
    bg: "bg-rose-50",
    text: "text-rose-700",
    border: "border-rose-200",
    label: "Low",
  };
};
