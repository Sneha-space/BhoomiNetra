import api from "./client";

/**
 * Upload a land record file (PDF, JPG or PNG)
 * @param {File} file
 */
export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
