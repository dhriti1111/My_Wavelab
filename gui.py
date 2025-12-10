import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="WaveLab",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'custom_eq' not in st.session_state:
    st.session_state.custom_eq = "sin(2*pi*5*t) * exp(-2*t)"

# --- NAVIGATION HELPER ---
def nav_to(page_name):
    st.session_state.page = page_name

# --- THEME CONSTANTS ---
NEON_DARK = {
    "BG": "#101014",
    "PANEL": "#181820",
    "ACCENT": "#C9E819",     # Neon Lime
    "TEXT": "#00FFFF",       # Cyan
    "BTN": "#53C4F1",
    "SIGNAL1": "#B4C6F5",    # Light Blue
    "SIGNAL2": "#F9CC98",    # Light Orange
    "RESULT": "#39FF14",     # Bright Green
    "GRID": "#444455"
}

# --- CSS STYLING ---
st.markdown((
    """
    <style>
    /* Responsive font sizes for titles */
    @media (max-width: 600px) {
        .sidebar-custom-title {
            font-size: 2rem !important;
        }
        .custom-title {
            font-size: 2.5rem !important;
        }
    }
    @media (max-width: 400px) {
        .sidebar-custom-title {
            font-size: 1.3rem !important;
        }
        .custom-title {
            font-size: 1.7rem !important;
        }
    }
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@700&display=swap');

    /* Global Font & Background */
    .stApp {{
        background-color: {bg};
        color: {text};
        font-family: 'Montserrat', sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {panel};
        border-right: 1px solid #333;
    }}

    /* --- SIDEBAR HEADER (NON-STICKY) --- */
    .sidebar-title-container {{
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid {grid};
    }}

    /* Title Styles inside Sidebar */
    .sidebar-custom-title {{
        font-family: 'Exo 2', 'Pacifico', cursive, sans-serif;
        font-size: 3rem;
        background: linear-gradient(90deg, #A259FF 0%, #FF6F91 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        text-shadow: 0 4px 8px rgba(0,0,0,0.5);
        line-height: 1.2;
        margin: 0;
    }}
    
    /* Subtitle Styles inside Sidebar (CYAN) */
    .sidebar-subtitle {{
        font-family: 'Montserrat', sans-serif;
        color: #00FFFF !important; /* Cyan */
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 5px;
        opacity: 1;
    }}

    /* --- SIDEBAR NAVIGATION BUTTONS STYLING --- */
    [data-testid="stSidebar"] div.stButton > button {{
        background-color: transparent;
        border: 1px solid {accent};
        color: {accent};
        border-radius: 8px;
        width: 100%;
        text-align: left;
        padding-left: 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-bottom: 5px;
    }}
    
    [data-testid="stSidebar"] div.stButton > button:hover {{
        background-color: {accent};
        color: {bg};
        border-color: {accent};
        transform: translateX(5px);
        box-shadow: 0 0 10px {accent};
    }}
    
    /* Section Headers in Sidebar */
    .sidebar-header {{
        color: #888;
        font-size: 0.8rem;
        font-weight: bold;
        letter-spacing: 1.5px;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}

    /* Main Page Title Styles */
    .custom-title {{
        font-family: 'Exo 2', 'Pacifico', cursive, sans-serif;
        font-size: 4rem;
        background: linear-gradient(90deg, #A259FF 0%, #FF6F91 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
        margin-bottom: -0.5rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }}
    .custom-subtitle {{
        font-family: sans-serif;
        color: {text};
        opacity: 0.7;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
    
    /* Profile Card */
    .profile-card {{
        background-color: {panel};
        border: 1px solid {accent};
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        transition: transform 0.2s;
        min-height: 320px;
        min-width: 240px;
        max-width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        flex: 1 1 0;
    }}
    .profile-card:hover {{
        transform: scale(1.02);
    }}
    .profile-name {{
        color: {accent};
        font-family: 'Pacifico', cursive;
        font-size: 2rem;
        margin-bottom: 10px;
    }}
    .profile-role {{
        color: {btn};
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 5px;
    }}
    a {{
        color: {btn};
        text-decoration: none;
        margin: 0 5px;
    }}
    
    /* License Footer */
    .license-container {{
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid {grid};
        text-align: center;
        font-size: 0.8rem;
        color: #888;
    }}
    
    div.stButton > button {{
        font-weight: bold;
    }}
    </style>
    """
    .format(
        bg=NEON_DARK['BG'],
        text=NEON_DARK['TEXT'],
        panel=NEON_DARK['PANEL'],
        accent=NEON_DARK['ACCENT'],
        btn=NEON_DARK['BTN'],
        grid=NEON_DARK['GRID']
    )
), unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---

def evaluate_custom_signal(expression, t):
    """Safely evaluates a user string as a numpy expression."""
    allowed_names = {
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
        "pi": np.pi, "np": np, "t": t, "abs": np.abs, 
        "sign": np.sign, "heaviside": np.heaviside
    }
    try:
        result = eval(expression, {"__builtins__": None}, allowed_names)
        if np.isscalar(result):
            result = np.full_like(t, result)
        return result
    except Exception as e:
        return np.zeros_like(t)

def generate_signal(sig_type, t, amp, freq, phase):
    if sig_type == "Custom User Signal":
        return evaluate_custom_signal(st.session_state.custom_eq, t)

    phase_rad = np.deg2rad(phase)
    with np.errstate(divide='ignore', invalid='ignore'):
        if sig_type == "Sine":
            return amp * np.sin(2 * np.pi * freq * t + phase_rad)
        elif sig_type == "Square":
            return amp * np.sign(np.sin(2 * np.pi * freq * t + phase_rad))
        elif sig_type == "Sawtooth":
            return amp * (2 * (freq * t - np.floor(0.5 + freq * t)))
        elif sig_type == "Step":
            return amp * np.heaviside(t, 1)
        elif sig_type == "Impulse":
            arr = np.zeros_like(t)
            idx = np.abs(t).argmin()
            arr[idx] = amp
            return arr
        elif sig_type == "Ramp":
            return amp * t
    return np.zeros_like(t)

# --- OPERATION THEORY ---
OPERATION_THEORY = {
    "Time Scaling": """
    **Time Scaling Theory:**
    Time scaling modifies the "speed" of a signal. Given x(t), the scaled signal is x(at):
    - If a > 1: Signal plays faster (compressed in time)
    - If 0 < a < 1: Signal plays slower (stretched in time)
    """,
    "Amplitude Scaling": """
    **Amplitude Scaling Theory:**
    Amplitude scaling changes the "height" of a signal. Given x(t), the scaled signal is A·x(t):
    - Multiplying by A changes the peak amplitude.
    """,
    "Time Shifting": """
    **Time Shifting Theory:**
    Time shifting delays or advances a signal. Given x(t), the shifted signal is x(t - t₀):
    - If t₀ > 0: Signal is delayed (shifted right)
    - If t₀ < 0: Signal is advanced (shifted left)
    """,
    "Time Reversal": """
    **Time Reversal Theory:**
    Time reversal flips the signal about t = 0. Given x(t), the reversed signal is x(-t).
    """,
    "Signal Addition": """
    **Signal Addition Theory:**
    Adding two signals produces their superposition: y(t) = x₁(t) + x₂(t).
    """,
    "Signal Multiplication": """
    **Signal Multiplication Theory:**
    Multiplying two signals produces modulation: y(t) = x₁(t) · x₂(t).
    """
}

def add_watermark(fig, text="MyWavelab"):
    """Add a faint centered watermark to a Plotly figure."""
    fig.add_annotation(
        text=text,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=50, color="rgba(255,255,255,0.08)", family="Montserrat, sans-serif"),
        align="center"
    )

