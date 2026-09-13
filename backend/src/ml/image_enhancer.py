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
                self.model = RealESRGAN(self.device, scale=4)
                
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
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.resize(gray, (720, 1280))
        
        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=10,
            templateWindowSize=7,
            searchWindowSize=21
        )
        return cv2.cvtColor(denoised,cv2.COLOR_GRAY2RGB)

    def enhance(self, image: np.ndarray) -> np.ndarray:
        try:
            if len(image.shape) == 2:
                pil_img = Image.fromarray(image).convert('RGB')
            else:
                pil_img = Image.fromarray(image)
                
            output_image = self.model.predict(pil_img)
            
            output_cv = np.array(output_image), cv2.COLOR_RGB2GRAY
            return output_cv
            
        except Exception as e:
            return image