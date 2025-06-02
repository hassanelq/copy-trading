import os
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Helper function to wait until a new CSV appears and is fully downloaded
def wait_for_new_csv(download_dir, before_files, timeout=30, poll_interval=0.5):
    """
    After clicking “Export,” call this with a snapshot of files already in download_dir.
    Polls until a new .csv file is present and no .crdownload temp file remains.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        current_files = set(os.listdir(download_dir))
        new_candidates = [
            f
            for f in current_files
            if f not in before_files and f.lower().endswith(".csv")
        ]
        if new_candidates:
            # Ensure it’s not still being written (no .crdownload)
            if not any(f.lower().endswith(".crdownload") for f in current_files):
                return new_candidates[0]
        time.sleep(poll_interval)
    raise TimeoutError(f"No new CSV appeared in {timeout} seconds.")


# ─── Setup ───
DOWNLOAD_DIR = os.path.abspath("results")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Point to your preferred Chrome binary (stable or Dev). Adjust path if needed.
CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome Dev\Application\chrome.exe"

options = uc.ChromeOptions()
options.binary_location = CHROME_BINARY_PATH
options.headless = False
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True,
}
options.add_experimental_option("prefs", prefs)

# If using Chrome Dev v139, you can explicitly request a matching driver:
driver = uc.Chrome(version_main=139, options=options)

# Base URL for scraping pages
base_url = (
    "https://arbiscan.io/advanced-filter?"
    "tadd=0x2Df1c51E09aECF9cacB7bc98cB1742757f163dF7&"
    "amt=100000~999999999&ps=100&p="
)

# ─── Start scraping ───
try:
    for page in range(1, 455):
        print(f"Processing page {page}...")
        driver.get(base_url + str(page))

        try:
            wait = WebDriverWait(driver, 15)
            download_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "btnExportQuickTableToCSV"))
            )

            # Snapshot of files before clicking
            before = set(os.listdir(DOWNLOAD_DIR))

            # Click the export button
            download_btn.click()
            print(f"→ Clicked Export on page {page}, waiting for CSV...")

            # Wait until a new CSV appears
            try:
                new_file = wait_for_new_csv(DOWNLOAD_DIR, before, timeout=30)
                print(f"✅ Download complete: {new_file}")
            except TimeoutError as e:
                print(f"❌ Timeout on page {page}: {e}")
                screenshot = os.path.join(DOWNLOAD_DIR, f"timeout_page_{page}.png")
                driver.save_screenshot(screenshot)
                print(f"Screenshot saved at {screenshot}")
                continue

        except Exception:
            screenshot = os.path.join(DOWNLOAD_DIR, f"debug_page_{page}.png")
            driver.save_screenshot(screenshot)
            print(
                f"❌ Page {page} - Button not found. Screenshot saved at {screenshot}"
            )
            continue

finally:
    driver.quit()

# ─── Merge downloaded CSVs ───
print("📁 All downloads complete. Merging CSVs...")
csv_files = sorted(f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".csv"))
dataframes = []

for file in csv_files:
    path = os.path.join(DOWNLOAD_DIR, file)
    try:
        df = pd.read_csv(path)
        dataframes.append(df)
    except Exception:
        print(f"⚠️ Skipped unreadable file: {file}")

if dataframes:
    merged = pd.concat(dataframes, ignore_index=True)
    merged.to_csv("merged_output.csv", index=False)
    print("✅ Merged file saved: merged_output.csv")
else:
    print("❌ No valid CSVs to merge.")
