from src.ml.image_enhancer import CVProcessor
from src.services.pdf_to_img import extract_images_from_pdf
import cv2
processor = CVProcessor()



if __name__=="__main__":
    image_bytes = extract_images_from_pdf(r"D:/College/120308254035_Rikan Maji_AM-305.pdf")
    images = processor.process_bytes(image_bytes)
    for image in images:
        cv2.imshow("IMG",image)
        cv2.waitKey(0)
    