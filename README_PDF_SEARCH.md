# Azure Cognitive Search - PDF Upload & Search

This script allows you to upload your PDF file to Azure Cognitive Search and search for specific phrases within it.

## 🚀 Quick Start

### Step 1: Install Additional Dependencies

```bash
pip install PyPDF2==3.0.1
```

Or install from the requirements file:
```bash
pip install -r requirements_pdf.txt
```

### Step 2: Place Your PDF File

Make sure your PDF file `NIES_English_FullStrategy.pdf` is in the same directory as the script:

```
azure-search-test/
├── .env
├── upload_and_search_pdf.py
├── NIES_English_FullStrategy.pdf  ← Your PDF here
└── requirements_pdf.txt
```

### Step 3: Run the Script

```bash
python upload_and_search_pdf.py
```

## 📋 What the Script Does

1. **Extracts text** from your PDF (all pages)
2. **Creates an index** in Azure Cognitive Search (if it doesn't exist)
3. **Uploads the PDF content** to the search index
4. **Enters interactive search mode** - you can search for any phrase!

## 🔍 Example Usage

After running the script, you'll see:

```
🔍 Search query: climate change

📋 Search Results:

Document: NIES_English_FullStrategy.pdf
Score: 2.45

Found 5 occurrence(s):

Occurrence 1:
   ...the impact of climate change on biodiversity and ecosystems...

Occurrence 2:
   ...strategies to mitigate climate change through sustainable practices...

🔍 Search query: environmental policy

...more results...

🔍 Search query: quit
👋 Goodbye!
```

## 💡 Search Tips

### Good Search Queries:
- Single words: `climate`, `policy`, `environment`
- Phrases: `climate change`, `sustainable development`, `environmental protection`
- Specific terms: `carbon emissions`, `biodiversity`, `renewable energy`

### The script will:
- Show you the search score (how relevant the result is)
- Display the context around where your phrase appears
- Show up to 3 occurrences of your search term
- Let you search multiple times in one session

## 🎯 Understanding Search Results

**Score**: Higher score = more relevant
- `2.0+` - Highly relevant
- `1.0-2.0` - Moderately relevant  
- `0.5-1.0` - Somewhat relevant

**Context**: Shows ~100 characters before and after your search term

## 📊 Azure Portal - Viewing Your Data

To see your uploaded document in Azure Portal:

1. Go to Azure Portal → **acs-1026hack-test**
2. Click **Search Explorer**
3. Select index: **pdf-documents-index**
4. Click **Search** to see all documents

## 🔧 Troubleshooting

### "PDF file not found"
- Make sure `NIES_English_FullStrategy.pdf` is in the same directory
- Check the filename is exactly correct

### "Module not found: PyPDF2"
```bash
pip install PyPDF2
```

### "No results found"
- The search is case-insensitive
- Try broader search terms
- Make sure the PDF was uploaded successfully (check for ✅ SUCCESS message)

## 🎨 Customization

### Search Different PDF
Change the filename in the script:
```python
PDF_FILE = "your_document.pdf"
```

### Change Index Name
```python
index_name = "my-custom-index"
```

### Get More Results
Change the `top` parameter:
```python
results = search_client.search(
    search_text=search_query,
    top=10  # Get top 10 results instead of 5
)
```

## 📝 Notes

- The script extracts text from **all pages** of the PDF
- Text extraction quality depends on the PDF (scanned images may not work well)
- The index is persistent - you only need to upload once
- You can upload multiple PDFs by running the script multiple times with different IDs

## 🔒 Security

- Your `.env` file contains your API key - never commit it to Git
- The `.gitignore` file protects your credentials
- All searches are logged in Azure (visible in Activity Log after ~15 minutes)

## 🎉 Next Steps

After testing with this PDF, you can:
1. Upload multiple PDFs by modifying the script
2. Build a web interface for searching
3. Integrate search into your hackathon project
4. Add more advanced features like filters, facets, or autocomplete

Good luck with your project! 🚀
