# npm install -g lighthouse

import shutil
import subprocess
import os

# List of URLs to test
urls = [
    "https://almoapi.com/",
    "https://almoapi.com/faq",
    "https://almoapi.com/privacy-policy",
    "https://almoapi.com/aboutus",
    "https://almoapi.com/contactus",
    "https://almoapi.com/login",
    "https://almoapi.com/register",
]

# Output directory for reports
output_dir = "lighthouse_reports"
os.makedirs(output_dir, exist_ok=True)

# Lighthouse CLI options
chrome_flags = "--headless"
format = "html"

for url in urls:
    # Safe filename
    safe_url = url.replace("https://", "").replace("/", "_")
    output_path = os.path.join(output_dir, f"{safe_url}.html")

    print(f"Running Lighthouse for: {url}")
    cmd = [
        shutil.which("lighthouse"), 
        url,
        f"--chrome-flags={chrome_flags}",
        f"--output={format}",
        f"--output-path={output_path}"
    ]

    print("Running command:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Report saved to: {output_path}")
