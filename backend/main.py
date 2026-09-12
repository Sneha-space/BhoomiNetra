import cv2
from src.ml.image_enhancer import CVProcessor
from src.services.pdf_to_img import extract_images_from_pdf

# Initialize the processor (it automatically loads the AI model)
processor = CVProcessor(use_enhancement=True)

if __name__ == "__main__":
    # 1. Convert PDF pages to image bytes
    image_bytes = extract_images_from_pdf(r"c:\Users\sneha\Downloads\pgms vs nns-Sneha Biswas.pdf")
    
    # 2. Decode bytes into OpenCV images
    images = processor.process_bytes(image_bytes)
    
    # 3. Run Preprocessing + AI Enhancement
    enhanced_images = processor.process(images)
    
    # 4. Display the resulting enhanced images
    for idx, image in enumerate(enhanced_images):
        cv2.imshow(f"Enhanced Page {idx+1}", image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()