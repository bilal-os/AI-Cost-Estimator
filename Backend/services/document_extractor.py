import os
import PyPDF2
import docx
import mammoth  # Better alternative for .docx files

def extract_text_from_document(document):
    """
    Extract text from various document types
    
    :param document: File object from Flask request
    :return: Extracted text as string
    """
    try:
        # Get original filename
        filename = document.filename.lower()
        
        # Temporarily save the uploaded file
        temp_path = os.path.join('/tmp', filename)
        document.save(temp_path)
        
        # Extract text based on file extension
        if filename.endswith('.pdf'):
            with open(temp_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ' '.join([page.extract_text() for page in reader.pages])
        
        elif filename.endswith('.docx'):
            with open(temp_path, 'rb') as file:
                result = mammoth.extract_text(file)
                text = result.value
        
        elif filename.endswith('.txt'):
            with open(temp_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        else:
            # Fallback for unknown file types
            text = "Unsupported file type"
        
        # Remove temporary file
        os.unlink(temp_path)
        
        return text
    
    except Exception as e:
        print(f"Error extracting document text: {str(e)}")
        return ""