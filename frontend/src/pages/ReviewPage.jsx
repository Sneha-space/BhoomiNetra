import React, { useState } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import useRecord from "../hooks/useRecord";
import RecordHeader from "../components/review/RecordHeader";
import FieldRow from "../components/review/FieldRow";
import Button from "../components/common/Button";
import { FieldListSkeleton, Skeleton } from "../components/common/Skeleton";

export default function ReviewPage() {
  const { recordId } = useParams();
  const navigate = useNavigate();
  const { record, loading, error, verifying, submitVerification } = useRecord(recordId);

  // Track corrections locally: { field_id: corrected_value }
  const [corrections, setCorrections] = useState({});
  const [successMsg, setSuccessMsg] = useState(null);

  const handleCorrectionChange = (fieldId, value) => {
    const original = record?.fields.find((f) => f.field_id === fieldId)?.value ?? "";
    setCorrections((prev) => {
      const next = { ...prev };
      // saving the original value back is not a correction — drop it
      if (value === original) delete next[fieldId];
      else next[fieldId] = value;
      return next;
    });
  };

  const handleVerify = async () => {
    // Build the payload expected by the API
    const payload = Object.entries(corrections).map(([field_id, corrected_value]) => ({
      field_id: Number(field_id),
      corrected_value,
    }));

    try {
      await submitVerification(payload);
      setSuccessMsg("Record verified successfully!");
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      // error is already set in the hook
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto space-y-6">
        <Skeleton className="h-4 w-32" />
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <div className="flex items-center gap-3 mb-2">
            <Skeleton className="h-7 w-36" />
            <Skeleton className="h-6 w-24 rounded-full" />
          </div>
          <Skeleton className="h-4 w-48" />
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-4 w-16" />
          </div>
          <FieldListSkeleton />
        </div>
      </div>
    );
  }


  if (error && !record) {
    return (
      <div className="max-w-lg mx-auto mt-20 text-center">
        <div className="bg-rose-50 text-rose-700 rounded-2xl p-6 border border-rose-100">
          <p className="font-medium mb-2">Could not load record</p>
          <p className="text-sm mb-4">{error}</p>
          <Link to="/">
            <Button variant="secondary" size="sm">
              Back to Dashboard
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const fields = record?.fields || [];
  const isVerified = record?.status === "verified";

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Back link */}
      <Link
        to="/"
        className="inline-flex items-center text-sm text-gray-500 hover:text-emerald-600"
      >
        <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </Link>

      <RecordHeader record={record} />

      {/* Fields */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-gray-900">Extracted Fields</h2>
          <span className="text-sm text-gray-500">{fields.length} fields</span>
        </div>

        {fields.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-100 p-8 text-center text-gray-500 text-sm">
            No fields extracted for this record.
          </div>
        ) : (
          fields.map((field) => (
            <FieldRow
              key={field.field_id}
              field={{
                ...field,
                // Show the latest local correction if any
                display_value:
                  corrections[field.field_id] !== undefined
                    ? corrections[field.field_id]
                    : field.display_value,
                corrected_value:
                  corrections[field.field_id] !== undefined
                    ? corrections[field.field_id]
                    : field.corrected_value,
              }}
              onCorrectionChange={handleCorrectionChange}
              readOnly={isVerified}
            />
          ))
        )}
      </div>

      {/* Actions */}
      {!isVerified && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 sticky bottom-4">
          {error && (
            <div className="mb-3 text-sm text-rose-600 bg-rose-50 px-3 py-2 rounded-lg">
              {error}
            </div>
          )}
          {successMsg && (
            <div className="mb-3 text-sm text-emerald-700 bg-emerald-50 px-3 py-2 rounded-lg">
              {successMsg}
            </div>
          )}

          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-gray-500">
              {Object.keys(corrections).length > 0
                ? `${Object.keys(corrections).length} field(s) corrected`
                : "No corrections made — mark as verified"}
            </p>
            <Button onClick={handleVerify} loading={verifying} disabled={verifying}>
              {verifying ? "Verifying…" : "Verify Record"}
            </Button>
          </div>
        </div>
      )}

      {isVerified && (
        <div className="bg-emerald-50 border border-emerald-100 text-emerald-800 rounded-2xl p-5 text-center">
          <p className="font-medium">This record has been verified.</p>
        </div>
      )}
    </div>
  );
}
