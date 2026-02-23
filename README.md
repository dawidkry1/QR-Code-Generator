# QR Code Generator for URLs

A Python and Streamlit app to generate QR codes for multiple URLs quickly.  
Perfect for sharing web apps, dashboards, or any online resources with colleagues or mobile devices.

## Features

- Generate QR codes from a list of URLs
- Display QR codes in a Streamlit dashboard for easy scanning
- Save QR codes locally as PNG files
- Customizable QR code size and colors
- Supports multiple apps / websites at once

## Usage

1. Update the `urls` dictionary below with your desired URLs:

urls = {
    "App 1": "https://example.com/app1",
    "App 2": "https://example.com/app2",
    "GitHub Repo": "https://github.com/username/repo"
}

2. Run the Streamlit app:

    pip install streamlit qrcode[pil] pillow
    streamlit run app.py

3. Scan the QR codes displayed on the dashboard to open the URLs on your phone or tablet.

4. PNG files of each QR code will also be saved locally for printing or sharing.

## Requirements

- Python 3.x
- Streamlit
- qrcode
- Pillow


## License

MIT License

Copyright (c) 2026 dawidkry
