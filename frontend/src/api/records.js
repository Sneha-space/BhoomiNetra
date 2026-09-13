import api from "./client";

/**
 * Get a single record with all its fields
 * @param {number|string} recordId
 */
export const getRecord = (recordId) => {
  return api.get(`/records/${recordId}`);
};

/**
 * Verify a record with optional corrections
 * @param {number|string} recordId
 * @param {Array<{field_id: number, corrected_value: string}>} corrections
 */
export const verifyRecord = (recordId, corrections = []) => {
  return api.post(`/records/${recordId}/verify`, {
    corrections,
  });
};
