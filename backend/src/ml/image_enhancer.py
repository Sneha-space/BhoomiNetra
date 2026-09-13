import cv2
import numpy as np


class CVProcessor:
    def process(self,images:list[np.ndarray])->list[np.ndarray]:
        image_list = []
        for image in images:
            image = self.preprocess(image)
            image = self.enhance(image)
            image_list.append(image)
        return image_list
    def process_bytes(self, list_image_bytes: bytes) -> list[np.ndarray]:
        images = []
        for image_bytes in list_image_bytes:
            image = np.frombuffer(image_bytes, dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Invalid image bytes")
            images.append(image)
        return images

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(1948,2752))
        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=10,
            templateWindowSize=7,
            searchWindowSize=21
        )

        return cv2.cvtColor(denoised,cv2.COLOR_GRAY2RGB)

    def enhance(self, image: np.ndarray) -> np.ndarray:
        return image