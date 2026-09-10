import pymupdf

def extract_images_from_pdf(path:str)->list:
    image_frames = []
    try:
        doc = pymupdf.open(path)
        for page_number, page in enumerate(doc):
            images = page.get_images(full=True)
            for image_num, img in enumerate(images):
                xref = img[0]
                image = doc.extract_image(xref)
                image_bytes =  image["image"]
                image_frames.append(image_bytes)                
    except:
        pass
    return image_frames



