import base64
import fitz
import io
import pytesseract
import openai
from PIL import Image
import concurrent.futures

# Set your OpenAI API key
openai.api_key = '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'


def extract_text_from_base64_pdf(base64_content):
    try:
        pdf_content = base64.b64decode(base64_content)
        pdf_document = fitz.open(stream=pdf_content)
        # Iterate through each page in the document
        text = ""
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
                text += image_text
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content



def process_pdfs_and_query_wrapper(pdf_file_paths):
    # Process PDFs and query OpenAI in a thread-safe manner
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = []
        for pdf_file_path in pdf_file_paths:
            # Read the PDF file and encode it to base64
            with open(pdf_file_path, "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read()).decode("utf-8")

            # Extract text from the base64-encoded PDF
            extracted_text = extract_text_from_base64_pdf(encoded_string)

            # Create a prompt using the extracted text
            prompt = f"""
                  print name ,date of birth and id card type in one json format from given 
                    data with the text delimited by triple backticks" \
                    ```{extracted_text}```
                """

            # Submit each file for processing in a separate thread
            future = executor.submit(get_completion, prompt)
            results.append(future)

        # Wait for all threads to complete and get their results
        final_results = [future.result() for future in concurrent.futures.as_completed(results)]

    return final_results
