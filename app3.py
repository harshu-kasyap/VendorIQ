"""
╔══════════════════════════════════════════════════════════════╗
║         VENDOR INTELLIGENCE PORTAL  ─  Streamlit App         ║
║                                                              ║
║  INSTALL:  pip install streamlit pandas plotly openpyxl      ║
║  RUN:      streamlit run vendor_portal.py                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import io
import traceback
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG  — must be first Streamlit call
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Vendor Intelligence Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  CUSTOM CSS  — broad selectors that survive Streamlit updates
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp,
.stApp > div,
section.main,
section.main > div,
.block-container { background-color: #080e1e !important; }

html, body, .stApp, p, span, div, label, input, button {
    font-family: 'DM Sans', sans-serif !important;
    color: #dde6f5;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; visibility: hidden !important; }

.block-container {
    padding: 1rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1528 0%, #090f1e 100%) !important;
    border-right: 1px solid rgba(56,189,248,0.12) !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8 !important;
    font-size: 12px !important;
}

input[type="text"], .stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 10px !important;
    color: #dde6f5 !important;
    font-size: 13px !important;
    padding: 8px 14px !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: rgba(56,189,248,0.6) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;
    outline: none !important;
}
input::placeholder { color: #475569 !important; }

.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #dde6f5 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(56,189,248,0.1) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-radius: 8px 8px 0 0 !important;
    color: #64748b !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: all 0.18s !important;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    background: rgba(56,189,248,0.07) !important;
    border-bottom: 2px solid #38bdf8 !important;
}

.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(56,189,248,0.3) !important;
    color: #7dd3fc !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 12px !important;
    transition: all 0.18s ease !important;
    padding: 0.4rem 1rem !important;
}
.stButton > button:hover {
    background: rgba(56,189,248,0.12) !important;
    border-color: rgba(56,189,248,0.55) !important;
    color: #38bdf8 !important;
    transform: translateY(-1px) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] {
    background: rgba(56,189,248,0.03) !important;
    border: 2px dashed rgba(56,189,248,0.25) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(56,189,248,0.14) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080e1e; }
::-webkit-scrollbar-thumb { background: rgba(56,189,248,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.45); }

.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #dde6f5 !important; }
.stMarkdown p, .stMarkdown li { color: #94a3b8 !important; }
.stMarkdown strong { color: #dde6f5 !important; }

/* ═══ CUSTOM HTML COMPONENTS ════════════════════ */
.vip-header {
    background: linear-gradient(135deg, #0d1528 0%, #111d38 50%, #0a1220 100%);
    border: 1px solid rgba(56,189,248,0.16);
    border-radius: 18px; padding: 24px 28px; margin-bottom: 1.2rem;
    position: relative; overflow: hidden;
    display: flex; align-items: center; justify-content: space-between;
}
.vip-header::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(56,189,248,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.vip-logo { display: flex; align-items: center; gap: 14px; }
.vip-logo-icon {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    border-radius: 13px; display: flex; align-items: center;
    justify-content: center; font-size: 22px; flex-shrink: 0;
    box-shadow: 0 0 24px rgba(14,165,233,0.4);
}
.vip-title {
    font-family: 'Syne', sans-serif !important; font-size: 21px; font-weight: 800;
    color: #f0f7ff !important; letter-spacing: -0.4px; line-height: 1.15;
}
.vip-sub { font-size: 12px; color: #64748b !important; margin-top: 3px; }
.vip-badges { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.vip-badge {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 13px; border-radius: 20px; font-size: 11px; font-weight: 600;
}
.badge-live { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.32); color: #34d399; }
.badge-user { background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.24); color: #7dd3fc; }
.dot-live {
    width: 6px; height: 6px; background: #34d399; border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.3; transform:scale(0.65); }
}

.kpi-row { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 1.2rem; }
.kpi-card {
    background: linear-gradient(135deg, #0d1528, #111d38);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 14px; padding: 17px 19px;
    position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(0,0,0,0.4); }
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0;
    height:2px; border-radius: 14px 14px 0 0;
}
.kpi-c1::before{background:linear-gradient(90deg,#0ea5e9,#6366f1);}
.kpi-c2::before{background:linear-gradient(90deg,#f59e0b,#ef4444);}
.kpi-c3::before{background:linear-gradient(90deg,#10b981,#0ea5e9);}
.kpi-c4::before{background:linear-gradient(90deg,#a78bfa,#ec4899);}
.kpi-c5::before{background:linear-gradient(90deg,#f472b6,#fb923c);}
.kpi-top { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; }
.kpi-icon { width:34px; height:34px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:16px; }
.kpi-i1{background:rgba(14,165,233,0.15);} .kpi-i2{background:rgba(245,158,11,0.15);}
.kpi-i3{background:rgba(16,185,129,0.15);} .kpi-i4{background:rgba(167,139,250,0.15);}
.kpi-i5{background:rgba(244,114,182,0.15);}
.kpi-label { font-size:10px; font-weight:700; color:#475569 !important; letter-spacing:0.6px; text-transform:uppercase; }
.kpi-value { font-family:'Syne',sans-serif !important; font-size:23px; font-weight:800; color:#f0f7ff !important; letter-spacing:-0.6px; line-height:1; margin-bottom:3px; }
.kpi-sub { font-size:10px; color:#334155 !important; }

.chart-card {
    background: linear-gradient(135deg, #0d1528, #0f1a30);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 16px; padding: 16px 18px 4px; margin-bottom: 1rem;
}
.chart-title { font-family:'Syne',sans-serif !important; font-size:14px; font-weight:700; color:#dde6f5 !important; margin-bottom:2px; }
.chart-sub { font-size:11px; color:#475569 !important; margin-bottom:6px; }

.sb-brand {
    display:flex; align-items:center; gap:10px;
    padding:2px 4px 14px;
    border-bottom:1px solid rgba(56,189,248,0.1); margin-bottom:12px;
}
.sb-icon { width:32px; height:32px; background:linear-gradient(135deg,#0ea5e9,#6366f1); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:15px; flex-shrink:0; }
.sb-name { font-family:'Syne',sans-serif !important; font-size:14px; font-weight:800; color:#f0f7ff !important; }
.sb-ver  { font-size:10px; color:#334155 !important; }
.sb-section { font-size:9px; font-weight:700; color:#475569 !important; letter-spacing:1.1px; text-transform:uppercase; padding:12px 4px 5px; }

.empty-wrap {
    text-align:center; padding:80px 24px;
    background:linear-gradient(135deg,#0d1528,#111d38);
    border:1px dashed rgba(56,189,248,0.2);
    border-radius:16px; margin-top:0.5rem;
}
.empty-icon { font-size:52px; margin-bottom:14px; opacity:0.28; display:block; }
.empty-title { font-family:'Syne',sans-serif !important; font-size:18px; font-weight:700; color:#475569 !important; margin-bottom:7px; }
.empty-sub { font-size:12px; color:#334155 !important; line-height:1.75; }
.empty-sub b { color:#3b82f6 !important; }

.v-card {
    background:linear-gradient(135deg,#0d1528,#0f1a30);
    border:1px solid rgba(56,189,248,0.1);
    border-radius:14px; padding:17px;
    transition:all 0.22s; position:relative; overflow:hidden;
}
.v-card:hover { border-color:rgba(56,189,248,0.38); transform:translateY(-3px); box-shadow:0 12px 36px rgba(0,0,0,0.45); }
.v-avatar { width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:19px; margin-bottom:9px; }
.v-name { font-family:'Syne',sans-serif !important; font-size:13px; font-weight:700; color:#dde6f5 !important; margin-bottom:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.v-loc { font-size:10px; color:#475569 !important; margin-bottom:9px; }
.v-stats { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
.v-stat { background:rgba(255,255,255,0.03); border:1px solid rgba(56,189,248,0.08); border-radius:8px; padding:7px 8px; text-align:center; }
.v-stat-val { font-family:'Syne',sans-serif !important; font-size:12px; font-weight:700; color:#f0f7ff !important; display:block; line-height:1; }
.v-stat-lbl { font-size:9px; color:#475569 !important; margin-top:2px; }

.tbl-info { font-size:11px; color:#475569 !important; margin-bottom:6px; }
.tbl-info strong { color:#38bdf8 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════
COLS = [
    "PO Dt","PO No","Supplier","Item","HSN No","Item Description",
    "Indent Dt","Indent No","UOM","Quantity","Rate",
    "Material","Excise","Discount","Tax","Freight","Others","Net",
]
NUMERIC_COLS = ["Quantity","Rate","Material","Excise","Discount","Tax","Freight","Others","Net"]
PALETTE = ["#0ea5e9","#6366f1","#10b981","#f59e0b","#ec4899",
           "#a78bfa","#38bdf8","#34d399","#fb923c","#f472b6"]
_BG   = "#0d1528"
_GRID = "rgba(56,189,248,0.07)"
_TICK = "#475569"
_LAYOUT = dict(
    paper_bgcolor=_BG, plot_bgcolor=_BG,
    font=dict(family="DM Sans", color=_TICK, size=11),
    margin=dict(t=10, b=10, l=10, r=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=_TICK)),
)

def _ax(grid=True, **kw):
    """Axis config. Pass overrides (incl. tickfont) via **kw to avoid duplicate-key TypeError."""
    base = dict(
        showgrid=grid, gridcolor=_GRID, zeroline=False,
        linecolor="rgba(56,189,248,0.08)",
        tickfont=dict(size=10, color=_TICK),
    )
    base.update(kw)
    return base


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def fmt_inr(n) -> str:
    try:
        n = float(n)
        if n != n: return "₹0"
    except (TypeError, ValueError):
        return "₹0"
    if   n >= 1_00_00_000: return f"₹{n/1_00_00_000:.2f}Cr"
    elif n >= 1_00_000:    return f"₹{n/1_00_000:.2f}L"
    elif n >= 1_000:       return f"₹{n/1_000:.1f}K"
    else:                  return f"₹{n:,.0f}"

def fmt_inr_full(n) -> str:
    try:    return f"₹{float(n):,.2f}"
    except: return "₹0.00"

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    str_cols = ["PO Dt","PO No","Supplier","Item","HSN No","Item Description","Indent Dt","Indent No","UOM"]
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip().replace({"nan":"","None":"","NaN":""})
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df

def safe_sort(series: pd.Series) -> list:
    return sorted(series.dropna().astype(str).replace("", pd.NA).dropna().unique().tolist())

def make_template_csv() -> bytes:
    header = ",".join(COLS) + "\n"
    row = "01/04/2024,PO-00001,Vendor Name,ITM-001,72071190,Item Description,28/03/2024,IN-00001,NOS,10,5000,50000,0,500,8910,1500,250,60160\n"
    return (header + row).encode()


# ═══════════════════════════════════════════════════════════════
#  SAMPLE DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_sample() -> pd.DataFrame:
    import random
    random.seed(42)
    suppliers = ["Tata Steel Ltd","Reliance Industries","Mahindra Logistics",
                 "Bosch India Pvt Ltd","Siemens Ltd","L&T Engineering",
                 "BHEL Corporation","Wipro Infrastructure","HCL Manufacturing","Infosys Supply"]
    items     = ["Cold Rolled Sheets","Hot Rolled Coils","Stainless Steel Pipes",
                 "Aluminium Extrusions","Copper Cables","PVC Conduits",
                 "MS Angles","GI Sheets","Carbon Steel Rods","Mild Steel Plates"]
    hsns = ["7209","7208","7306","7601","8544","3917","7216","7210","7213","7211"]
    uoms = ["MT","NOS","KG","MTR","SET","BOX","PCS","LTR","RLL","CTN"]
    rows = []
    for i in range(150):
        si=random.randint(0,9); ii=random.randint(0,9)
        qty=random.randint(10,500); rate=random.randint(200,6000)
        mat=qty*rate; tax=round(mat*0.18,2); disc=round(mat*0.03,2)
        frgt=random.randint(500,6000); oth=random.randint(100,1500)
        net=round(mat+tax-disc+frgt+oth,2)
        d=random.randint(1,28); m=random.randint(1,12); y=random.choice([2023,2024])
        rows.append({
            "PO Dt":f"{d:02d}/{m:02d}/{y}","PO No":f"PO-{2000+i:05d}",
            "Supplier":suppliers[si],"Item":f"ITM-{1000+ii:04d}",
            "HSN No":hsns[ii],"Item Description":items[ii],
            "Indent Dt":f"{d:02d}/{m:02d}/{y}","Indent No":f"IN-{3000+i:05d}",
            "UOM":uoms[random.randint(0,9)],
            "Quantity":qty,"Rate":rate,"Material":mat,"Excise":0,
            "Discount":disc,"Tax":tax,"Freight":frgt,"Others":oth,"Net":net,
        })
    return clean_df(pd.DataFrame(rows))


# ═══════════════════════════════════════════════════════════════
#  FILE PARSER
# ═══════════════════════════════════════════════════════════════
ALIASES = {
    "PO Dt":           ["po_dt","po_date","po date","order_date","date","inv_date"],
    "PO No":           ["po_no","po","po_number","purchase_order","order_no","voucher_no","po no"],
    "Supplier":        ["supplier","vendor","vendor_name","company","party","firm"],
    "Item":            ["item","item_code","item_no","item code","part_no","part","sku","material_code"],
    "HSN No":          ["hsn_no","hsn","hsn_code","hsn no","sac","sac_code"],
    "Item Description":["item_description","item description","description","material","goods","desc","product"],
    "Indent Dt":       ["indent_dt","indent_date","indent date","req_date","requisition_date"],
    "Indent No":       ["indent_no","indent","indent_number","indent no","req_no","requisition_no"],
    "UOM":             ["uom","unit","unit_of_measure","unit of measure","units"],
    "Quantity":        ["quantity","qty","count","nos"],
    "Rate":            ["rate","unit_price","price","unit_rate","unit price"],
    "Material":        ["material","material_value","basic","basic_amount","material value"],
    "Excise":          ["excise","excise_duty","ced","bed"],
    "Discount":        ["discount","disc","rebate"],
    "Tax":             ["tax","gst","vat","igst","cgst","sgst","taxes"],
    "Freight":         ["freight","shipping","transport","delivery"],
    "Others":          ["others","other","miscellaneous","misc","charges"],
    "Net":             ["net","net_amount","total","amount","net amount","line_total","net_value"],
}

def parse_file(f) -> pd.DataFrame:
    name = f.name.lower()
    try:
        df = pd.read_csv(f) if name.endswith((".csv",".txt")) else pd.read_excel(f)
    except Exception as e:
        print(f"[VendorIQ] File read error: {e}"); traceback.print_exc()
        st.error("❌ Cannot read file — see terminal for details.")
        return pd.DataFrame()
    df.columns = [str(c).strip() for c in df.columns]
    lc = {c.lower().strip(): c for c in df.columns}
    rmap = {}
    for target, aliases in ALIASES.items():
        for a in aliases:
            if a in lc: rmap[lc[a]] = target; break
    df = df.rename(columns=rmap)
    for col in ["PO Dt","PO No","Supplier","Item","HSN No","Item Description","Indent Dt","Indent No","UOM"]:
        if col not in df.columns: df[col] = ""
    for col in NUMERIC_COLS:
        if col not in df.columns: df[col] = 0.0
    df = clean_df(df)
    mask = df["Net"] == 0
    if mask.any():
        df.loc[mask,"Net"] = (df.loc[mask,"Material"]+df.loc[mask,"Excise"]
                              -df.loc[mask,"Discount"]+df.loc[mask,"Tax"]
                              +df.loc[mask,"Freight"]+df.loc[mask,"Others"])
    extras = [c for c in df.columns if c not in COLS]
    return df[[c for c in COLS+extras if c in df.columns]]


# ═══════════════════════════════════════════════════════════════
#  CHART BUILDERS
# ═══════════════════════════════════════════════════════════════
def chart_supplier_bar(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Supplier")["Net"].sum().reset_index().sort_values("Net",ascending=False).head(8)
    g["L"] = g["Supplier"].str[:22]
    fig = go.Figure(go.Bar(
        x=g["L"], y=g["Net"],
        marker=dict(color=g["Net"],colorscale=[[0,"#0ea5e9"],[1,"#6366f1"]],line=dict(width=0)),
        customdata=g["Supplier"],
        hovertemplate="<b>%{customdata}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_traces(marker_cornerradius=5)
    fig.update_layout(**_LAYOUT, height=240, bargap=0.3,
                      xaxis=_ax(False, tickangle=-18), yaxis=_ax(tickprefix="₹"))
    return fig

def chart_material_bar(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Item Description")["Net"].sum().reset_index().sort_values("Net",ascending=False).head(8)
    g["L"] = g["Item Description"].str[:24]
    fig = go.Figure(go.Bar(
        x=g["L"], y=g["Net"],
        marker=dict(color=g["Net"],colorscale=[[0,"#10b981"],[1,"#0ea5e9"]],line=dict(width=0)),
        customdata=g["Item Description"],
        hovertemplate="<b>%{customdata}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_traces(marker_cornerradius=5)
    fig.update_layout(**_LAYOUT, height=240, bargap=0.3,
                      xaxis=_ax(False, tickangle=-18), yaxis=_ax(tickprefix="₹"))
    return fig

def chart_trend(df: pd.DataFrame):
    try:
        d = df.copy()
        d["_dt"] = pd.to_datetime(d["PO Dt"], dayfirst=True, errors="coerce")
        d = d.dropna(subset=["_dt"])
        if d.empty: return None
        d["Month"] = d["_dt"].dt.to_period("M").astype(str)
        g = d.groupby("Month")["Net"].sum().reset_index().sort_values("Month")
        fig = go.Figure(go.Scatter(
            x=g["Month"], y=g["Net"], mode="lines+markers",
            line=dict(color="#0ea5e9",width=2.4),
            marker=dict(size=6,color="#0ea5e9",line=dict(color=_BG,width=2)),
            fill="tozeroy", fillcolor="rgba(14,165,233,0.08)",
            hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(**_LAYOUT, height=210, xaxis=_ax(False), yaxis=_ax(tickprefix="₹"))
        return fig
    except Exception:
        print("[VendorIQ] chart_trend error"); traceback.print_exc(); return None

def chart_cost_breakdown(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Supplier")[["Material","Tax","Freight","Others"]].sum().reset_index()
    g["_total"] = g[["Material","Tax","Freight","Others"]].sum(axis=1)
    g = g.sort_values("_total",ascending=False).head(8)
    fig = go.Figure()
    for col,color,label in [("Material","#0ea5e9","Material"),("Tax","#f59e0b","Tax"),
                             ("Freight","#10b981","Freight"),("Others","#a78bfa","Others")]:
        fig.add_trace(go.Bar(name=label, x=g["Supplier"].str[:18], y=g[col], marker_color=color,
                             hovertemplate=f"<b>%{{x}}</b><br>{label}: ₹%{{y:,.0f}}<extra></extra>"))
    fig.update_layout(**_LAYOUT, height=300, barmode="stack", bargap=0.24,
                      xaxis=_ax(False, tickangle=-18), yaxis=_ax(tickprefix="₹"))
    return fig

def chart_donut(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Supplier")["Net"].sum().reset_index().sort_values("Net",ascending=False).head(10)
    fig = go.Figure(go.Pie(
        labels=g["Supplier"], values=g["Net"], hole=0.55,
        marker=dict(colors=PALETTE, line=dict(color=_BG, width=2)),
        textposition="inside", textinfo="percent",
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    layout = {**_LAYOUT, "height":300}
    layout["legend"] = dict(orientation="v", font=dict(size=10), x=1.01, y=0.5)
    fig.update_layout(**layout)
    return fig

def chart_hbar(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("Item Description")["Net"].sum().reset_index().sort_values("Net",ascending=True).tail(10)
    g["L"] = g["Item Description"].str[:32]
    fig = go.Figure(go.Bar(
        y=g["L"], x=g["Net"], orientation="h",
        marker=dict(color=g["Net"],colorscale=[[0,"#6366f1"],[1,"#0ea5e9"]],line=dict(width=0)),
        customdata=g["Item Description"],
        hovertemplate="<b>%{customdata}</b><br>₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_traces(marker_cornerradius=4)
    # ✅ FIX: tickfont passed INTO _ax() as kwarg — no duplicate key TypeError
    fig.update_layout(**_LAYOUT, height=320, bargap=0.22,
                      xaxis=_ax(tickprefix="₹"),
                      yaxis=_ax(False, tickfont=dict(size=9, color=_TICK)))
    return fig

def chart_discount_tax(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=df["Discount"], y=df["Tax"], mode="markers",
        marker=dict(color=df["Net"],colorscale="Blues",size=7,opacity=0.75,
                    line=dict(color="#0ea5e9",width=0.5),showscale=True,
                    colorbar=dict(title="Net ₹",tickprefix="₹",tickfont=dict(size=9,color=_TICK))),
        text=df["Supplier"],
        hovertemplate="<b>%{text}</b><br>Discount: ₹%{x:,.0f}<br>Tax: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, height=300,
                      xaxis=_ax(title="Discount (₹)", tickprefix="₹"),
                      yaxis=_ax(title="Tax (₹)", tickprefix="₹"))
    return fig

def chart_uom_bar(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("UOM")["Net"].sum().reset_index().sort_values("Net",ascending=False)
    fig = go.Figure(go.Bar(
        x=g["UOM"], y=g["Net"],
        marker=dict(color=g["Net"],colorscale=[[0,"#f59e0b"],[1,"#ef4444"]],line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_traces(marker_cornerradius=5)
    fig.update_layout(**_LAYOUT, height=300, bargap=0.3,
                      xaxis=_ax(False), yaxis=_ax(tickprefix="₹"))
    return fig

def _render(fn, df, key):
    """Safe chart render — errors → terminal only, never crash the UI."""
    try:
        fig = fn(df)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar":False}, key=key)
    except Exception:
        print(f"[VendorIQ] Chart error key={key}"); traceback.print_exc()


# ═══════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-icon">🏭</div>
      <div><div class="sb-name">VendorIQ</div><div class="sb-ver">v3.1 · Intelligence Portal</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-section">📥 Import Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload file", type=["csv","xlsx","xls","txt"], label_visibility="collapsed")
    if uploaded:
        parsed = parse_file(uploaded)
        if not parsed.empty:
            c1,c2 = st.columns(2)
            with c1:
                if st.button("➕ Append", use_container_width=True):
                    st.session_state.df = clean_df(pd.concat([st.session_state.df, parsed], ignore_index=True))
                    st.success(f"✅ {len(parsed):,} rows added")
            with c2:
                if st.button("🔄 Replace", use_container_width=True):
                    st.session_state.df = clean_df(parsed)
                    st.success(f"✅ {len(parsed):,} rows loaded")

    qa1,qa2 = st.columns(2)
    with qa1:
        if st.button("🎲 Sample Data", use_container_width=True):
            st.session_state.df = load_sample()
            st.success("✅ 150 rows loaded")
    with qa2:
        st.download_button("📄 Template", data=make_template_csv(),
                           file_name="vendor_template.csv", mime="text/csv", use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sb-section">🔽 Filters</div>', unsafe_allow_html=True)

    df_all = st.session_state.df
    if df_all.empty:
        st.markdown('<p style="color:#475569;font-size:12px;padding:4px 2px">Import data to enable filters</p>', unsafe_allow_html=True)
        f_sup=[]; f_item=""; f_min=0.0; f_max=0.0
    else:
        f_sup  = st.multiselect("🏢 Supplier", safe_sort(df_all["Supplier"]), default=[])
        f_item = st.text_input("📦 Item Description", placeholder="Search item description…", key="f_item_search")
        mn=float(df_all["Net"].min()); mx=float(df_all["Net"].max())
        if mn < mx:
            f_min,f_max = st.slider("💰 Net Amount (₹)", min_value=mn, max_value=mx, value=(mn,mx), format="₹%.0f")
        else:
            f_min,f_max = mn,mx

    st.markdown("---")
    if not df_all.empty:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.df = pd.DataFrame(); st.rerun()

    st.markdown('<p style="font-size:9px;color:#1e293b;text-align:center;margin-top:14px">© 2024 VendorIQ · All rights reserved</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="vip-header">
  <div class="vip-logo">
    <div class="vip-logo-icon">🏭</div>
    <div>
      <div class="vip-title">Vendor Intelligence Portal</div>
      <div class="vip-sub">Search · Analyse · Export purchase order &amp; vendor supply data</div>
    </div>
  </div>
  <div class="vip-badges">
    <div class="vip-badge badge-live"><div class="dot-live"></div> Live</div>
    <div class="vip-badge badge-user">👤 Welcome User </div>
  </div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  GLOBAL SEARCH + EXPORT / REFRESH
# ═══════════════════════════════════════════════════════════════
sc1,sc2,sc3 = st.columns([6,1,1])
with sc1:
    g_search = st.text_input("global_search", label_visibility="collapsed",
                              placeholder="🔍   Search vendor, item, PO number, HSN, description…", key="g_search")
with sc2:
    if st.session_state.df.empty:
        st.button("📤 Export", disabled=True, use_container_width=True)
    else:
        st.download_button("📤 Export", data=st.session_state.df.to_csv(index=False).encode(),
                           file_name=f"vendor_{datetime.today():%Y%m%d}.csv",
                           mime="text/csv", use_container_width=True, key="dl_global")
with sc3:
    if st.button("🔄 Refresh", use_container_width=True): st.rerun()


# ═══════════════════════════════════════════════════════════════
#  BUILD FILTERED DATAFRAME
# ═══════════════════════════════════════════════════════════════
df = st.session_state.df.copy()
if not df.empty:
    if g_search.strip():
        q = g_search.strip().lower()
        mask = pd.Series(False, index=df.index)
        for col in ["Supplier","Item Description","PO No","Item","HSN No","Indent No"]:
            if col in df.columns:
                mask |= df[col].astype(str).str.lower().str.contains(q, na=False)
        df = df[mask]
    if f_sup:   df = df[df["Supplier"].isin(f_sup)]
    if f_item.strip():
        df = df[df["Item Description"].astype(str).str.lower().str.contains(f_item.strip().lower(), na=False)]
    if f_min != f_max: df = df[(df["Net"]>=f_min)&(df["Net"]<=f_max)]


# ═══════════════════════════════════════════════════════════════
#  EMPTY STATE
# ═══════════════════════════════════════════════════════════════
if df.empty:
    st.markdown("""
    <div class="empty-wrap">
      <span class="empty-icon">🏭</span>
      <div class="empty-title">No data yet</div>
      <div class="empty-sub">
        Click <b>🎲 Sample Data</b> in the sidebar to load demo records,<br>
        or upload your own CSV / Excel file.
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════════
#  KPI CARDS
# ═══════════════════════════════════════════════════════════════
total_net=df["Net"].sum(); total_material=df["Material"].sum()
total_tax=df["Tax"].sum(); total_discount=df["Discount"].sum()
uniq_vendors=df["Supplier"].nunique()

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card kpi-c1">
    <div class="kpi-top"><div class="kpi-label">Total Net Value</div><div class="kpi-icon kpi-i1">💰</div></div>
    <div class="kpi-value">{fmt_inr(total_net)}</div><div class="kpi-sub">Total procurement spend</div>
  </div>
  <div class="kpi-card kpi-c2">
    <div class="kpi-top"><div class="kpi-label">Material Value</div><div class="kpi-icon kpi-i2">🏗️</div></div>
    <div class="kpi-value">{fmt_inr(total_material)}</div><div class="kpi-sub">Base material cost</div>
  </div>
  <div class="kpi-card kpi-c3">
    <div class="kpi-top"><div class="kpi-label">Total Tax</div><div class="kpi-icon kpi-i3">🧾</div></div>
    <div class="kpi-value">{fmt_inr(total_tax)}</div><div class="kpi-sub">GST / VAT collected</div>
  </div>
  <div class="kpi-card kpi-c4">
    <div class="kpi-top"><div class="kpi-label">Total Discount</div><div class="kpi-icon kpi-i4">🏷️</div></div>
    <div class="kpi-value">{fmt_inr(total_discount)}</div><div class="kpi-sub">Savings on orders</div>
  </div>
  <div class="kpi-card kpi-c5">
    <div class="kpi-top"><div class="kpi-label">Unique Vendors</div><div class="kpi-icon kpi-i5">🏢</div></div>
    <div class="kpi-value">{uniq_vendors}</div><div class="kpi-sub">Distinct suppliers</div>
  </div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  OVERVIEW CHARTS
