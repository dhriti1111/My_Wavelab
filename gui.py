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
st.markdown(f"""
    <style>
    /* Import Handwriting Font (Pacifico) */
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

    /* Main Background */
    .stApp {{
        background-color: {NEON_DARK['BG']};
        color: {NEON_DARK['TEXT']};
    }}
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: {NEON_DARK['PANEL']};
        border-right: 1px solid #333;
    }}
    
    /* Custom Title Style */
    .custom-title {{
        font-family: 'Pacifico', cursive;
        font-size: 4.5rem;
        color: {NEON_DARK['ACCENT']};
        margin-bottom: -1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }}
    
    .custom-subtitle {{
        font-family: sans-serif;
        color: {NEON_DARK['TEXT']};
        opacity: 0.7;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}

    /* About Us Card Style */
    .profile-card {{
        background-color: {NEON_DARK['PANEL']};
        border: 1px solid {NEON_DARK['ACCENT']};
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}
    .profile-name {{
        color: {NEON_DARK['ACCENT']};
        font-family: 'Pacifico', cursive;
        font-size: 2rem;
        margin-bottom: 10px;
    }}
    .profile-role {{
        color: {NEON_DARK['BTN']};
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 5px;
    }}
    .profile-text {{
        color: {NEON_DARK['TEXT']};
        opacity: 0.9;
    }}
    a {{
        color: {NEON_DARK['BTN']};
        text-decoration: none;
    }}
    a:hover {{
        color: {NEON_DARK['ACCENT']};
        text-decoration: underline;
    }}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {NEON_DARK['PANEL']};
        border-radius: 4px;
        color: {NEON_DARK['TEXT']};
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {NEON_DARK['ACCENT']} !important;
        color: {NEON_DARK['BG']} !important;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---

def generate_signal(sig_type, t, amp, freq, phase):
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
        hovermode="x unified", dragmode="zoom", height=550, margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

# --- MAIN APP LAYOUT ---

# Define Tabs at the very top
tab_home, tab_about = st.tabs(["Signal Visualizer", "About Us"])

# --- SIDEBAR (Global Controls) ---
with st.sidebar:
    st.markdown(f"<div class='custom-title' style='font-size:2.5rem;'>WaveLab</div>", unsafe_allow_html=True)
    
    st.header("Time Settings")
    col_mode, col_samp = st.columns([1, 1.5])
    with col_mode:
        is_discrete = st.toggle("Discrete Time", value=False)
    
    if is_discrete:
        num_samples = st.slider("Samples", 10, 200, 50)
        t_input = np.linspace(0, 1, num_samples)
    else:
        num_samples = 500
        t_input = np.linspace(0, 1, 500)

    st.divider()
    st.header("Signal 1")
    s1_type = st.selectbox("Type", ["Sine", "Square", "Sawtooth", "Step", "Impulse", "Ramp"], key="s1_type")
    
    col1, col2 = st.columns(2)
    with col1:
        s1_amp = st.number_input("Amplitude", 0.1, 10.0, 1.0, 0.1, key="s1_amp")
        s1_freq = st.number_input("Freq (Hz)", 0.1, 50.0, 1.0, 0.5, key="s1_freq")
    with col2:
        s1_phase = st.number_input("Phase (°)", -360.0, 360.0, 0.0, 10.0, key="s1_phase")

    st.divider()
    st.header("Operation")
    operations_map = {
        "Time Scaling": "x(at)",
        "Amplitude Scaling": "A·x(t)",
        "Time Shifting": "x(t - t₀)",
        "Time Reversal": "x(-t)",
        "Signal Addition": "x₁(t) + x₂(t)",
        "Signal Multiplication": "x₁(t) · x₂(t)"
    }
    operation = st.selectbox("Select Operation", list(operations_map.keys()))
    st.latex(operations_map[operation])

    param_val = 1.0
    s2_generated = None
    
    if operation in ["Signal Addition", "Signal Multiplication"]:
        st.subheader("Signal 2")
        s2_type = st.selectbox("Type", ["Sine", "Square", "Sawtooth", "Step", "Impulse", "Ramp"], key="s2_type")
        c2_1, c2_2 = st.columns(2)
        with c2_1:
            s2_amp = st.number_input("Amplitude", 0.1, 10.0, 1.0, 0.1, key="s2_amp")
            s2_freq = st.number_input("Freq (Hz)", 0.1, 50.0, 1.0, 0.5, key="s2_freq")
        with c2_2:
            s2_phase = st.number_input("Phase (°)", -360.0, 360.0, 0.0, 10.0, key="s2_phase")
        s2_generated = generate_signal(s2_type, t_input, s2_amp, s2_freq, s2_phase)
    elif operation == "Time Scaling":
        param_val = st.slider("Scaling Factor (a)", 0.1, 5.0, 1.0, 0.1)
    elif operation == "Amplitude Scaling":
        param_val = st.slider("Amplitude Factor (A)", 0.1, 5.0, 1.0, 0.1)
    elif operation == "Time Shifting":
        param_val = st.slider("Shift (t₀)", -5.0, 5.0, 0.0, 0.1)

# --- PROCESSING (Calculations) ---
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

# --- TAB 1: VISUALIZER ---
with tab_home:
    st.markdown('<div class="custom-title">WaveLab</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">Interactive Signal Processing Visualizer</div>', unsafe_allow_html=True)

    # Main Plot
    fig = create_plotly_chart(
        t_input, s1_generated, 
        t_input, s2_generated, 
        t_processed, s_processed, 
        operation, is_discrete, p_val_display
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed View
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

        fig2.update_layout(height=600, paper_bgcolor=NEON_DARK['PANEL'], plot_bgcolor=NEON_DARK['PANEL'], font=dict(color=NEON_DARK['TEXT']), showlegend=False)
        fig2.update_xaxes(showgrid=True, gridcolor=NEON_DARK['GRID'])
        fig2.update_yaxes(showgrid=True, gridcolor=NEON_DARK['GRID'])
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: ABOUT US ---
with tab_about:
    st.markdown('<div class="custom-title">Meet the Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">The minds behind WaveLab</div>', unsafe_allow_html=True)

    # --- EDIT YOUR DETAILS HERE ---
    team = [
        {
            "name": "Member Name 1",
            "branch": "Electronics & Comm. Engineering",
            "domain": "Signal Processing & Python",
            "linkedin": "#",
            "github": "#",
            "email": "mailto:email@example.com"
        },
        {
            "name": "Member Name 2",
            "branch": "Computer Science Engineering",
            "domain": "Frontend & Visualization",
            "linkedin": "#",
            "github": "#",
            "email": "mailto:email@example.com"
        }
    ]
    # ------------------------------

    # Create Columns for the cards
    cols = st.columns(len(team))

    for i, member in enumerate(team):
        with cols[i]:
            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-name">{member['name']}</div>
                <div class="profile-role">{member['branch']}</div>
                <div class="profile-text"><b>Domain:</b> {member['domain']}</div>
                <br>
                <div class="profile-text">
                    <a href="{member['linkedin']}">LinkedIn</a> &nbsp;|&nbsp; 
                    <a href="{member['github']}">GitHub</a> &nbsp;|&nbsp; 
                    <a href="{member['email']}">Email</a>
                </div>
            </div>
            """, unsafe_allow_html=True)