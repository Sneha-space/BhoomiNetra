import regex as re
from transformers import AutoModelForCausalLM, AutoTokenizer
from .prompt import EXTRACTOR_MODEL_PROMPT

FIELD_LABELS = {
    "district":            "District",
    "khata_number":        "Khatian No",       
    "survey_number":       "J.L.No",           
    "village":             "Mouza",
    "tehsil":              "Police Station",
    "prep_date":           "Khatian Prep.Date",
    "total_plots":         "Total Plots",
    "landowner_name":      "Name",
    "guardian_name":       "Father/Husband",
    "landowner_address":   "Address",
    "plotwise_section":    "Plot-wise Land Details",
    "total_khatian_count": "Total Khatian Count",
    "fees_received":       "Fees Received",
    "signed_by":           "Digitally signed by",
}



class LLMTextExtractor:
    def __init__(self,model_name):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    def process(self,text):
        prompt = EXTRACTOR_MODEL_PROMPT + f"""<<<\n{text}\n>>>\nJSON:"""
        messages = [
            {"role": "system", "content": "You are an helpful ai for converting unstructured data to structured data by extracting relevant fields"},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_p=0.8,
            top_k=20,
            repetition_penalty=1.3,
            no_repeat_ngram_size=4,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,       
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response


class RegexTextExtractor:
    def __init__(self):
        self.field_patterns = {}
        self.total_area_pat = re.compile(r"Land\s*Area\s*Dec\.?\s*[:\-]*\s*(?P<value>[\d.]+)", re.IGNORECASE)
        self.plot_row_pat = re.compile(
            r"^(?P<plot_no>\d+)\t"
            r"(?P<land_class>[A-Za-z]+)\t"
            r"(?P<remarks>From\s*Kh\.?No\.?-?\s*[\d,\s]+)\t"
            r"(?P<total_plot_area>[\d.]+)\t"
            r"(?P<occupier_share>[\d.]+)\t"
            r"(?P<share_area>[\d.]+)",
            re.IGNORECASE,
        )
        self.ownership_type_pat = re.compile(r"\b(Raiyat|Bargadar|Sikimi|Under\s*Raiyat)\b", re.IGNORECASE)
        self.registration_pat = re.compile(r"Certified to be true copy.*?(?:Act\s*\d+\s*of\s*\d+\)?)", re.IGNORECASE | re.DOTALL)
        self.cert_date_pat = re.compile(r"Digitally\s*signed.*?Date\s*[:\-]?\s*(?P<value>\d{4}\.\d{2}\.\d{2})",re.IGNORECASE | re.DOTALL)
        self.ref_code_pat = re.compile(r"\[(?P<value>\d+)\]")
        self.mutation_pat = re.compile(r"(?:mutation){e<=1}", re.IGNORECASE)
        self.copy_no_pat = re.compile(r"Copy\s*No\s*[:\-]?\s*(?P<value>\d+)", re.IGNORECASE)
        self.district_pat = re.compile(r"(?im)^\s*District\s*[:\-]?\s*(.+?)\s*^\t&")
    def process(self,text:str):
        rows = self.load_rows(text)
        return self.extract_header_fields(rows)
    def extract_specialized(self,text):
        out = {}
        m = self.total_area_pat.search(text)
        out["total_land_area_dec"] = m.group("value") if m else None
        out["ownership_type"] = None
        m = self.ownership_type_pat.search(text)
        out["ownership_type"] = m.group(1)
        m = self.registration_pat.search(text)
        out["registration_statement"] = re.sub(r"\s+", " ", m.group(0)).strip() if m else None
        m = self.copy_no_pat.search(text)
        out["copy_no"] = m.group("value") if m else None

    def label_regex(self,label):
        escaped = re.escape(label)
        escaped = escaped.replace(r"\ ", r"\s*")
        escaped = escaped.replace(r"\.", r"\.?")
        return re.compile(
            rf"^\(?\d{{0,2}}\)?\s*{escaped}\s*[:\-]*\s*(?P<val>.*)$",
            re.IGNORECASE,
        )
    def generate_patterns(self):
        for name,lbl in FIELD_LABELS.items():
            self.field_patterns[name] = self.label_regex(lbl)
    def load_rows(self,text):
        text = text.replace("\r", "")
        rows = []
        for line in text.split("\n"):
            cells = [c.strip() for c in line.split("\t")]
            cells = [c for c in cells if c != ""]   # drop empty trailing cells
            if cells:
                rows.append(cells)
        return rows
    def extract_header_fields(self,rows):
        found = {}
        for row in rows:
            for i, cell in enumerate(row):
                for field, pattern in self.field_patterns.items():
                    if field in found:
                        continue
                    m = pattern.match(cell)
                    if m:
                        val = m.group("val").strip()
                        if not val and i + 1 < len(row):
                            val = row[i + 1].strip()
                        found[field] = val or None
        return found


    