# ═══════════════════════════════════════════════════════════════
ch1,ch2 = st.columns(2)
with ch1:
    st.markdown('<div class="chart-card"><div class="chart-title">🏢 Top Suppliers by Net Value</div><div class="chart-sub">Total net spend per vendor</div>', unsafe_allow_html=True)
    _render(chart_supplier_bar, df, "ov1")
    st.markdown('</div>', unsafe_allow_html=True)
with ch2:
    st.markdown('<div class="chart-card"><div class="chart-title">📦 Top Items by Net Value</div><div class="chart-sub">Highest-value item descriptions</div>', unsafe_allow_html=True)
    _render(chart_material_bar, df, "ov2")
    st.markdown('</div>', unsafe_allow_html=True)

trend_fig = chart_trend(df)
if trend_fig:
    st.markdown('<div class="chart-card"><div class="chart-title">📈 Monthly Spend Trend</div><div class="chart-sub">Net procurement value by PO month</div>', unsafe_allow_html=True)
    st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar":False}, key="ov3")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card"><div class="chart-title">📊 Cost Breakdown by Supplier</div><div class="chart-sub">Material · Tax · Freight · Others stacked per vendor</div>', unsafe_allow_html=True)
_render(chart_cost_breakdown, df, "ov4")
st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════
tab_rec, tab_vs, tab_an = st.tabs([f"📋  Records  ({len(df):,})", "🏢  Vendor Summary", "📊  Analytics"])


