from transformers import TrOCRProcessor, VisionEncoderDecoderModel


PROCESSOR_PRINTED = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
OCR_MODEL_PRINTED = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')

PROCESSOR_HANDWRITTEN = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
OCR_MODEL_HANDWRITTEN = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

def ocr_image_printed(image):
    pixel_values = PROCESSOR_PRINTED(images=image, return_tensors="pt").pixel_values
    generated_ids = OCR_MODEL_PRINTED.generate(pixel_values)
    generated_text = PROCESSOR_PRINTED.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return int(generated_text.replace(' ', ''))

def ocr_image_handwritten(image):
    pixel_values = PROCESSOR_HANDWRITTEN(images=image, return_tensors="pt").pixel_values
    generated_ids = OCR_MODEL_HANDWRITTEN.generate(pixel_values)
    generated_text = PROCESSOR_HANDWRITTEN.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text