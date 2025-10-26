"""
Azure Cognitive Search - PDF Upload and Search Script
This script extracts text from a PDF and uploads it to Azure Cognitive Search for searching
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
import PyPDF2

# Load environment variables
load_dotenv()

# Get credentials from .env file
endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
api_key = os.getenv('AZURE_SEARCH_API_KEY')
index_name = "pdf-documents-index"  # New index for PDF documents

# Path to your PDF file
PDF_FILE = "NIES_English_FullStrategy.pdf"


def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF file"""
    print(f"\n📄 Extracting text from {pdf_path}...")
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            print(f"   Found {total_pages} pages")
            
            # Extract text from all pages
            full_text = ""
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += f"\n--- Page {page_num + 1} ---\n{text}"
            
            print(f"✅ Extracted {len(full_text)} characters")
            return full_text, total_pages
            
    except Exception as e:
        print(f"❌ Error extracting PDF: {str(e)}")
        return None, 0


def create_pdf_index():
    """Create a search index for PDF documents"""
    print("\n" + "="*60)
    print("Creating PDF Documents Index")
    print("="*60)
    
    try:
        credential = AzureKeyCredential(api_key)
        index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
        
        # Check if index already exists
        try:
            existing_index = index_client.get_index(index_name)
            print(f"ℹ️  Index '{index_name}' already exists!")
            print(f"   Using existing index: {existing_index.name}")
            return True
        except:
            print(f"   Creating new index '{index_name}'...")
        
        # Define index schema for PDF documents
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="filename", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
            SimpleField(name="page_count", type=SearchFieldDataType.Int32),
            SimpleField(name="upload_date", type=SearchFieldDataType.String)
        ]
        
        # Create the index
        index = SearchIndex(name=index_name, fields=fields)
        result = index_client.create_index(index)
        
        print(f"✅ SUCCESS: Index '{result.name}' created!")
        print(f"   Fields: {len(fields)}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Could not create index!")
        print(f"   Error: {str(e)}")
        return False


def upload_pdf_to_search(pdf_path):
    """Upload PDF content to Azure Cognitive Search"""
    print("\n" + "="*60)
    print("Uploading PDF to Azure Cognitive Search")
    print("="*60)
    
    try:
        # Extract text from PDF
        content, page_count = extract_text_from_pdf(pdf_path)
        
        if not content:
            return False
        
        # Create search client
        credential = AzureKeyCredential(api_key)
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Prepare document
        from datetime import datetime
        document = {
            "id": "1",
            "filename": os.path.basename(pdf_path),
            "content": content,
            "page_count": page_count,
            "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"\n📤 Uploading document...")
        print(f"   Filename: {document['filename']}")
        print(f"   Pages: {document['page_count']}")
        print(f"   Content length: {len(content)} characters")
        
        # Upload document
        result = search_client.upload_documents(documents=[document])
        
        if result[0].succeeded:
            print(f"✅ SUCCESS: PDF uploaded to Azure Cognitive Search!")
            return True
        else:
            print(f"❌ FAILED: Upload failed")
            return False
        
    except Exception as e:
        print(f"❌ FAILED: Could not upload PDF!")
        print(f"   Error: {str(e)}")
        return False


def search_pdf_content(search_query):
    """Search for specific phrases in the PDF"""
    print("\n" + "="*60)
    print(f"Searching for: '{search_query}'")
    print("="*60)
    
    try:
        credential = AzureKeyCredential(api_key)
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Perform search
        results = search_client.search(
            search_text=search_query,
            select=["filename", "content"],
            top=5  # Get top 5 results
        )
        
        print("\n📋 Search Results:\n")
        
        found_results = False
        for result in results:
            found_results = True
            print(f"Document: {result['filename']}")
            print(f"Score: {result['@search.score']:.2f}")
            
            # Find and display context around the search term
            content = result['content']
            search_lower = search_query.lower()
            content_lower = content.lower()
            
            # Find all occurrences
            positions = []
            start = 0
            while True:
                pos = content_lower.find(search_lower, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if positions:
                print(f"\nFound {len(positions)} occurrence(s):\n")
                
                for i, pos in enumerate(positions[:3], 1):  # Show first 3 occurrences
                    # Get context (100 chars before and after)
                    start_pos = max(0, pos - 100)
                    end_pos = min(len(content), pos + len(search_query) + 100)
                    context = content[start_pos:end_pos]
                    
                    # Clean up the context
                    context = ' '.join(context.split())
                    
                    print(f"Occurrence {i}:")
                    print(f"   ...{context}...")
                    print()
            
            print("-" * 60 + "\n")
        
        if not found_results:
            print("⚠️  No results found for your search query.")
            print("   Try different search terms or phrases.")
        else:
            print("✅ Search completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Could not search!")
        print(f"   Error: {str(e)}")
        return False


def interactive_search():
    """Interactive search mode - keep searching until user quits"""
    print("\n" + "="*60)
    print("Interactive Search Mode")
    print("="*60)
    print("\nEnter search phrases (or 'quit' to exit)")
    
    while True:
        query = input("\n🔍 Search query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not query:
            print("⚠️  Please enter a search query")
            continue
        
        search_pdf_content(query)


def main():
    """Main function to run the PDF upload and search"""
    print("\n" + "="*60)
    print("AZURE COGNITIVE SEARCH - PDF UPLOAD & SEARCH")
    print("="*60)
    
    # Check if PDF exists
    if not os.path.exists(PDF_FILE):
        print(f"❌ ERROR: PDF file not found: {PDF_FILE}")
        print("   Please make sure the PDF file is in the same directory as this script.")
        return
    
    # Step 1: Create index
    if not create_pdf_index():
        print("\n❌ Failed to create index. Exiting.")
        return
    
    # Step 2: Upload PDF
    print("\n⏳ Waiting 2 seconds...")
    import time
    time.sleep(2)
    
    if not upload_pdf_to_search(PDF_FILE):
        print("\n❌ Failed to upload PDF. Exiting.")
        return
    
    # Wait for indexing to complete
    print("\n⏳ Waiting 5 seconds for indexing to complete...")
    time.sleep(5)
    
    # Step 3: Interactive search
    interactive_search()


if __name__ == "__main__":
    main()
