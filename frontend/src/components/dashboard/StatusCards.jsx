import React from "react";

const cards = [
  {
    key: "needs_review",
    label: "Needs Review",
    color: "amber",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    ),
  },
  {
    key: "auto_approved",
    label: "Auto Approved",
    color: "sky",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    key: "verified",
    label: "Verified",
    color: "emerald",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
      </svg>
    ),
  },
];

const colorMap = {
  amber: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    iconBg: "bg-amber-100",
    iconText: "text-amber-600",
  },
  sky: {
    bg: "bg-sky-50",
    text: "text-sky-700",
    iconBg: "bg-sky-100",
    iconText: "text-sky-600",
  },
  emerald: {
    bg: "bg-emerald-50",
    text: "text-emerald-700",
    iconBg: "bg-emerald-100",
    iconText: "text-emerald-600",
  },
};

export default function StatusCards({ counts = {} }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {cards.map((card) => {
        const colors = colorMap[card.color];
        const value = counts[card.key] ?? 0;

        return (
          <div
            key={card.key}
            className={`${colors.bg} rounded-2xl p-5 border border-white/60 shadow-sm`}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.label}</p>
                <p className={`text-3xl font-semibold mt-1 ${colors.text}`}>{value}</p>
              </div>
              <div className={`${colors.iconBg} ${colors.iconText} p-2.5 rounded-xl`}>
                {card.icon}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
