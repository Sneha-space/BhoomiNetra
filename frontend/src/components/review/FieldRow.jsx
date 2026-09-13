import React, { useState } from "react";
import { getFieldLabel } from "../../utils/fieldLabels";
import { getConfidenceClasses } from "../../utils/confidenceColor";
import { formatConfidence } from "../../utils/formatters";

// readOnly: set for verified records — the value is shown but cannot be edited
export default function FieldRow({ field, onCorrectionChange, readOnly = false }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(field.display_value || "");

  const confidence = getConfidenceClasses(field.confidence);

  // only a value that differs from what the machine read counts as a change
  const isChanged =
    field.corrected_value != null && field.corrected_value !== (field.value ?? "");

  const startEdit = () => {
    setEditValue(field.corrected_value ?? field.display_value ?? "");
    setIsEditing(true);
  };

  const cancelEdit = () => {
    setIsEditing(false);
  };

  const saveEdit = () => {
    onCorrectionChange?.(field.field_id, editValue);
    setIsEditing(false);
  };

  return (
    <div className="bg-white rounded-xl border border-gray-100 p-4 hover:border-emerald-100 transition-colors">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-sm font-medium text-gray-700">
              {getFieldLabel(field.name)}
            </span>
            <span
              className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${confidence.bg} ${confidence.text} ${confidence.border}`}
            >
              {formatConfidence(field.confidence)} · {confidence.label}
            </span>
          </div>

          {isEditing && !readOnly ? (
            <div className="mt-2 flex items-center gap-2">
              <input
                type="text"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                className="flex-1 px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                autoFocus
              />
              <button
                onClick={saveEdit}
                className="px-3 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700"
              >
                Save
              </button>
              <button
                onClick={cancelEdit}
                className="px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Cancel
              </button>
            </div>
          ) : (
            <div>
              <p className="text-base text-gray-900 font-medium break-words">
                {field.display_value || (
                  <span className="text-gray-400 italic">Not found</span>
                )}
              </p>
              {isChanged && (
                <p className="text-sm text-gray-500 mt-1">
                  Original:{" "}
                  {field.value ? (
                    <span className="line-through">{field.value}</span>
                  ) : (
                    <span className="italic">Not found</span>
                  )}
                </p>
              )}
            </div>
          )}
        </div>

        {!isEditing && !readOnly && (
          <button
            onClick={startEdit}
            className="shrink-0 text-sm text-emerald-600 hover:text-emerald-700 font-medium px-2 py-1 rounded-md hover:bg-emerald-50"
          >
            Edit
          </button>
        )}
      </div>
    </div>
  );
}
