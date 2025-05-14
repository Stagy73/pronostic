
import subprocess
import sys
import os

def run_script(name):
    try:
        print(f"🚀 Running: {name}")
        subprocess.run([sys.executable, name], check=True)
        print(f"✅ Finished: {name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists("turfoo_scraper.py"):
        print("❌ turfoo_scraper.py not found")
        sys.exit(1)
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        sys.exit(1)

    run_script("turfoo_scraper.py")
    run_script("main.py")
    print("📄 Fichier JSON existe :", os.path.exists("turfoo_data.json"))

