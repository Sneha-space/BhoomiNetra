from src.ml.image_enhancer import CVProcessor
from src.services.pdf_to_img import extract_images_from_pdf
from src.ml.text_ext_ocr import PaddleOCRProcessor,TextProcessor
from src.ml.field_extractor import LLMTextExtractor,RegexTextExtractor
import time
import cv2
import json
processor = CVProcessor()
ocr_processor = PaddleOCRProcessor()
text_processor = TextProcessor()
# llm_extractor = LLMTextExtractor(model_name = "Qwen/Qwen3.5-4B")
regex_ext = RegexTextExtractor()


if __name__=="__main__":
    image_bytes = extract_images_from_pdf(r"D:\Diagrams\DigiLanDoc\Data\land_record1.pdf") #land record address
    images = processor.process_bytes(image_bytes)
    # # images = [cv2.imread(r"D:\Diagrams\DigiLanDoc\Data\Land SSIHE Record_page-0002.jpg"),
    # #           cv2.imread(r"D:\Diagrams\DigiLanDoc\Data\Land SSIHE Record_page-0002.jpg")]
    print("Processing Image...")
    images = processor.process(images)
    st = time.perf_counter()   
    print("Start OCR...")
    res = ocr_processor.process(images)
    mid = time.perf_counter()
    print("Start OCR Postprocessing...")
    text = text_processor.process(res)["text"]
    result = regex_ext.process(text) ## or llm_extractor.process(text)
    
    end = time.perf_counter()
    print(result)
    with open("response.json","w",encoding="utf-8") as f:
        json.dump({"response":result},f)
    print(f"Total Time taken : {end-st} Sec")
    print(f"Processing Time : {mid-st} Sec")
    print(f"Post-Processing Time : {end-mid} Sec")