# ─────────────────────────────────────────────────────────────
#  TAB 1 : RECORDS
# ─────────────────────────────────────────────────────────────
with tab_rec:
    tb1,tb2,tb3,tb4 = st.columns([3,2,1.8,1.2])
    with tb1:
        tbl_q = st.text_input("tbl_search", label_visibility="collapsed", placeholder="🔍  Filter table rows…", key="tbl_search")
    with tb2:
        sup_opts = ["All Suppliers"]+safe_sort(df["Supplier"])
        sel_sup  = st.selectbox("Supplier filter", sup_opts, label_visibility="collapsed", key="sel_sup")
    with tb3:
        sort_by = st.selectbox("Sort by", ["Net ↓","Net ↑","PO Dt ↓","Supplier A-Z","Rate ↓","Material ↓"],
                               label_visibility="collapsed", key="sort_by")
    with tb4:
        st.download_button("📤 Export", data=df.to_csv(index=False).encode(),
                           file_name=f"records_{datetime.today():%Y%m%d}.csv",
                           mime="text/csv", use_container_width=True, key="dl_tab1")

    df_tbl = df.copy()
    if tbl_q.strip():
        q2=tbl_q.strip().lower(); m2=pd.Series(False,index=df_tbl.index)
        for col in ["Supplier","Item Description","PO No","Item","HSN No"]:
            if col in df_tbl.columns: m2 |= df_tbl[col].astype(str).str.lower().str.contains(q2,na=False)
        df_tbl = df_tbl[m2]
    if sel_sup!="All Suppliers": df_tbl=df_tbl[df_tbl["Supplier"]==sel_sup]

    sort_map={"Net ↓":("Net",False),"Net ↑":("Net",True),"PO Dt ↓":("PO Dt",False),
              "Supplier A-Z":("Supplier",True),"Rate ↓":("Rate",False),"Material ↓":("Material",False)}
    sc_,sa_=sort_map.get(sort_by,("Net",False))
    if sc_ in df_tbl.columns: df_tbl=df_tbl.sort_values(sc_,ascending=sa_)

    st.markdown(f'<div class="tbl-info">Showing <strong>{len(df_tbl):,}</strong> of <strong>{len(df):,}</strong> records — Net Total: <strong>{fmt_inr(df_tbl["Net"].sum())}</strong></div>', unsafe_allow_html=True)

    disp=df_tbl.copy()
    for c in ["Rate","Material","Excise","Discount","Tax","Freight","Others","Net"]:
        if c in disp.columns: disp[c]=disp[c].apply(fmt_inr_full)
    if "Quantity" in disp.columns: disp["Quantity"]=disp["Quantity"].apply(lambda x:f"{int(x):,}")

    st.dataframe(disp, use_container_width=True, height=min(42+len(disp)*36,560), hide_index=True,
                 column_config={
                     "PO Dt":st.column_config.TextColumn("📅 PO Dt",width=100),
                     "PO No":st.column_config.TextColumn("📄 PO No",width=160),
                     "Supplier":st.column_config.TextColumn("🏢 Supplier",width=200),
                     "Item":st.column_config.TextColumn("🔖 Item",width=90),
                     "HSN No":st.column_config.TextColumn("🔢 HSN",width=80),
                     "Item Description":st.column_config.TextColumn("📦 Description",width=240),
                     "Indent Dt":st.column_config.TextColumn("📅 Indent Dt",width=100),
                     "Indent No":st.column_config.TextColumn("📋 Indent No",width=130),
                     "UOM":st.column_config.TextColumn("📐 UOM",width=65),
                     "Quantity":st.column_config.TextColumn("Qty",width=70),
                     "Rate":st.column_config.TextColumn("💵 Rate",width=110),
                     "Material":st.column_config.TextColumn("🏗️ Material",width=110),
                     "Excise":st.column_config.TextColumn("Excise",width=90),
                     "Discount":st.column_config.TextColumn("🏷️ Discount",width=100),
                     "Tax":st.column_config.TextColumn("🧾 Tax",width=100),
                     "Freight":st.column_config.TextColumn("🚚 Freight",width=100),
                     "Others":st.column_config.TextColumn("Others",width=85),
                     "Net":st.column_config.TextColumn("💰 Net",width=120),
                 })