def create_plotly_chart(t_s1, y_s1, t_s2, y_s2, t_proc, y_proc, op_name, is_discrete, param_val):
    fig = go.Figure()
    hover_temp = "<b>%{text}</b><br>Time: %{x:.2f}<br>Amp: %{y:.2f}<extra></extra>"
    
    # 1. Signal 1
    if is_discrete:
        fig.add_trace(go.Bar(x=t_s1, y=y_s1, name="Signal 1", marker_color=NEON_DARK['SIGNAL1'], text=["Signal 1"] * len(t_s1), hovertemplate=hover_temp))
    else:
        fig.add_trace(go.Scatter(x=t_s1, y=y_s1, name="Signal 1", mode='lines', line=dict(color=NEON_DARK['SIGNAL1'], width=2), text=["Signal 1"] * len(t_s1), hovertemplate=hover_temp))

    # 2. Signal 2
    if y_s2 is not None:
        if is_discrete:
            fig.add_trace(go.Bar(x=t_s2, y=y_s2, name="Signal 2", marker_color=NEON_DARK['SIGNAL2'], text=["Signal 2"] * len(t_s2), hovertemplate=hover_temp))
        else:
            fig.add_trace(go.Scatter(x=t_s2, y=y_s2, name="Signal 2", mode='lines', line=dict(color=NEON_DARK['SIGNAL2'], width=2, dash='dash'), text=["Signal 2"] * len(t_s2), hovertemplate=hover_temp))

    # 3. Processed
    label_proc = "Processed"
    if is_discrete:
        fig.add_trace(go.Bar(x=t_proc, y=y_proc, name=label_proc, marker_color=NEON_DARK['RESULT'], opacity=0.8, text=[label_proc] * len(t_proc), hovertemplate=hover_temp))
    else:
        fig.add_trace(go.Scatter(x=t_proc, y=y_proc, name=label_proc, mode='lines', line=dict(color=NEON_DARK['RESULT'], width=4), text=[label_proc] * len(t_proc), hovertemplate=hover_temp))

    fig.update_layout(
        title=dict(text=f"Operation: {op_name} (Param: {param_val:.2f})" if param_val else op_name, font=dict(color=NEON_DARK['ACCENT'], size=20)),
        paper_bgcolor=NEON_DARK['PANEL'], plot_bgcolor=NEON_DARK['PANEL'], font=dict(color=NEON_DARK['TEXT']),
        xaxis=dict(title="Time (s)", showgrid=True, gridcolor=NEON_DARK['GRID'], zerolinecolor=NEON_DARK['ACCENT']),
        yaxis=dict(title="Amplitude", showgrid=True, gridcolor=NEON_DARK['GRID'], zerolinecolor=NEON_DARK['ACCENT']),
        legend=dict(bgcolor=NEON_DARK['BG'], bordercolor=NEON_DARK['ACCENT'], borderwidth=1),
        hovermode="x unified", dragmode="zoom", height=500, margin=dict(l=40, r=40, t=60, b=40)
    )
    add_watermark(fig)
    return fig

