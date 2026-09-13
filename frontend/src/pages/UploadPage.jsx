import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useUpload from "../hooks/useUpload";
import FileDropzone from "../components/upload/FileDropzone";
import Button from "../components/common/Button";

export default function UploadPage() {
  const navigate = useNavigate();
  const { upload, uploading, error, result, reset } = useUpload();
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const data = await upload(file);
    if (data) {
      // After successful upload, go back to dashboard
      setTimeout(() => navigate("/"), 1500);
    }
  };

  return (
    <div className="max-w-xl mx-auto">
      <div className="mb-8">
        <Link
          to="/"
          className="inline-flex items-center text-sm text-gray-500 hover:text-emerald-600 mb-4"
        >
          <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Dashboard
        </Link>
        <h1 className="text-2xl font-semibold text-gray-900">Upload Land Record</h1>
        <p className="text-sm text-gray-500 mt-1">
          Upload a PDF, JPG or PNG file. Processing will start automatically.
        </p>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-6">
        <FileDropzone
          onFileSelect={(f) => {
            setFile(f);
            reset();
          }}
          disabled={uploading}
        />

        {error && (
          <div className="rounded-xl bg-rose-50 border border-rose-100 text-rose-700 px-4 py-3 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-800 px-4 py-3 text-sm">
            <p className="font-medium">Upload successful!</p>
            <p className="mt-1 text-emerald-700">
              Document ID: {result.document_id} · Status: {result.status}
            </p>
            <p className="mt-1 text-xs text-emerald-600">Redirecting to dashboard…</p>
          </div>
        )}

        <div className="flex items-center gap-3">
          <Button
            onClick={handleUpload}
            disabled={!file || uploading || !!result}
            loading={uploading}
            className="flex-1"
          >
            {uploading ? "Uploading…" : "Upload Document"}
          </Button>
          <Link to="/">
            <Button variant="secondary" disabled={uploading}>
              Cancel
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
