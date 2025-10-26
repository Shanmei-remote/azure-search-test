"""
Azure Cognitive Search API Test Script
This script tests your Azure Cognitive Search connection and basic operations
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

# Load environment variables
load_dotenv()

# Get credentials from .env file
endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
api_key = os.getenv('AZURE_SEARCH_API_KEY')
index_name = os.getenv('AZURE_SEARCH_INDEX_NAME')

def test_connection():
    """Test 1: Check if we can connect to Azure Cognitive Search"""
    print("\n" + "="*60)
    print("TEST 1: Testing Connection to Azure Cognitive Search")
    print("="*60)
    
    try:
        # Check if environment variables are loaded
        if not endpoint or not api_key or not index_name:
            print("❌ FAILED: Missing environment variables!")
            print(f"   Endpoint: {'✓' if endpoint else '✗ Missing'}")
            print(f"   API Key: {'✓' if api_key else '✗ Missing'}")
            print(f"   Index Name: {'✓' if index_name else '✗ Missing'}")
            return False
        
        print(f"✓ Endpoint: {endpoint}")
        print(f"✓ Index Name: {index_name}")
        print(f"✓ API Key: {'*' * 20}... (hidden)")
        
        # Create a credential object
        credential = AzureKeyCredential(api_key)
        
        # Create index client
        index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
        
        # Try to list indexes (this tests the connection)
        indexes = list(index_client.list_indexes())
        
        print(f"\n✅ SUCCESS: Connected to Azure Cognitive Search!")
        print(f"   Found {len(indexes)} existing index(es)")
        
        if indexes:
            print("\n   Existing indexes:")
            for idx in indexes:
                print(f"   - {idx.name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: Connection error!")
        print(f"   Error: {str(e)}")
        return False


def create_test_index():
    """Test 2: Create a simple test index"""
    print("\n" + "="*60)
    print("TEST 2: Creating Test Index")
    print("="*60)
    
    try:
        credential = AzureKeyCredential(api_key)
        index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
        
        # Check if index already exists
        try:
            existing_index = index_client.get_index(index_name)
            print(f"ℹ️  Index '{index_name}' already exists!")
            print(f"   Created: {existing_index.name}")
            return True
        except:
            print(f"   Index '{index_name}' does not exist. Creating new index...")
        
        # Define a simple index schema
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SimpleField(name="category", type=SearchFieldDataType.String, filterable=True)
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


def upload_test_documents():
    """Test 3: Upload sample documents to the index"""
    print("\n" + "="*60)
    print("TEST 3: Uploading Test Documents")
    print("="*60)
    
    try:
        credential = AzureKeyCredential(api_key)
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Sample documents
        documents = [
            {
                "id": "1",
                "title": "Azure Cognitive Search Introduction",
                "content": "Azure Cognitive Search is a cloud search service with built-in AI capabilities.",
                "category": "Documentation"
            },
            {
                "id": "2",
                "title": "Getting Started with Search",
                "content": "Learn how to create your first search index and query documents.",
                "category": "Tutorial"
            },
            {
                "id": "3",
                "title": "Advanced Search Features",
                "content": "Explore faceted navigation, filters, and scoring profiles.",
                "category": "Advanced"
            }
        ]
        
        # Upload documents
        result = search_client.upload_documents(documents=documents)
        
        successful = sum(1 for r in result if r.succeeded)
        print(f"✅ SUCCESS: Uploaded {successful}/{len(documents)} documents!")
        
        for i, res in enumerate(result):
            status = "✓" if res.succeeded else "✗"
            print(f"   {status} Document {i+1}: {res.key}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Could not upload documents!")
        print(f"   Error: {str(e)}")
        return False


def search_test_documents():
    """Test 4: Search the uploaded documents"""
    print("\n" + "="*60)
    print("TEST 4: Searching Documents")
    print("="*60)
    
    try:
        credential = AzureKeyCredential(api_key)
        search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Perform a search
        search_text = "Azure search"
        print(f"   Search query: '{search_text}'")
        
        results = search_client.search(search_text=search_text)
        
        count = 0
        print("\n   Search results:")
        for result in results:
            count += 1
            print(f"\n   Result {count}:")
            print(f"   - ID: {result['id']}")
            print(f"   - Title: {result['title']}")
            print(f"   - Category: {result['category']}")
            print(f"   - Score: {result['@search.score']:.2f}")
        
        if count > 0:
            print(f"\n✅ SUCCESS: Found {count} result(s)!")
            return True
        else:
            print("\n⚠️  WARNING: Search completed but no results found.")
            return True
        
    except Exception as e:
        print(f"❌ FAILED: Could not search documents!")
        print(f"   Error: {str(e)}")
        return False


def cleanup_test_index():
    """Test 5: Optional cleanup - delete the test index"""
    print("\n" + "="*60)
    print("TEST 5: Cleanup (Optional)")
    print("="*60)
    
    response = input("\nDo you want to delete the test index? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("   Skipping cleanup. Index will remain.")
        return True
    
    try:
        credential = AzureKeyCredential(api_key)
        index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
        
        index_client.delete_index(index_name)
        print(f"✅ SUCCESS: Index '{index_name}' deleted!")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Could not delete index!")
        print(f"   Error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("AZURE COGNITIVE SEARCH API TEST SUITE")
    print("="*60)
    
    results = {
        "Connection": False,
        "Create Index": False,
        "Upload Documents": False,
        "Search Documents": False,
        "Cleanup": True  # Optional, so True by default
    }
    
    # Run tests
    results["Connection"] = test_connection()
    
    if results["Connection"]:
        results["Create Index"] = create_test_index()
        
        if results["Create Index"]:
            results["Upload Documents"] = upload_test_documents()
            
            if results["Upload Documents"]:
                # Wait a moment for indexing to complete
                import time
                print("\n   Waiting 3 seconds for indexing to complete...")
                time.sleep(3)
                
                results["Search Documents"] = search_test_documents()
                
                if results["Search Documents"]:
                    results["Cleanup"] = cleanup_test_index()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print("\n" + "="*60)
    print(f"RESULT: {total_passed}/{total_tests} tests passed")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
