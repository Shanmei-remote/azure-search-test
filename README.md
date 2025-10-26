# Azure Cognitive Search API Test

This is a comprehensive test suite to verify your Azure Cognitive Search API is working correctly.

## 📋 Prerequisites

- Python 3.7 or higher
- Azure Cognitive Search service created (acs-1026hack-test)
- Admin API key from Azure portal

## 🚀 Step-by-Step Setup Instructions

### Step 1: Get Your API Key from Azure Portal

1. Go to your Azure Portal: https://portal.azure.com
2. Navigate to your search service: **acs-1026hack-test**
3. In the left sidebar, click **Settings** → **Keys**
4. Copy your **Primary admin key** (it will be a long string)

### Step 2: Set Up Your Project Files

1. **Create a project folder:**
   ```bash
   mkdir azure-search-test
   cd azure-search-test
   ```

2. **Copy these files into your project folder:**
   - `test_azure_search.py` (the main test script)
   - `requirements.txt` (Python dependencies)
   - `.env.template` (environment variables template)

### Step 3: Create Your .env File

1. **Copy the template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit the .env file** and replace the placeholders:
   ```env
   AZURE_SEARCH_ENDPOINT=https://acs-1026hack-test.search.windows.net
   AZURE_SEARCH_API_KEY=paste_your_actual_key_here
   AZURE_SEARCH_INDEX_NAME=test-index
   ```

   **Important:** 
   - Replace `paste_your_actual_key_here` with the key you copied from Azure
   - Keep `test-index` as is (the script will create this index)

3. **Save the file**

### Step 4: Install Required Python Packages

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install azure-search-documents==11.4.0 python-dotenv==1.0.0
```

### Step 5: Run the Test

```bash
python test_azure_search.py
```

## 📊 What the Test Does

The test suite will run 5 tests in sequence:

1. **Connection Test** ✓
   - Verifies your credentials are correct
   - Checks if you can connect to Azure Cognitive Search
   - Lists any existing indexes

2. **Create Index Test** ✓
   - Creates a new search index called "test-index"
   - Defines a simple schema with fields: id, title, content, category

3. **Upload Documents Test** ✓
   - Uploads 3 sample documents to the index
   - Verifies the upload was successful

4. **Search Test** ✓
   - Performs a search query: "Azure search"
   - Displays search results with scores
   - Verifies search functionality works

5. **Cleanup (Optional)** ⚠️
   - Asks if you want to delete the test index
   - Type "yes" to clean up, or "no" to keep the index

## ✅ Expected Output

If everything works correctly, you should see:

```
============================================================
AZURE COGNITIVE SEARCH API TEST SUITE
============================================================

============================================================
TEST 1: Testing Connection to Azure Cognitive Search
============================================================
✓ Endpoint: https://acs-1026hack-test.search.windows.net
✓ Index Name: test-index
✓ API Key: ********************... (hidden)

✅ SUCCESS: Connected to Azure Cognitive Search!
   Found 0 existing index(es)

============================================================
TEST 2: Creating Test Index
============================================================
   Index 'test-index' does not exist. Creating new index...
✅ SUCCESS: Index 'test-index' created!
   Fields: 4

============================================================
TEST 3: Uploading Test Documents
============================================================
✅ SUCCESS: Uploaded 3/3 documents!
   ✓ Document 1: 1
   ✓ Document 2: 2
   ✓ Document 3: 3

   Waiting 3 seconds for indexing to complete...

============================================================
TEST 4: Searching Documents
============================================================
   Search query: 'Azure search'

   Search results:

   Result 1:
   - ID: 1
   - Title: Azure Cognitive Search Introduction
   - Category: Documentation
   - Score: 2.15

   Result 2:
   - ID: 2
   - Title: Getting Started with Search
   - Category: Tutorial
   - Score: 1.82

✅ SUCCESS: Found 2 result(s)!

============================================================
TEST 5: Cleanup (Optional)
============================================================

Do you want to delete the test index? (yes/no): yes
✅ SUCCESS: Index 'test-index' deleted!

============================================================
TEST SUMMARY
============================================================
✅ PASSED: Connection
✅ PASSED: Create Index
✅ PASSED: Upload Documents
✅ PASSED: Search Documents
✅ PASSED: Cleanup

============================================================
RESULT: 5/5 tests passed
============================================================
```

## 🐛 Troubleshooting

### Error: "Missing environment variables"
- Make sure your `.env` file exists in the same directory
- Check that all three variables are set correctly

### Error: "Authentication failed"
- Verify your API key is correct (no extra spaces)
- Make sure you copied the **Primary admin key**, not a query key

### Error: "Connection timeout"
- Check your internet connection
- Verify the endpoint URL is correct

### Error: "Index already exists"
- This is normal if you ran the test before
- The script will use the existing index
- Choose "yes" for cleanup to remove it

## 📁 Project Structure

```
azure-search-test/
├── test_azure_search.py   # Main test script
├── requirements.txt        # Python dependencies
├── .env                    # Your credentials (DO NOT COMMIT!)
└── README.md              # This file
```

## 🔒 Security Notes

- **Never commit your `.env` file to version control!**
- Add `.env` to your `.gitignore` file:
  ```bash
  echo ".env" >> .gitignore
  ```
- Keep your API keys secure and rotate them regularly

## 📚 Next Steps

After the test passes successfully, you can:

1. **Keep the test index** to experiment with queries
2. **Create a production index** with your actual data schema
3. **Integrate search** into your application
4. **Explore advanced features** like:
   - Faceted navigation
   - Autocomplete/suggestions
   - Scoring profiles
   - Semantic search

## 📖 Additional Resources

- [Azure Cognitive Search Documentation](https://docs.microsoft.com/en-us/azure/search/)
- [Python SDK Reference](https://docs.microsoft.com/en-us/python/api/overview/azure/search-documents-readme)
- [REST API Reference](https://docs.microsoft.com/en-us/rest/api/searchservice/)

## ❓ Questions?

If you encounter any issues:
1. Check the error message carefully
2. Review the troubleshooting section
3. Verify your credentials in the Azure Portal
4. Make sure all dependencies are installed

Good luck with your hackathon! 🚀
