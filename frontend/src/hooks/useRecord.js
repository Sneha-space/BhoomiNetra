import { useState, useEffect, useCallback } from "react";
import { getRecord, verifyRecord } from "../api/records";

export default function useRecord(recordId) {
  const [record, setRecord] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [verifying, setVerifying] = useState(false);

  const fetchRecord = useCallback(async () => {
    if (!recordId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getRecord(recordId);
      setRecord(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to load record");
    } finally {
      setLoading(false);
    }
  }, [recordId]);

  useEffect(() => {
    fetchRecord();
  }, [fetchRecord]);

  const submitVerification = async (corrections) => {
    setVerifying(true);
    setError(null);
    try {
      const res = await verifyRecord(recordId, corrections);
      // Update local state to verified
      setRecord((prev) => (prev ? { ...prev, status: "verified" } : prev));
      return res.data;
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Verification failed";
      setError(msg);
      throw err;
    } finally {
      setVerifying(false);
    }
  };

  return {
    record,
    loading,
    error,
    verifying,
    refetch: fetchRecord,
    submitVerification,
  };
}
