import React from "react";
import Badge from "../common/Badge";

export default function RecordHeader({ record }) {
  if (!record) return null;

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-xl font-semibold text-gray-900">
              Record #{record.record_number}
            </h1>
            <Badge status={record.status} />
          </div>
          <p className="text-sm text-gray-500">
            {record.filename} · Page {record.page_number}
          </p>
        </div>
      </div>
    </div>
  );
}
