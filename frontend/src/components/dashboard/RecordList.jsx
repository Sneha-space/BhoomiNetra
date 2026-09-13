import React from "react";
import { Link } from "react-router-dom";
import Badge from "../common/Badge";
import EmptyState from "../common/EmptyState";

export default function RecordList({ title, records = [], emptyTitle, emptyDescription }) {
  if (!records.length) {
    return (
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100">
          <h2 className="text-base font-semibold text-gray-900">{title}</h2>
        </div>
        <EmptyState title={emptyTitle} description={emptyDescription} />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <h2 className="text-base font-semibold text-gray-900">{title}</h2>
        <span className="text-sm text-gray-500">{records.length} records</span>
      </div>

      <div className="divide-y divide-gray-50">
        {records.map((record) => (
          <Link
            key={record.record_id}
            to={`/records/${record.record_id}`}
            className="flex items-center justify-between px-6 py-4 hover:bg-emerald-50/40 transition-colors group"
          >
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-900 truncate">
                  {record.filename}
                </span>
                <Badge status={record.status || "needs_review"} />
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Record #{record.record_number} · Page {record.page_number}
              </p>
            </div>

            <svg
              className="w-5 h-5 text-gray-300 group-hover:text-emerald-500 transition-colors shrink-0 ml-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        ))}
      </div>
    </div>
  );
}
