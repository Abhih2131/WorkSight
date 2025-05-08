def render(data_frames):
    import streamlit as st
    import pandas as pd
    import os
    from datetime import datetime
    from PIL import Image, ImageDraw, ImageOps
    import base64
    from io import BytesIO
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    import time

    def format_inr(val):
        try:
            return f"₹ {round(val / 100000, 2)} Lakhs"
        except:
            return "-"

    def format_date(val):
        try:
            return pd.to_datetime(val).strftime("%d-%b-%Y")
        except:
            return "-"

    def create_circular_image(path, size=(150, 150)):
        img = Image.open(path).convert("RGBA").resize(size)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output

    def get_circular_image_b64(empid):
        for ext in [".png", ".jpg", ".jpeg"]:
            path = f"data/images/{empid}{ext}"
            if os.path.exists(path):
                img = create_circular_image(path)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        return ""

    def export_html_to_pdf_using_headless(html_path, pdf_path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,1696")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # ✅ Headless Chrome with WebDriver Manager (No System Packages)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("file://" + os.path.abspath(html_path))
        time.sleep(2)

        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "preferCSSPageSize": True
        })

        with open(pdf_path, "wb") as f:
            f.write(base64.b64decode(result['data']))

        driver.quit()

    df = data_frames.get("employee", pd.DataFrame())
    if df.empty:
        st.warning("Employee data not available.")
        return

    today = pd.to_datetime("today")
    df["date_of_exit"] = pd.to_datetime(df["date_of_exit"], errors="coerce")
    df["date_of_joining"] = pd.to_datetime(df["date_of_joining"], errors="coerce")
    df_active = df[df["date_of_exit"].isna() | (df["date_of_exit"] > today)]

    st.markdown("### 🔍 Talent Profile Summary")
    emp_id = st.text_input("Enter Employee ID", key="pdf_input")

    if not emp_id:
        return

    try:
        emp_id = int(emp_id)
    except:
        st.error("Employee ID must be numeric.")
        return

    row = df_active[df_active["employee_id"] == emp_id]
    if row.empty:
        st.warning("No active employee found.")
        return

    emp = row.iloc[0]
    photo_b64 = get_circular_image_b64(emp["employee_id"])

    age = "-"
    tenure = "-"
    if pd.notna(emp["date_of_birth"]):
        age = int((today - emp["date_of_birth"]).days / 365.25)
        age = f"{age} yrs"
    if pd.notna(emp["date_of_joining"]):
        delta = today - emp["date_of_joining"]
        years = delta.days // 365
        months = (delta.days % 365) // 30
        tenure = f"{years} yrs {months} months" if years > 0 else f"{months} months"

    html = f"""
    <html><head><meta charset='utf-8'>
    <style>
    body {{ font-family: 'Segoe UI', sans-serif; font-size: 13px; margin: 20px; background: #f5f8fc; }}
    .profile-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0E2A47;
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
    }}
    .profile-info {{
        flex-grow: 1;
    }}
    .profile-info h2 {{
        margin: 0;
        font-size: 22px;
    }}
    .photo {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid white;
        object-fit: cover;
    }}
    </style></head><body>

    <div class="profile-header">
        <div class="profile-info">
            <h2>{emp['employee_name']}</h2>
            <div>Employee ID: <b>{emp['employee_id']}</b></div>
            <div>{emp['function']} | {emp['department']} | Band: {emp['band']} | Grade: {emp['grade']}</div>
            <div>Age: {age} | Tenure: {tenure}</div>
        </div>
        {f"<img src='{photo_b64}' class='photo'/>" if photo_b64 else ''}
    </div>
    </body></html>
    """

    st.components.v1.html(html, height=800, scrolling=True)

    os.makedirs("exports", exist_ok=True)
    html_path = os.path.join("exports", f"profile_{emp['employee_id']}.html")
    pdf_path = os.path.join("exports", f"profile_{emp['employee_id']}.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    export_html_to_pdf_using_headless(html_path, pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download as PDF", f, file_name=os.path.basename(pdf_path))
