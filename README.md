
# Vendor Intelligence Portal — # VendorIQ

A modern and interactive **Vendor Intelligence Dashboard** built using **Streamlit**, designed to analyze vendor performance, materials supplied, pricing trends, and purchase order insights. This portal supports CSV uploads, data cleaning, visual analytics, and real-time vendor intelligence with a futuristic UI theme.

---

## 🚀 Features

### Dashboard Highlights

* Upload your **Vendor / Purchase Order CSV**
* Automatic data cleaning
* Rich UI with custom CSS theme
* Interactive charts powered by Plotly
* Vendor-wise analytics
* Material pricing overview
* Purchase order insights
* Smart KPI cards (Spend, Vendor Count, Material Count, etc.)

### Visual Analytics

* Spend distribution by vendor
* Item-wise and material-wise cost breakdown
* Rate comparison charts
* Trend analysis
* Summary metrics

### Data Handling

* Cleans numeric and text fields
* Supports large datasets
* Provides downloadable **template CSV**
* Ensures consistent column formats

### UI / UX

* Dark gradient theme
* Custom-styled sidebar
* Animated badges
* Responsive card layout
* Neon glow effects

---

## 🛠 Installation

Ensure you have Python 3.8+ installed.

```bash
pip install streamlit pandas plotly openpyxl
```

---

## ▶️ How to Run

Save your file as `vendor_portal.py`, then run:

```bash
streamlit run vendor_portal.py
```

The portal will open at:

```
http://localhost:8501
```

---

## 📂 CSV Template Format

Your CSV must contain these columns:

```
PO Dt, PO No, Supplier, Item, HSN No, Item Description,
Indent Dt, Indent No, UOM, Quantity, Rate,
Material, Excise, Discount, Tax, Freight, Others, Net
```

A downloadable template CSV is available inside the application.

---

## 🧩 Core Functions

### Data Cleaning

* Converts blank, NaN, None → clean text
* Converts numeric fields into float
* Removes formatting issues

### File Upload Support

* Accepts `.csv` and `.xlsx`
* Converts into DataFrame
* Sample dataset loaded via caching

### Chart Engine

* Dark mode plotly layout
* INR formatting (Lakhs, Crores, Thousands)
* Custom axis formatters

### UI CSS

* Sidebar branding
* KPI glow effects
* Vendor cards
* Empty state screens
* Smooth gradients and styling

---

## 📁 Recommended Project Structure

```
📦 Vendor-Intelligence-Portal
 ┣ 📜 vendor_portal.py
 ┣ 📜 README.md
 ┣ 📁 data/
 ┃   ┗ sample_vendor_data.csv
 ┗ 📁 assets/
     ┗ styles.css
```

---

## 💡 Future Enhancements

* Vendor performance score system
* Predictive pricing models
* Material consumption forecasting
* ERP or Google Sheets API integration
* Role-based authentication

---

## 📝 Author

Vendor Intelligence Portal — Built using **Streamlit**, **Pandas**, and **Plotly**, styled with custom CSS.

---
