// Human-readable labels for API field names
// Easy to edit later for the original model

export const FIELD_LABELS = {
  owner_name: "Owner Name",
  area: "Area",
  survey_number: "Survey Number",
  khasra_number: "Khasra Number",
  khata_number: "Khata Number",
  village: "Village",
  tehsil: "Tehsil",
  district: "District",
  state: "State",
  land_classification: "Land Classification",
  mutation_number: "Mutation Number",
  mutation_date: "Mutation Date",
  registration_number: "Registration Number",
};

export const getFieldLabel = (name) => {
  return FIELD_LABELS[name] || name.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
};
