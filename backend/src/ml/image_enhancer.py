import os
import cv2
import numpy as np
import torch
from PIL import Image
from py_real_esrgan.model import RealESRGAN


class CVProcessor:
    def __init__(self, use_enhancement: bool = True):
        self.use_enhancement = use_enhancement
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.model = None
        if self.use_enhancement:
            try:
                # Initialize RealESRGAN with 4x scale factor
                self.model = RealESRGAN(self.device, scale=4)
                
                # Build an absolute path pointing directly to the backend/weights folder
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                weights_path = os.path.join(BASE_DIR, 'weights', 'RealESRGAN_x4plus.pth')

                self.model.load_weights(weights_path, download=False)
            except Exception as e:
                self.model = None

    def process(self, images: list[np.ndarray]) -> list[np.ndarray]:
        image_list = []
        for image in images:
            preprocessed_image = self.preprocess(image)
            
            if self.use_enhancement and self.model is not None:
                enhanced_image = self.enhance(preprocessed_image)
            else:
                enhanced_image = preprocessed_image
                
            image_list.append(enhanced_image)
        return image_list

    def process_bytes(self, list_image_bytes: list) -> list[np.ndarray]:
        images = []
        for image_bytes in list_image_bytes:
            image = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Invalid image bytes")
            images.append(image)
        return images

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        # Force rotation to correct horizontal/landscape scans into a vertical layout
        # If it rotates the wrong way, change to cv2.ROTATE_90_COUNTERCLOCKWISE
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Set explicit vertical dimensions (Width, Height)
        gray = cv2.resize(gray, (720, 1280))
        
        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=10,
            templateWindowSize=7,
            searchWindowSize=21
        )
        return denoised

    def enhance(self, image: np.ndarray) -> np.ndarray:
        try:
            # Convert OpenCV numpy array to PIL Image format expected by py-real-esrgan
            if len(image.shape) == 2:
                pil_img = Image.fromarray(image).convert('RGB')
            else:
                pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                
            # Run AI super-resolution inference
            output_image = self.model.predict(pil_img)
            
            # Convert PIL image back to OpenCV grayscale format
            output_cv = cv2.cvtColor(np.array(output_image), cv2.COLOR_RGB2GRAY)
            return output_cv
            
        except Exception as e:
            return image