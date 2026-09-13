import React from "react";

const variants = {
  primary:
    "bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm border border-transparent",
  secondary:
    "bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 shadow-sm",
  danger:
    "bg-rose-600 hover:bg-rose-700 text-white shadow-sm border border-transparent",
  ghost: "bg-transparent hover:bg-gray-100 text-gray-600 border border-transparent",
};

const sizes = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-sm",
  lg: "px-5 py-2.5 text-base",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  disabled = false,
  loading = false,
  className = "",
  type = "button",
  onClick,
  ...props
}) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`
        inline-flex items-center justify-center gap-2 font-medium rounded-lg
        transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-1
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variants[variant]} ${sizes[size]} ${className}
      `}
      {...props}
    >
      {loading && (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      )}
      {children}
    </button>
  );
}
