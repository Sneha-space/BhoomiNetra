import os
from dataclasses import dataclass, asdict
import regex as re
# import sys
# from pathlib import Path
"""
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))     
SRC_DIR = os.path.dirname(CURRENT_DIR)                      
# BACKEND_ROOT = os.path.dirname(SRC_DIR)                     
# PROJECT_WORKSPACE = os.path.dirname(BACKEND_ROOT)           
# if PROJECT_WORKSPACE not in sys.path:
#     sys.path.insert(0, PROJECT_WORKSPACE)

# if BACKEND_ROOT not in sys.path:
#     sys.path.insert(0, BACKEND_ROOT)

WEIGHTS_PATH = os.path.join(SRC_DIR,"ml", "indic_ocr_weights")
LAYOUT_WEIGHTS = os.path.join(WEIGHTS_PATH, "weights", "layout")
OCR_WEIGHTS = os.path.join(WEIGHTS_PATH, "weights", "ocr")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ml" / "indic_ocr_weights"))
"""
import numpy as np
import cv2
from paddleocr import PaddleOCR
# import json
# from PIL import Image
# from .indic_ocr_weights.indic_ocr import IndicDocLayout, IndicBlockOCR 
# from .indic_ocr_weights.idp_recognizer import build_requests
# from .indic_ocr_weights.idp_types import CropConfig

# class IndicOCRProcessor:
#     def __init__(self):
#         self.layout_engine = IndicDocLayout(LAYOUT_WEIGHTS)
#         self.ocr_engine = IndicBlockOCR(OCR_WEIGHTS)
#         self.EXCLUDE_TYPES = {"image", "chart", "diagram", "website-link", "advertisement", "flag"}

#     def process(self, rgb_array):
#         pil_image = Image.fromarray(rgb_array)
#         layout_blocks = self.layout_engine.backend.detect(pil_image)
#         crop_cfg = CropConfig()
#         requests,orders = build_requests(layout_blocks,pil_image,crop_cfg,table_format="html")
#         texts = self.ocr_engine.backend.transcribe(requests)
#         order_to_text = dict(zip(orders, texts))
#         final_markdown_output = []
#         structured_json_blocks = []

#         for block in layout_blocks:
#             record = block.as_record()
#             record["text"] = order_to_text.get(record["order"], "")
#             if record["type"].lower() not in self.EXCLUDE_TYPES:
#                 record["text"] = order_to_text.get(record["order"], "")
#                 structured_json_blocks.append(record)
#                 final_markdown_output.append(record["text"])
#             elif record["type"] == "image":
#                 final_markdown_output.append("![Image Block](...)")
#         complete_markdown = "\n\n".join(final_markdown_output)
        
#         return {
#             "markdown": complete_markdown,
#             "json_layout": structured_json_blocks
#         }


@dataclass
class OCRItem:
    text: str
    confidence : float
    x1: float
    cx: float
    cy: float
    width: float
    height: float


class PaddleOCRProcessor:
    def __init__(self,lang="en"):
        self.ocr = PaddleOCR(
            lang=lang,
            device="cpu",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            ocr_version="PP-OCRv4",
            enable_mkldnn=False,
        )
    def process(self,images:list[np.ndarray])->list[dict[str,list]]:
        if isinstance(images,list):
            for i,img in enumerate(images):
                if len(img.shape)!=3:
                    images[i] = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        result = self.ocr.predict(images)
        
        return result
class TextProcessor:
    def process(self,results:list[dict[str,list]])->dict[str,str]: # [{page:page_id, text:}]
        page_text = ""
        confidence = 0
        line_pages = self.post_process(results)
        pages,low_conf_text = self.to_line(line_pages)
        for i,page in enumerate(pages):
            page_text += page.get("text","") + "\n"
            confidence += line_pages[i].get("confidence",0)
        
        text,low_conf_text = self._normalize(page_text), self._normalize(low_conf_text)
        return {"text":text,"low_confidence_text":low_conf_text,"confidence":confidence/len(pages)}
    def _normalize(self,text):
        text = text.replace("\u00a0", " ")
        text = text.replace("N0", "No")
        text = text.replace("n0", "no")
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"\s*:\s*", ": ", text)
        return text


    def post_process(self,results):
        pages = self._info_grouping(results)
        line_pages=[]
        for page in pages:
            items = page.get("items")
            page_idx = page.get("page")
            lines, confidence = self._line_grouping(items)
            line_pages.append({"page":page_idx,"lines":lines,"confidence":confidence})
        return line_pages
    def to_line(self,line_pages):
        page_text = []
        low_conf_text = ""
        for page in line_pages:
            lines = page.get("lines")
            page_idx = page.get("page")
            text = ""
            for line in lines:
                for item in line:
                    text += item.text + "\t"
                    if item.confidence < 0.86:
                        low_conf_text += item.text + " "
                text += "\n"
            page_text.append({"page":page_idx,"text":text})
        return page_text,low_conf_text
    
    def _info_grouping(self,results):
        pages = []
        for page_idx, result in enumerate(results):
            texts = result.get("rec_texts",[])
            conf_scores = result.get("rec_scores",[])
            bboxs = result.get("rec_polys",[])
            items = []
            for text,conf,poly in zip(texts,conf_scores,bboxs):
                if not text or not text.strip():
                    continue
                x1 = float(np.min(poly[:, 0]))
                y1 = float(np.min(poly[:, 1]))
                x2 = float(np.max(poly[:, 0]))
                y2 = float(np.max(poly[:, 1]))
                width = x2 - x1
                height = y2 - y1

                item = OCRItem(
                    text=text.strip(),
                    confidence=float(conf),
                    x1 = x1,
                    cx=(x1 + x2) / 2,
                    cy=(y1 + y2) / 2,
                    width=width,
                    height=height,
                )

                items.append(item)

            pages.append({
                "page": page_idx,
                "items": items
            })
        return pages
    def _line_grouping(self,items, y_threshold_ratio=0.5):
        confidence = 0
        if not items:
            return []
        items = sorted(items, key=lambda x: x.cy)
        lines = []
        for item in items:
            placed = False
            confidence += item.confidence
            for line in lines:
                avg_y = np.mean([x.cy for x in line])
                avg_h = np.mean([x.height for x in line])
                threshold = avg_h * y_threshold_ratio
                if abs(item.cy - avg_y) <= threshold:
                    line.append(item)
                    placed = True
                    break
            if not placed:
                lines.append([item])
        for line in lines:
            line.sort(key=lambda x: x.x1)
        lines.sort(key=lambda line: np.mean([x.cy for x in line]))
        for line_id, line in enumerate(lines):
            for item in line:
                item.line_id = line_id

        return lines,confidence/len(items)





# class EasyOCRProcessor:
#     def __init__(self,lang_list=['eng'],gpu=True):
#         self.ocr = Reader(
#             lang_list=lang_list,
#             gpu=gpu
#         )
#     def process(self,images:list[np.ndarray])->dict:
#         all_batch_results = {}
#         text = ""
#         for idx,image in enumerate(images):
#             result = self.ocr.readtext(image,paragraph=True)
#             all_batch_results[idx] = result
#             for res in result:
#                 text += res[1] + "\n"
#         return result,text