import io
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import os

count = 1


def extract_text(pdf_document, count):
    results_folder = "results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    output_text_file_path = os.path.join(results_folder, f"output_text-pdf{count}.txt")
    output_text_file = open(output_text_file_path, "w", encoding="utf-8")

    pdf_document = fitz.open(pdf_document)
    # Iterate through each page in the document
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        # Get the images on the page
        images = page.get_images(full=True)

        # Iterate through each image on the page
        for img_index, img_info in enumerate(images):
            img_index += 1  # Image index starts from 1
            image_index = img_info[0]
            base_image = pdf_document.extract_image(image_index)

            # Convert image bytes to a format that Tesseract can process
            image_bytes = base_image["image"]
            image_pil = Image.open(io.BytesIO(image_bytes))

            # Use pytesseract to extract text from the image
            image_text = pytesseract.image_to_string(image_pil)

            # Extract text content from the PDF page
            page_text = page.get_text()

            # Write the extracted text content to the text file
            output_text_file.write(f"Page {page_number + 1}, Image {img_index} Text:\n")
            if image_text:
                output_text_file.write(image_text + "\n")
                output_text_file.write("=" * 50 + "\n")
            if page_text:
                output_text_file.write("PDF Page Text:\n")
                output_text_file.write(page_text + "\n")
                output_text_file.write("=" * 50 + "\n\n")
    # Close the text file
    output_text_file.close()
