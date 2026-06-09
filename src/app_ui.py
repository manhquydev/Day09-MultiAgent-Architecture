import sys
from pathlib import Path
import re
import json

# Ensure src is in python path
src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import streamlit as st
from app.config import Settings
from app.graph import ShoppingAssistant
from app.data_access import ShoppingDataStore

# Page config
st.set_page_config(
    page_title="VinShop Demo - Multi-Agent Shopping Assistant",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------
# 1. State & Theme Initialization
# ----------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "active_trace" not in st.session_state:
    st.session_state.active_trace = None

if "custom_settings" not in st.session_state:
    st.session_state.custom_settings = Settings.load()

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Color tokens based on dark/light
bg = "#09090b" if IS_DARK else "#ffffff"
bg_subtle = "#0e0e11" if IS_DARK else "#f9fafb"
card = "#121216" if IS_DARK else "#ffffff"
card_hover = "#1a1a22" if IS_DARK else "#f4f4f5"
border = "#27272a" if IS_DARK else "#e4e4e7"
border_subtle = "#1f1f23" if IS_DARK else "#f0f0f2"
text = "#fafafa" if IS_DARK else "#09090b"
text_dim = "#71717a" if IS_DARK else "#a1a1aa"
green = "#22c55e" if IS_DARK else "#16a34a"
green_muted = "rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"
red = "#ef4444" if IS_DARK else "#dc2626"
red_muted = "rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"
amber = "#f59e0b" if IS_DARK else "#d97706"
amber_muted = "rgba(245,158,11,0.12)" if IS_DARK else "rgba(217,119,6,0.08)"
shadow = "none" if IS_DARK else "0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)"

# Custom CSS Injection
st.markdown(f"""
<style>
/* Hide Streamlit Default Chrome */
header[data-testid="stHeader"], footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton {{
    display: none !important;
}}
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: {bg} !important;
    color: {text} !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}}
.block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1440px !important;
}}

/* Custom Sidebar styling */
section[data-testid="stSidebar"] {{
    background-color: {bg_subtle} !important;
    border-right: 1px solid {border} !important;
}}

/* Styled Title */
.brand-title {{
    font-size: 1.5rem;
    font-weight: 700;
    color: {text};
    letter-spacing: -0.03em;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.brand-subtitle {{
    font-size: 0.8rem;
    color: #71717a;
    margin-bottom: 1.5rem;
}}

/* Metric Card */
.metric-card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: {shadow};
    margin-bottom: 0.75rem;
}}
.metric-label {{
    font-size: 0.72rem;
    color: #71717a;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.metric-value {{
    font-size: 1.4rem;
    font-weight: 700;
    color: {text};
    letter-spacing: -0.02em;
    margin-top: 0.2rem;
}}

/* Data table styling */
.data-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.8rem;
    margin-top: 0.5rem;
    border: 1px solid {border};
    border-radius: 8px;
    overflow: hidden;
}}
.data-table th {{
    text-align: left;
    padding: 0.6rem 0.8rem;
    color: #71717a;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1px solid {border};
    background: {bg_subtle};
}}
.data-table td {{
    padding: 0.65rem 0.8rem;
    color: {text};
    border-bottom: 1px solid {border_subtle};
    background: {card};
}}
.data-table tr:hover td {{
    background: {card_hover} !important;
}}
.data-table tr:last-child td {{
    border-bottom: none;
}}

/* Custom Chat Bubbles */
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 520px;
    overflow-y: auto;
    padding-right: 5px;
}}
.chat-bubble {{
    padding: 0.8rem 1rem;
    border-radius: 10px;
    font-size: 0.875rem;
    line-height: 1.45;
    box-shadow: {shadow};
    border: 1px solid {border};
    position: relative;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}}
.chat-bubble:hover {{
    border-color: #2563eb;
    transform: translateY(-1px);
}}
.chat-user {{
    background: {bg_subtle};
    align-self: flex-end;
    border-radius: 12px 12px 0 12px;
    max-width: 85%;
}}
.chat-assistant {{
    background: {card};
    align-self: flex-start;
    border-radius: 12px 12px 12px 0;
    max-width: 85%;
}}
.chat-meta {{
    font-size: 0.68rem;
    color: #71717a;
    margin-top: 0.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* Badge Indicators */
.badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}}
.badge-green {{ color: {green}; background: {green_muted}; }}
.badge-red {{ color: {red}; background: {red_muted}; }}
.badge-amber {{ color: {amber}; background: {amber_muted}; }}
.badge-blue {{ color: #2563eb; background: rgba(37,99,235,0.1); }}

/* Pill tabs override */
button[data-baseweb="tab"] {{
    background: transparent !important;
    color: #71717a !important;
    font-size: 0.835rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1rem !important;
    border: 1px solid transparent !important;
    border-radius: 7px !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {text} !important;
    background: {card} !important;
    border-color: {border} !important;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
    display: none !important;
}}
[data-baseweb="tab-list"] {{
    gap: 4px !important;
    background: {bg_subtle} !important;
    border: 1px solid {border} !important;
    border-radius: 10px !important;
    padding: 3px;
    margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# 2. Assistant Loader & Data Cache
# ----------------------------------------------------
@st.cache_resource
def load_assistant(provider, model, temp, top_k):
    settings = Settings.load()
    # Apply dynamic overrides
    settings.provider = provider
    settings.model = model
    settings.temperature = temp
    settings.top_k = top_k
    
    # Also override for all workers to simplify dynamic testing
    settings.supervisor_provider = provider
    settings.supervisor_model = model
    settings.policy_provider = provider
    settings.policy_model = model
    settings.data_provider = provider
    settings.data_model = model
    settings.response_provider = provider
    settings.response_model = model
    
    return ShoppingAssistant(settings)

@st.cache_resource
def load_data_store():
    settings = Settings.load()
    return ShoppingDataStore(settings.orders_path)

data_store = load_data_store()

# Sidebar Configuration
with st.sidebar:
    st.markdown(f'<div class="brand-title">◆ Dynamic Setup</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Configure model & parameters</div>', unsafe_allow_html=True)
    
    prov_opt = ["gemini", "openai", "deepseek", "ollama"]
    selected_provider = st.selectbox("LLM Provider", prov_opt, index=prov_opt.index(st.session_state.custom_settings.provider))
    
    # Models list based on provider
    if selected_provider == "gemini":
        model_opt = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    elif selected_provider == "openai":
        model_opt = ["gpt-4o-mini", "gpt-4o", "o1-mini"]
    elif selected_provider == "deepseek":
        model_opt = ["deepseek-chat", "deepseek-reasoner"]
    else:
        model_opt = ["gemma2:9b", "llama3.1:8b", "mistral:7b"]
        
    selected_model = st.selectbox("LLM Model", model_opt, index=0)
    
    selected_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    selected_top_k = st.slider("RAG Top K Hits", min_value=2, max_value=10, value=6, step=1)
    
    st.markdown("---")
    # Quick Test Presets
    st.markdown("**💡 Quick Test Presets:**")
    presets = [
        ("Q01: Trả hàng", "Chính sách hoàn trả hàng ra sao?"),
        ("Q06: Giao hàng 1971", "Đơn hàng 1971 bao giờ được giao?"),
        ("Q11: Trả hàng 1971?", "Đơn hàng 1971 có được hoàn trả không?"),
        ("Q15: Hỗ trợ voucher", "Voucher của tôi còn dùng được không?"),
        ("Q21: Quota voucher", "Khách hàng C001 tối đa dùng bao nhiêu voucher mỗi tháng?")
    ]
    
    preset_clicked = None
    for label, q_text in presets:
        if st.button(label, use_container_width=True):
            preset_clicked = q_text
            
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.active_trace = None
        st.rerun()

# Load Cached Assistant
assistant = load_assistant(selected_provider, selected_model, selected_temp, selected_top_k)


# ----------------------------------------------------
# 3. Main Dashboard Layout
# ----------------------------------------------------

# Header Row
head_left, head_right = st.columns([10, 2])
with head_left:
    st.markdown('<div class="brand-title">VinShop Demo ◆ Shopping Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Multi-Agent framework with RAG & local database tools. Click on any assistant response to view its reasoning trace.</div>', unsafe_allow_html=True)
with head_right:
    theme_lbl = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
    st.button(theme_lbl, on_click=toggle_theme, use_container_width=True)

col_chat, col_details = st.columns([5, 7])

# ----------------------------------------------------
# Left Column: Chat Interface
# ----------------------------------------------------
with col_chat:
    st.markdown("### 💬 Chat interface")
    
    # Process preset click or chat input
    user_query = st.chat_input("Hỏi tôi về chính sách shop hoặc mã đơn hàng/khách hàng...")
    
    if preset_clicked:
        user_query = preset_clicked
        
    if user_query:
        # Append User message
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        
        # Invoke assistant
        with st.spinner("Assistant is thinking..."):
            res = assistant.ask(user_query)
            
        # Append Assistant response & trace
        st.session_state.chat_history.append({
            "role": "assistant",
            "text": res["final_answer"],
            "route": res.get("route"),
            "status": res.get("status"),
            "policy_result": res.get("policy_result"),
            "data_result": res.get("data_result"),
            "trace": res.get("trace")
        })
        # Auto-set active trace
        st.session_state.active_trace = st.session_state.chat_history[-1]
        
    # Render chat bubbles
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for idx, msg in enumerate(st.session_state.chat_history):
        role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
        bubble_type = "👤 Bạn" if msg["role"] == "user" else "🤖 VinShop AI Assistant"
        
        # Check if active
        active_border = "border-color: #2563eb; transform: translateY(-1px);" if st.session_state.active_trace == msg else ""
        
        # Content rendering
        clean_text = msg["text"].replace("\n", "<br>")
        
        # Meta footer
        meta_html = ""
        if msg["role"] == "assistant":
            route_str = " → ".join(msg.get("route", [])) if msg.get("route") else "None"
            status_val = msg.get("status", "ok")
            status_class = "badge-green" if status_val == "ok" else ("badge-amber" if status_val == "clarification_needed" else "badge-red")
            meta_html = f"""
            <div class="chat-meta">
                <span>Route: <code>{route_str}</code></span>
                <span class="badge {status_class}">{status_val}</span>
            </div>
            """
            
        st.markdown(f"""
        <div class="chat-bubble {role_class}" style="{active_border}" onclick="document.dispatchEvent(new CustomEvent('select-msg', {{detail: {idx}}}));">
            <strong>{bubble_type}</strong><br>
            <div style="margin-top: 0.4rem;">{clean_text}</div>
            {meta_html}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------------------------------
# Right Column: Details & Database Inspection
# ----------------------------------------------------
with col_details:
    st.markdown("### 🔍 Agent Thought Process & Data Inspection")
    
    t_thoughts, t_customers, t_orders = st.tabs([
        "🧠 Thoughts & Trace", 
        "👥 Customer Database", 
        "📦 Orders Database"
    ])
    
    # TAB 1: Thoughts & Trace
    with t_thoughts:
        active = st.session_state.active_trace
        if not active:
            st.info("💡 Chưa có lượt hội thoại nào được chọn. Hãy hỏi trợ lý hoặc click vào một tin nhắn để xem vết suy luận của Agent.")
        else:
            st.markdown(f"#### 🔎 Trace Inspector cho câu hỏi:")
            st.markdown(f"> *\"{active.get('text') if active.get('role') == 'user' else 'Câu trả lời trợ lý'}\"*")
            
            # Show summary parameters
            c1, c2, c3 = st.columns(3)
            with c1:
                status_val = active.get("status", "ok")
                status_class = "badge-green" if status_val == "ok" else ("badge-amber" if status_val == "clarification_needed" else "badge-red")
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Trạng thái định tuyến</div>
                    <div class="metric-value"><span class="badge {status_class}" style="font-size: 1.1rem; padding: 4px 12px;">{status_val}</span></div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                route_list = active.get("route", [])
                route_str = " ➔ ".join(route_list) if route_list else "Supervisor"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Đường dẫn thực thi (Route)</div>
                    <div class="metric-value" style="font-size: 1.1rem; color: #2563eb;">{route_str}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                # Calculate processing steps
                steps = len(active.get("trace", []))
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Số bước xử lý (Steps)</div>
                    <div class="metric-value">{steps} nodes</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Expand details of each node trace
            st.markdown("##### 🚀 Tiến trình hoạt động của các Agent (LangGraph nodes)")
            for node_trace in active.get("trace", []):
                node_name = node_trace.get("node")
                with st.expander(f"📍 Node: {node_name}", expanded=True):
                    # Format JSON payload nicely
                    st.markdown("**Output Payload:**")
                    st.json(node_trace.get("output", {}))
                    
                    if "raw_response" in node_trace:
                        st.markdown("**Mô hình trả về (Raw Response):**")
                        st.code(node_trace.get("raw_response"))
                        
            # Show retrieved facts if present
            if active.get("policy_result") and active["policy_result"].get("raw_hits"):
                st.markdown("##### 📚 Tài liệu chính sách khớp từ RAG (Chroma Policy Store)")
                for hit in active["policy_result"]["raw_hits"]:
                    with st.expander(f"📖 {hit['citation']} (Khoảng cách: {hit['distance']:.4f})", expanded=False):
                        st.write(hit["content"])
                        
    # TAB 2: Customer Database
    with t_customers:
        st.markdown("#### 👥 Danh sách Khách hàng giả lập (Mock Customers)")
        
        # Build HTML table for customers
        rows = ""
        for cust in data_store.customers_list:
            tier_badge = "badge-green" if cust.get("tier") == "Gold" else ("badge-blue" if cust.get("tier") == "Silver" else "badge-amber")
            rows += f"""
            <tr>
                <td><strong>{cust.get('customer_id')}</strong></td>
                <td>{cust.get('customer_name')}</td>
                <td><span class="badge {tier_badge}">{cust.get('tier')}</span></td>
                <td>{cust.get('vouchers_used_this_month')}/{cust.get('max_voucher_per_month')}</td>
                <td>{cust.get('remaining_voucher_quota_this_month')}</td>
            </tr>
            """
            
        st.markdown(f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Mã KH</th>
                    <th>Tên khách hàng</th>
                    <th>Hạng</th>
                    <th>Voucher Đã dùng/Tối đa</th>
                    <th>Hạn mức còn lại</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
    # TAB 3: Orders Database
    with t_orders:
        st.markdown("#### 📦 Danh sách Đơn hàng giả lập (Mock Orders)")
        
        # Build HTML table for orders
        rows = ""
        for o in data_store.orders_list:
            status_val = o.get("order_status")
            status_badge = "badge-green" if status_val == "completed" else ("badge-blue" if status_val == "delivered" else ("badge-amber" if status_val == "in_transit" else "badge-red"))
            
            returnable_badge = "badge-green" if o.get("can_return_now") else "badge-red"
            returnable_txt = "Có" if o.get("can_return_now") else "Không"
            
            # Extract item summaries
            items_desc = ", ".join([f"{item.get('product_name')} (x{item.get('quantity')})" for item in o.get("items", [])])
            if len(items_desc) > 40:
                items_desc = items_desc[:40] + "..."
                
            rows += f"""
            <tr>
                <td><strong>{o.get('order_id')}</strong></td>
                <td>{o.get('customer_id')}</td>
                <td><span class="badge {status_badge}">{status_val}</span></td>
                <td title="{', '.join([item.get('product_name') for item in o.get('items', [])])}">{items_desc}</td>
                <td>{o.get('shipping_method')}</td>
                <td>{o.get('estimated_delivery')}</td>
                <td><span class="badge {returnable_badge}">{returnable_txt}</span></td>
            </tr>
            """
            
        st.markdown(f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Mã ĐH</th>
                    <th>Mã KH</th>
                    <th>Trạng thái</th>
                    <th>Sản phẩm</th>
                    <th>Vận chuyển</th>
                    <th>Dự kiến giao</th>
                    <th>Có thể trả?</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """, unsafe_allow_html=True)
