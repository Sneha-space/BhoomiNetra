import os
import cv2
from .image_enhancer import CVProcessor
from .image_processor import PaddleOCRProcessor,TextProcessor
from .text_processor import LLMTextExtractor,RegexTextExtractor
from ..utils.file_type_det import guess_file_type
from ..services.pdf_to_img import extract_images_from_pdf
from ..core.config import UPLOAD_DIR
from ..services.ingest import save_document_results

from ..core.session_maker import get_session,delete_session,stop_session
class MlPipeline:
    def __init__(self):
        self.guess_file_type = guess_file_type
        self.extract_images_from_pdf = extract_images_from_pdf
        self.cvprocessor = CVProcessor()
        self.ocr_processor = PaddleOCRProcessor()
        self.text_processor = TextProcessor()
        self.text_extractor = RegexTextExtractor() # LLMTextExtractor("Qwen/Qwen3.5-4B")
    def process(self,key:str):
        path = os.path.join(UPLOAD_DIR,key)
        ftype = guess_file_type(path)
        if ftype=="pdf":
            list_image_bytes = self.extract_images_from_pdf(path)
            images = self.cvprocessor.process_bytes(list_image_bytes)
        elif ftype in ["png","jpg","jpeg"]:
            images = [cv2.imread(path)]
        else:
            raise TypeError("File type should be pdf or image(png,jpg.jpeg)")
        images = self.cvprocessor.process(images)
        ocr_result = self.ocr_processor.process(images)
        text_result = self.text_processor.process(ocr_result) #dict{text,low_confidence_text,confidence}
        result = self.text_extractor.process(text_result["text"])
        self.ingest_to_db(key,result,text_result["confidence"])
        stop_session(key)
        return result
    def ingest_to_db(self,key,result,confidence):
        session = get_session(key)
        doc_id = session["doc_id"]
        pages = format_output(result,confidence)
        save_document_results(doc_id,pages)
        


def format_output(result,confidence)->list[list[dict]]:
    output = []
    for i,plot in enumerate(result["plot_area"]["per_plot"]):
        info = {
            "owner_name":{"value":result["landowner_details"]["name"],"confidence":confidence},
            "guardian":{"value":result["landowner_details"]["guardian"],"confidence":confidence},
            "survey_number":{"value":result["survey_number"],"confidence":confidence},
            "khasra_number":{"value":plot["plot_no"],"confidence":confidence},
            "khata_number":{"value":result["khata_number"],"confidence":confidence},
            "area":{"value":plot["total_plot_area"],"confidence":confidence},
            "ocupier_share":{"value":plot["occupier_share"],"confidence":confidence},
            "share_area":{"value":plot["share_area"],"confidence":confidence},
            "village":{"value":result["village"],"confidence":confidence},
            "tehsil":{"value":result["tehsil"],"confidence":confidence},
            "district":{"value":result["district"],"confidence":confidence},
            "state":{"value":None,"confidence":confidence},
            "land_classification":{"value":result["land_classification"][i],"confidence":confidence},
            "mutation_number":{"value":result["mutation_records"],"confidence":confidence},
            "mutation_date":{"value":result["registration_information"]["certification_date"],"confidence":confidence},
            "registration_number":{"value":result["registration_information"]["copy_no"],"confidence":confidence},
        }
        output.append(info)
    return [output]


