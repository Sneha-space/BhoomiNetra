import { useState } from "react";
import { uploadDocument } from "../api/documents";
import config from "../config";

export default function useUpload() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const upload = async (file) => {
    setError(null);
    setResult(null);

    // Client-side validation
    if (!file) {
      setError("Please select a file");
      return null;
    }

    if (!config.acceptedFileTypes.includes(file.type)) {
      setError("Only PDF, JPG and PNG files are allowed");
      return null;
    }

    const maxBytes = config.maxFileSizeMB * 1024 * 1024;
    if (file.size > maxBytes) {
      setError(`File is too large. Maximum size is ${config.maxFileSizeMB} MB`);
      return null;
    }

    setUploading(true);
    try {
      const res = await uploadDocument(file);
      setResult(res.data);
      return res.data;
    } catch (err) {
      const status = err.response?.status;
      let message = "Upload failed";

      if (status === 413) message = "File is too large (max 25 MB)";
      else if (status === 415) message = "Unsupported file type. Use PDF, JPG or PNG";
      else if (status === 422) message = "No file was sent";
      else message = err.response?.data?.detail || err.message || message;

      setError(message);
      return null;
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setError(null);
    setResult(null);
  };

  return { upload, uploading, error, result, reset };
}