# SIDEBAR STRUCTURE

with st.sidebar:
    # --- HEADER (Sticky) ---
    st.markdown(f"""
    <div class="sidebar-title-container">
        <div class='sidebar-custom-title'>MyWaveLab</div>
        <div class="sidebar-subtitle"><br>Interactive Signal Processing Visualizer</div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- MENU SECTION ---
    if st.session_state.page in ['home', 'custom']:
        st.markdown("<div class='sidebar-header'>Settings</div>", unsafe_allow_html=True)

        if st.button("✏️  Custom Input"):
            nav_to('custom')

        col_mode, col_samp = st.columns([1, 1])
        with col_mode:
            st.write("Mode")
            is_discrete = st.toggle("Discrete", value=False)
        
        with col_samp:
            if is_discrete:
                st.write("Samples")
                num_samples = st.slider("Samples", 10, 200, 50, label_visibility="collapsed")
                t_input = np.linspace(0, 1, num_samples)
            else:
                num_samples = 500
                t_input = np.linspace(0, 1, 500)

# ==============================================================================
# VIEW 1: HOME (VISUALIZER)
# ==============================================================================

if st.session_state.page == 'home':
    # --- MAIN AREA TITLE & SUBTITLE ---
    st.markdown('<div class="custom-title">MyWaveLab</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Interactive Signal Processing Visualizer</div>', unsafe_allow_html=True)

    # --- SPECIFIC CONTROLS (Appended to Sidebar) ---
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>Control Panel</div>", unsafe_allow_html=True)
        
        st.write(" **Signal 1**")
        signal_options = ["Sine", "Square", "Sawtooth", "Step", "Impulse", "Ramp", "Custom User Signal"]
        s1_type = st.selectbox("Signal Type", signal_options, key="s1_type", label_visibility="collapsed")
        
        if s1_type == "Custom User Signal":
            st.caption("Using equation from Custom Input.")
            s1_amp, s1_freq, s1_phase = 1.0, 1.0, 0.0
        else:
            s1_amp = st.slider("Amplitude", 0.1, 5.0, 1.0, 0.1, key="s1_amp")
            s1_freq = st.slider("Freq (Hz)", 0.1, 20.0, 1.0, 0.5, key="s1_freq")
            s1_phase = st.slider("Phase (°)", -180.0, 180.0, 0.0, 10.0, key="s1_phase")

        st.divider()
        st.write(" **Operation**")
        operations_map = {
            "Time Scaling": "x(at)",
            "Amplitude Scaling": "A·x(t)",
            "Time Shifting": "x(t - t₀)",
            "Time Reversal": "x(-t)",
            "Signal Addition": "x₁(t) + x₂(t)",
            "Signal Multiplication": "x₁(t) · x₂(t)"
        }
        operation = st.selectbox("Select Operation", list(operations_map.keys()), label_visibility="collapsed")
        st.latex(operations_map[operation])

        param_val = 1.0
        s2_generated = None
        
        if operation in ["Signal Addition", "Signal Multiplication"]:
            st.markdown("<div class='sidebar-header'>Signal 2</div>", unsafe_allow_html=True)
            s2_type = st.selectbox("Type", ["Sine", "Square", "Sawtooth", "Step", "Impulse", "Ramp"], key="s2_type")
            s2_amp = st.slider("Amp (S2)", 0.1, 5.0, 1.0, 0.1, key="s2_amp")
            s2_freq = st.slider("Freq (S2)", 0.1, 20.0, 1.0, 0.5, key="s2_freq")
            s2_phase = st.slider("Phase (S2)", -180.0, 180.0, 0.0, 10.0, key="s2_phase")
            s2_generated = generate_signal(s2_type, t_input, s2_amp, s2_freq, s2_phase)
        elif operation == "Time Scaling":
            param_val = st.slider("Scaling Factor (a)", 0.1, 5.0, 1.0, 0.1)
        elif operation == "Amplitude Scaling":
            param_val = st.slider("Amplitude Factor (A)", 0.1, 5.0, 1.0, 0.1)
        elif operation == "Time Shifting":
            param_val = st.slider("Shift (t₀)", -5.0, 5.0, 0.0, 0.1)

    # --- CALCULATIONS ---
    s1_generated = generate_signal(s1_type, t_input, s1_amp, s1_freq, s1_phase)
    t_processed = t_input
    s_processed = s1_generated
    p_val_display = 0

    if operation == "Time Shifting":
        t_processed = t_input + param_val
        s_processed = s1_generated
        p_val_display = param_val
    elif operation == "Time Scaling":
        a = param_val
        p_val_display = param_val
        if a > 1e-9:
            t_processed = t_input / a
        else:
            t_processed = t_input
            val_at_zero = generate_signal(s1_type, np.zeros(1), s1_amp, s1_freq, s1_phase)[0]
            s_processed = np.full_like(t_input, val_at_zero)
    elif operation == "Time Reversal":
        t_processed = -t_input
    elif operation == "Amplitude Scaling":
        s_processed = param_val * s1_generated
        p_val_display = param_val
    elif operation == "Signal Addition" and s2_generated is not None:
        s_processed = s1_generated + s2_generated
    elif operation == "Signal Multiplication" and s2_generated is not None:
        s_processed = s1_generated * s2_generated

    # --- MAIN CONTENT ---
    # Top-right About Us button
    col_title, col_about = st.columns([10, 2])
    with col_title:
        st.empty()
    with col_about:
        # Text label for About; widen column for single-line fit
        if st.button("About Us", key="about_btn", help="About Us", use_container_width=True):
            nav_to('about')

    fig = create_plotly_chart(
        t_input, s1_generated, 
        t_input, s2_generated, 
        t_processed, s_processed, 
        operation, is_discrete, p_val_display
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # --- DISPLAY OPERATION THEORY ---
    if operation in OPERATION_THEORY:
        st.markdown(OPERATION_THEORY[operation])

    with st.expander("Show Individual Component Plots"):
        if s2_generated is not None:
            fig2 = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=("Signal 1", "Signal 2", "Result"), vertical_spacing=0.1)
            hover_t = "<b>%{text}</b><br>T: %{x:.2f}<br>Amp: %{y:.2f}<extra></extra>"
            trace1 = go.Bar(x=t_input, y=s1_generated, marker_color=NEON_DARK['SIGNAL1'], text=["S1"]*len(t_input), hovertemplate=hover_t) if is_discrete else go.Scatter(x=t_input, y=s1_generated, line=dict(color=NEON_DARK['SIGNAL1']), text=["S1"]*len(t_input), hovertemplate=hover_t)
            fig2.add_trace(trace1, row=1, col=1)
            trace2 = go.Bar(x=t_input, y=s2_generated, marker_color=NEON_DARK['SIGNAL2'], text=["S2"]*len(t_input), hovertemplate=hover_t) if is_discrete else go.Scatter(x=t_input, y=s2_generated, line=dict(color=NEON_DARK['SIGNAL2']), text=["S2"]*len(t_input), hovertemplate=hover_t)
            fig2.add_trace(trace2, row=2, col=1)
            trace3 = go.Bar(x=t_processed, y=s_processed, marker_color=NEON_DARK['RESULT'], text=["Res"]*len(t_processed), hovertemplate=hover_t) if is_discrete else go.Scatter(x=t_processed, y=s_processed, line=dict(color=NEON_DARK['RESULT']), text=["Res"]*len(t_processed), hovertemplate=hover_t)
            fig2.add_trace(trace3, row=3, col=1)
        else:
            fig2 = make_subplots(rows=2, cols=1, shared_xaxes=False, subplot_titles=("Input Signal", "Output Signal"), vertical_spacing=0.15)
            hover_t = "<b>%{text}</b><br>T: %{x:.2f}<br>Amp: %{y:.2f}<extra></extra>"
            trace1 = go.Bar(x=t_input, y=s1_generated, marker_color=NEON_DARK['SIGNAL1'], text=["In"]*len(t_input), hovertemplate=hover_t) if is_discrete else go.Scatter(x=t_input, y=s1_generated, line=dict(color=NEON_DARK['SIGNAL1']), text=["In"]*len(t_input), hovertemplate=hover_t)
            fig2.add_trace(trace1, row=1, col=1)
            trace2 = go.Bar(x=t_processed, y=s_processed, marker_color=NEON_DARK['RESULT'], text=["Out"]*len(t_processed), hovertemplate=hover_t) if is_discrete else go.Scatter(x=t_processed, y=s_processed, line=dict(color=NEON_DARK['RESULT']), text=["Out"]*len(t_processed), hovertemplate=hover_t)
            fig2.add_trace(trace2, row=2, col=1)

        add_watermark(fig2)
        fig2.update_layout(height=600, paper_bgcolor=NEON_DARK['PANEL'], plot_bgcolor=NEON_DARK['PANEL'], font=dict(color=NEON_DARK['TEXT']), showlegend=False)
        fig2.update_xaxes(showgrid=True, gridcolor=NEON_DARK['GRID'])
        fig2.update_yaxes(showgrid=True, gridcolor=NEON_DARK['GRID'])
        st.plotly_chart(fig2, use_container_width=True)

    # --- FOOTER ---
    st.markdown("""
        <div class="license-container">
            <div class="license-text">
                © 2025 WaveLab Project. All Rights Reserved. Licensed under MIT.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# VIEW 2: CUSTOM INPUT
# ==============================================================================
elif st.session_state.page == 'custom':
    st.markdown('<div class="custom-title">Custom Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Define your own signal equation</div>', unsafe_allow_html=True)

    col_input, col_help = st.columns([2, 1])
    
    with col_input:
        user_text = st.text_area("Enter Equation (function of t)", value=st.session_state.custom_eq, height=150)
        st.session_state.custom_eq = user_text
        
        preview_sig = evaluate_custom_signal(user_text, t_input)
        
        fig_prev = go.Figure()
        hover_t = "<b>%{text}</b><br>T: %{x:.2f}<br>Amp: %{y:.2f}<extra></extra>"
        if is_discrete:
            fig_prev.add_trace(go.Bar(x=t_input, y=preview_sig, marker_color=NEON_DARK['ACCENT'], text=["Custom"]*len(t_input), hovertemplate=hover_t))
        else:
            fig_prev.add_trace(go.Scatter(x=t_input, y=preview_sig, mode='lines', line=dict(color=NEON_DARK['ACCENT'], width=2), text=["Custom"]*len(t_input), hovertemplate=hover_t))
        add_watermark(fig_prev)
        fig_prev.update_layout(
            title="Preview", paper_bgcolor=NEON_DARK['PANEL'], plot_bgcolor=NEON_DARK['PANEL'],
            font=dict(color=NEON_DARK['TEXT']), height=300,
            xaxis=dict(showgrid=True, gridcolor=NEON_DARK['GRID']),
            yaxis=dict(showgrid=True, gridcolor=NEON_DARK['GRID']),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_prev, use_container_width=True)
        
        st.success("✅ Equation saved! Go to the **Visualizer** and select **'Custom User Signal'** to use it.")
        
        if st.button("⬅ Back to Visualizer"):
            nav_to('home')

    with col_help:
        st.info("💡 **Syntax Guide**")
        st.markdown("""
        **Variables:** `t`, `pi`
        
        **Functions:**
        - `sin(x)`, `cos(x)`, `tan(x)`
        - `exp(x)`, `log(x)`, `sqrt(x)`
        - `abs(x)`, `sign(x)`
        - `heaviside(x, 1)`
        
        **Examples:**
        1. `sin(2*pi*t)`
        2. `exp(-2*t) * cos(10*t)`
        """)

# ==============================================================================
# VIEW 3: ABOUT US
# ==============================================================================
elif st.session_state.page == 'about':
    if st.button("⬅ Back to Visualizer"):
        nav_to('home')
    
    st.markdown('<div class="custom-title">Meet the Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">The Minds behind MyWaveLab</div>', unsafe_allow_html=True)

    team = [
        {
            "name": "Dhriti Manpurkar",
            "branch": "E&TC",
            "domain": "Interface Alchemist",
            "linkedin": "https://www.linkedin.com/in/dhriti-manpurkar-003ab0339/",
            "github": "https://github.com/dhriti1111",
            "email": "dhriti.manpurkar11@gmail.com"
        },
        {
            "name": "Revanth Sai Sreerangam",
            "branch": "E&TC",
            "domain": "Backend Brainiac",
            "linkedin": "https://www.linkedin.com/in/revanth-sai-sreerangam-74516421a/",
            "github": "https://github.com/REvaNTH-404",
            "email": "revanthsai.work@gmail.com"
        }
    ]

    cols = st.columns(len(team))
    for i, member in enumerate(team):
        with cols[i]:
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-name">{member['name']}</div>
                <div class="profile-role">{member['branch']}</div>
                <div style="color: {NEON_DARK['TEXT']}; font-size: 0.9rem; margin-bottom: 10px;">{member['domain']}</div>
                <div class="profile-links">
                    <a href="{member['linkedin']}">LinkedIn</a>
                    <a href="{member['github']}">GitHub</a>
                    <a href="{member['email']}">Email</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Disclaimer below member boxes
    st.markdown("""
    <div style='margin-top:32px; text-align:center; color:#aaa; font-size:0.95rem;'>
        <b>Disclaimer:</b> MyWavelab is an educational tool for learning and visualizing signal processing concepts. Results and visualizations are for academic purposes only and by using the app, users acknowledge that all outputs are for informational and experimental purposes only.
    """, unsafe_allow_html=True)