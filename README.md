# 📁 Mediafire Bulk Downloader

Download entire Mediafire folders without a premium account — using web scraping and automated downloading.

> Mediafire doesn't offer a native way to download uncompressed folders for free. This toolset solves that by scraping all file links from a folder URL and downloading them locally while preserving the original directory structure.

---

## 🛠️ How It Works

The workflow is split into three scripts that run in sequence:

```
mediafire_scraper.py  →  downloader_requests.py  →  downloader_selenium.py (fallback)
```

### 1. `mediafire_scraper.py` — Link Scraper
Set your target folder URL in the script:
```python
START_URL = "YOUR_FOLDER_URL_HERE"
```
The scraper recursively traverses all subfolders, collects every file's download link, and preserves the original path structure.

**Output:** `mediafire_links.csv`

---

### 2. `downloader_requests.py` — Fast Downloader
Reads `mediafire_links.csv` and downloads all files using HTTP requests, recreating the original folder structure locally.

Mediafire may block some automated requests. Files that fail to download are logged separately.

**Output:** downloaded files + `errors.csv` (failed downloads)

---

### 3. `downloader_selenium.py` — Fallback Downloader
Reads `errors.csv` and retries the failed downloads using a browser-based approach via Selenium. Slower, but significantly more reliable for files that were blocked.

---

## ✅ Requirements

- Python 3.x
- Google Chrome installed
- Python dependencies (install with the command below)

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/dlmeneguin/Mediafire_bulk_download.git
   cd Mediafire_bulk_download
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open `mediafire_scraper.py` and set your folder URL:
   ```python
   START_URL = "https://www.mediafire.com/folder/your-folder-id"
   ```

4. Run the scraper:
   ```bash
   python mediafire_scraper.py
   ```

5. Download files:
   ```bash
   python downloader_requests.py
   ```

6. If any files failed, run the Selenium fallback:
   ```bash
   python downloader_selenium.py
   ```

---

## 📂 Output Structure

```
your-folder/
├── subfolder-a/
│   ├── file1.ext
│   └── file2.ext
└── subfolder-b/
    └── file3.ext

mediafire_links.csv   ← all scraped links
errors.csv            ← files that failed in step 2
```

---

## ⚠️ Notes

- This tool is intended for downloading content you have legitimate access to.
- Mediafire's anti-bot measures may cause some downloads to fail on the first pass — the Selenium fallback handles those cases.
- ChromeDriver is managed automatically; just make sure Chrome is installed.

---

## 📄 License

MIT
