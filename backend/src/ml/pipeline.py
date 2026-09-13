import cv2
from .image_enhancer import CVProcessor
from .image_processor import PaddleOCRProcessor,TextProcessor
from .text_processor import LLMTextExtractor,RegexTextExtractor
from ..utils.file_type_det import guess_file_type
from ..services.pdf_to_img import extract_images_from_pdf
class MlPipeline:
    def __init__(self):
        self.guess_file_type = guess_file_type
        self.extract_images_from_pdf = extract_images_from_pdf
        self.cvprocessor = CVProcessor()
        self.ocr_processor = PaddleOCRProcessor()
        self.text_processor = TextProcessor()
        self.text_extractor = RegexTextExtractor() # LLMTextExtractor("Qwen/Qwen3.5-4B")
    def process(self,path:str):
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
        text = self.text_processor.process(ocr_result)["text"]
        result = self.text_extractor.process(text)
        return result
