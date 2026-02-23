"""
📱 QR Code Generator Pro – Fully Responsive with Multi-Removal

Features:
- Dynamic QR generator at the top
- Predefined app QR codes from JSON
- Grid layout adjusts columns automatically
- Download buttons for all QR codes
- QR color customization
- Add new URLs directly via a Streamlit form
- Remove one or multiple URLs with confirmation
- Clear all apps with confirmation
"""

import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import os
import json
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="QR Code Generator Pro", page_icon="📱", layout="wide")
st.title("📱 QR Code Generator Pro Dashboard")

# --- HELPER FUNCTION TO CREATE QR IMAGE ---
def generate_qr_image(url: str, fill_color="black", back_color="white") -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
    return img

# --- DYNAMIC QR GENERATOR ---
st.header("🔹 Generate a QR Code for Any URL")
user_url = st.text_input("Enter a URL here:")

# Optional color customization
st.subheader("QR Code Colors")
col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("Fill Color", "#000000")
with col2:
    back_color = st.color_picker("Background Color", "#ffffff")

if user_url:
    pil_user = generate_qr_image(user_url, fill_color, back_color)
    buf = BytesIO()
    pil_user.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(byte_im, caption=f"QR Code for {user_url}", use_column_width=False)
    st.markdown(f"[🔗 Click to open URL]({user_url})")
    st.download_button(
        label="💾 Download QR Code",
        data=byte_im,
        file_name="dynamic_QR.png",
        mime="image/png"
    )

st.divider()
st.markdown("### Predefined App QR Codes")

# --- CREATE FOLDER FOR SAVED QR CODES ---
save_folder = "qr_codes"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# --- LOAD PREDEFINED APPS FROM JSON ---
json_file = "apps_config.json"
if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump({}, f)

with open(json_file) as f:
    apps = json.load(f)

# --- FORM TO ADD NEW URL ---
st.subheader("➕ Add New App/URL")
with st.form("add_url_form", clear_on_submit=True):
    new_name = st.text_input("App Name")
    new_url = st.text_input("App URL")
    submit = st.form_submit_button("Add App")
    if submit and new_name and new_url:
        apps[new_name] = new_url
        with open(json_file, "w") as f:
            json.dump(apps, f, indent=4)
        st.success(f"Added {new_name}!")
        st.experimental_rerun()  # Refresh app to show new QR code

# --- FORM TO REMOVE APPS ---
if apps:
    st.subheader("🗑 Remove App(s)/URL(s)")

    with st.form("remove_url_form"):
        selected_remove = st.multiselect(
            "Select app(s) to remove",
            options=list(apps.keys())
        )
        confirm_remove = st.checkbox("Confirm removal of selected app(s)")
        submit_remove = st.form_submit_button("Remove Selected")
        if submit_remove:
            if confirm_remove and selected_remove:
                for app_name in selected_remove:
                    apps.pop(app_name)
                with open(json_file, "w") as f:
                    json.dump(apps, f, indent=4)
                st.success(f"Removed: {', '.join(selected_remove)}")
                st.experimental_rerun()
            elif not confirm_remove:
                st.warning("Please check the confirmation box before removing.")
            elif not selected_remove:
                st.warning("No apps selected for removal.")

    # Optional: Clear all apps
    with st.form("clear_all_form"):
        confirm_clear = st.checkbox("Confirm clearing all apps")
        submit_clear = st.form_submit_button("Clear All Apps")
        if submit_clear:
            if confirm_clear:
                apps.clear()
                with open(json_file, "w") as f:
                    json.dump(apps, f, indent=4)
                st.success("All apps cleared!")
                st.experimental_rerun()
            else:
                st.warning("Please check the confirmation box before clearing all apps.")

# --- RESPONSIVE GRID DISPLAY ---
total_apps = len(apps)
if total_apps == 0:
    st.info("No apps available.")
else:
    cols_per_row = min(max(math.ceil(total_apps / 2), 1), 4)
    cols = st.columns(cols_per_row)

    for i, (name, url) in enumerate(apps.items()):
        pil_img = generate_qr_image(url)
        filename = os.path.join(save_folder, f"{name.replace(' ', '_')}_QR.png")
        pil_img.save(filename)

        buf = BytesIO()
        pil_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        col = cols[i % cols_per_row]
        with col:
            st.markdown(f"**{name}**")
            st.image(byte_im, caption=f"Scan to open {name}", use_column_width=True)
            st.markdown(f"[🔗 Open {name}]({url})")
            st.download_button(
                label="💾 Download QR Code",
                data=byte_im,
                file_name=f"{name.replace(' ', '_')}_QR.png",
                mime="image/png"
            )

        if (i + 1) % cols_per_row == 0:
            cols = st.columns(cols_per_row)