# ─────────────────────────────────────────────────────────────
#  TAB 2 : VENDOR SUMMARY
# ─────────────────────────────────────────────────────────────
with tab_vs:
    vs = (df.groupby("Supplier")
            .agg(Records=("Net","count"),Total_Net=("Net","sum"),
                 Total_Material=("Material","sum"),Total_Tax=("Tax","sum"),
                 Total_Discount=("Discount","sum"),Total_Freight=("Freight","sum"),
                 Avg_Rate=("Rate","mean"))
            .reset_index().sort_values("Total_Net",ascending=False))
    vs["Share_%"]=(vs["Total_Net"]/vs["Total_Net"].sum()*100).round(1)

    avatars=["🏗️","⚙️","🔩","🧪","🌲","🧵","🔬","💎","⚡","🛠️","🎯","🔧"]
    av_bgs=["rgba(14,165,233,0.14)","rgba(99,102,241,0.14)","rgba(16,185,129,0.14)",
            "rgba(245,158,11,0.14)","rgba(236,72,153,0.14)","rgba(167,139,250,0.14)"]

    top6=vs.head(6); cols=st.columns(3)
    for i,(_,row) in enumerate(top6.iterrows()):
        with cols[i%3]:
            st.markdown(f"""
            <div class="v-card" style="margin-bottom:12px">
              <div class="v-avatar" style="background:{av_bgs[i%len(av_bgs)]}">{avatars[i%len(avatars)]}</div>
              <div class="v-name" title="{row.Supplier}">{row.Supplier}</div>
              <div class="v-loc">📋 {int(row.Records)} orders &nbsp;|&nbsp; Avg Rate: {fmt_inr(row.Avg_Rate)}</div>
              <div class="v-stats">
                <div class="v-stat"><span class="v-stat-val" style="color:#38bdf8">{fmt_inr(row.Total_Net)}</span><div class="v-stat-lbl">Net Value</div></div>
                <div class="v-stat"><span class="v-stat-val" style="color:#34d399">{row["Share_%"]:.1f}%</span><div class="v-stat-lbl">Spend Share</div></div>
                <div class="v-stat"><span class="v-stat-val" style="color:#f59e0b">{fmt_inr(row.Total_Tax)}</span><div class="v-stat-lbl">Total Tax</div></div>
                <div class="v-stat"><span class="v-stat-val" style="color:#f472b6">{fmt_inr(row.Total_Discount)}</span><div class="v-stat-lbl">Discount</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("**📋 All Vendors**")

    vd=vs.copy()
    vd["Net Value"]=vd["Total_Net"].apply(fmt_inr_full)
    vd["Material"]=vd["Total_Material"].apply(fmt_inr_full)
    vd["Tax"]=vd["Total_Tax"].apply(fmt_inr_full)
    vd["Discount"]=vd["Total_Discount"].apply(fmt_inr_full)
    vd["Freight"]=vd["Total_Freight"].apply(fmt_inr_full)
    vd["Avg Rate"]=vd["Avg_Rate"].apply(fmt_inr_full)
    vd["Share"]=vd["Share_%"].apply(lambda x:f"{x:.1f}%")
    vd=vd[["Supplier","Records","Net Value","Material","Tax","Discount","Freight","Avg Rate","Share"]]

    st.dataframe(vd, use_container_width=True, height=min(42+len(vd)*36,480), hide_index=True,
                 column_config={
                     "Supplier":st.column_config.TextColumn("🏢 Supplier",width=220),
                     "Records":st.column_config.NumberColumn("Records",width=80,format="%d"),
                     "Net Value":st.column_config.TextColumn("💰 Net Value",width=130),
                     "Material":st.column_config.TextColumn("🏗️ Material",width=130),
                     "Tax":st.column_config.TextColumn("🧾 Tax",width=120),
                     "Discount":st.column_config.TextColumn("🏷️ Discount",width=120),
                     "Freight":st.column_config.TextColumn("🚚 Freight",width=110),
                     "Avg Rate":st.column_config.TextColumn("Avg Rate",width=120),
                     "Share":st.column_config.TextColumn("Share %",width=80),
                 })
    st.download_button("📤 Export Vendor Summary", data=vs.to_csv(index=False).encode(),
                       file_name=f"vendor_summary_{datetime.today():%Y%m%d}.csv",
                       mime="text/csv", key="dl_vs")


# ─────────────────────────────────────────────────────────────
#  TAB 3 : ANALYTICS
# ─────────────────────────────────────────────────────────────
with tab_an:
    ac1,ac2 = st.columns(2)
    with ac1:
        st.markdown('<div class="chart-card"><div class="chart-title">🍩 Vendor Spend Share</div><div class="chart-sub">Top 10 vendors by proportion of net spend</div>', unsafe_allow_html=True)
        _render(chart_donut, df, "an1")
        st.markdown('</div>', unsafe_allow_html=True)
    with ac2:
        st.markdown('<div class="chart-card"><div class="chart-title">📊 Top Items Ranked</div><div class="chart-sub">Highest-value items by net amount</div>', unsafe_allow_html=True)
        _render(chart_hbar, df, "an2")
        st.markdown('</div>', unsafe_allow_html=True)

    ac3,ac4 = st.columns(2)
    with ac3:
        st.markdown('<div class="chart-card"><div class="chart-title">💹 Discount vs Tax Analysis</div><div class="chart-sub">Each dot = one PO line · colour = Net value</div>', unsafe_allow_html=True)
        _render(chart_discount_tax, df, "an3")
        st.markdown('</div>', unsafe_allow_html=True)
    with ac4:
        st.markdown('<div class="chart-card"><div class="chart-title">🔢 Spend by UOM</div><div class="chart-sub">Net value grouped by unit of measure</div>', unsafe_allow_html=True)
        _render(chart_uom_bar, df, "an4")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("**💎 Full Pricing Table — sorted by Net Value**")
    ps=df.copy().sort_values("Net",ascending=False)
    for c in ["Rate","Material","Excise","Discount","Tax","Freight","Others","Net"]:
        if c in ps.columns: ps[c]=ps[c].apply(fmt_inr_full)
    if "Quantity" in ps.columns:
        ps["Quantity"]=ps["Quantity"].apply(lambda x:f"{int(float(x)):,}" if str(x).replace(".","",1).isdigit() else x)

    show_cols=[c for c in COLS if c in ps.columns]
    st.dataframe(ps[show_cols], use_container_width=True, height=400, hide_index=True,
                 column_config={
                     "PO Dt":st.column_config.TextColumn("📅 PO Dt",width=100),
                     "PO No":st.column_config.TextColumn("📄 PO No",width=155),
                     "Supplier":st.column_config.TextColumn("🏢 Supplier",width=195),
                     "Item":st.column_config.TextColumn("🔖 Item",width=85),
                     "HSN No":st.column_config.TextColumn("🔢 HSN",width=80),
                     "Item Description":st.column_config.TextColumn("📦 Description",width=240),
                     "Indent Dt":st.column_config.TextColumn("📅 Indent Dt",width=100),
                     "Indent No":st.column_config.TextColumn("📋 Indent No",width=125),
                     "UOM":st.column_config.TextColumn("📐 UOM",width=65),
                     "Quantity":st.column_config.TextColumn("Qty",width=70),
                     "Rate":st.column_config.TextColumn("💵 Rate",width=110),
                     "Material":st.column_config.TextColumn("🏗️ Material",width=110),
                     "Excise":st.column_config.TextColumn("Excise",width=90),
                     "Discount":st.column_config.TextColumn("🏷️ Discount",width=100),
                     "Tax":st.column_config.TextColumn("🧾 Tax",width=100),
                     "Freight":st.column_config.TextColumn("🚚 Freight",width=95),
                     "Others":st.column_config.TextColumn("Others",width=85),
                     "Net":st.column_config.TextColumn("💰 Net",width=115),
                 })

    col_dl1,col_dl2,_=st.columns([1.2,1.2,4])
    with col_dl1:
        st.download_button("📥 Download CSV", data=df.to_csv(index=False).encode(),
                           file_name=f"vendor_data_{datetime.today():%Y%m%d}.csv",
                           mime="text/csv", key="dl_an_csv")
    with col_dl2:
        try:
            buf=io.BytesIO()
            with pd.ExcelWriter(buf,engine="openpyxl") as w: df.to_excel(w,index=False,sheet_name="VendorData")
            st.download_button("📥 Download Excel", data=buf.getvalue(),
                               file_name=f"vendor_data_{datetime.today():%Y%m%d}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key="dl_an_xlsx")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:24px 0 4px;font-size:10px;color:#1e293b;letter-spacing:0.3px">
  VendorIQ Intelligence Portal &nbsp;·&nbsp; Built with Streamlit
  &nbsp;·&nbsp; <span style="color:#0ea5e9">● Live</span>
</div>""", unsafe_allow_html=True)