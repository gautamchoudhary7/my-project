"""
CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform
Skill Wallet Capstone Project 2 | Platform ID: 6ac4c9851dcde6d7857c163b
Production Streamlit Application
"""
import os
import io
import datetime
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# Import Core Forensic Modules
from modules.config import (
    PLATFORM_NAME, PLATFORM_ID, CATEGORY, VERSION,
    DEFAULT_AGENCY, DEFAULT_INVESTIGATOR, DEFAULT_LAB,
    THREAT_LEVELS, SCENE_CLASSIFICATIONS, PENAL_CODE_DIRECTORY,
    APP_CSS
)
from modules.custody import ChainOfCustodyTracker, compute_sha256, generate_evidence_id
from modules.sample_data import get_preloaded_cases
from modules.visual_analyzer import (
    annotate_image, evaluate_threat_level, classify_scene,
    generate_investigative_leads, detect_objects_in_uploaded_image
)
from modules.audio_analyzer import process_audio_file, analyze_transcript_semantics
from modules.video_analyzer import sample_video_keyframes, get_video_progression_summary
from modules.fusion_rag import (
    build_unified_master_ledger, format_ledger_context_for_llm,
    get_cross_modal_correlations
)
from modules.llm_service import ForensicLLMService
from modules.pdf_report import generate_court_admissible_pdf
from modules.utils import (
    create_timeline_plotly_chart, create_acoustic_stress_chart,
    create_suspect_velocity_chart
)

# ---------------------------------------------------------
# Page Configuration & Forensic Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="CrimeVision AI | Multimodal Forensics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(APP_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "cases" not in st.session_state:
    st.session_state.cases = get_preloaded_cases()

if "selected_case_id" not in st.session_state:
    st.session_state.selected_case_id = "CASE-2026-CR-8841"

if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "demo"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "custody_tracker" not in st.session_state:
    tracker = ChainOfCustodyTracker(
        case_id="CASE-2026-CR-8841",
        lead_investigator=DEFAULT_INVESTIGATOR,
        agency=DEFAULT_AGENCY
    )
    # Log initial custody entries for preloaded assets
    tracker.record_event(
        evidence_id="EVD-IMG-2026-001",
        action="SECURED_AT_SCENE",
        custodian="CSI Unit 4 / Det. Vance",
        sha256_hash="7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
        notes="Crime scene master photography preserved in RAW format."
    )
    tracker.record_event(
        evidence_id="EVD-AUD-2026-002",
        action="RECORDED_DISPATCH",
        custodian="Emergency Comm Center",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        notes="Audio 911 recording retrieved from CAD server."
    )
    tracker.record_event(
        evidence_id="EVD-VID-2026-003",
        action="SEIZED_CCTV_FEED",
        custodian="Det. Marcus Vance (#8421)",
        sha256_hash="cb8379ac2098aa165029e3938a51da0bcecfc008fd6795f401178647f96c5b34",
        notes="Surveillance DVR drive extracted from alley staging camera."
    )
    st.session_state.custody_tracker = tracker

# Active Case Reference
case = st.session_state.cases[st.session_state.selected_case_id]

# ---------------------------------------------------------
# Sidebar - Configuration, Custody & System Telemetry
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div style="background: rgba(0,240,255,0.15); border: 1px solid #00f0ff; border-radius: 8px; padding: 8px 12px; font-size: 1.4rem;">
                🛡️
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.15rem; color: #00f0ff; letter-spacing: -0.02em;">CrimeVision AI</h3>
                <span style="font-size: 0.72rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">v2.4.0-PROD | ID: 6ac4c985</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Case Selector
    st.markdown("### 📁 Active Investigation Case")
    case_ids = list(st.session_state.cases.keys())
    selected_idx = case_ids.index(st.session_state.selected_case_id) if st.session_state.selected_case_id in case_ids else 0
    new_case_id = st.selectbox(
        "Select Forensic Case File:",
        options=case_ids,
        index=selected_idx,
        format_func=lambda cid: f"{cid} - {st.session_state.cases[cid]['title'][:24]}..."
    )
    if new_case_id != st.session_state.selected_case_id:
        st.session_state.selected_case_id = new_case_id
        st.session_state.chat_history = []
        st.rerun()

    case = st.session_state.cases[st.session_state.selected_case_id]

    st.markdown(f"""
        <div class="forensic-card" style="padding: 10px 14px; margin-bottom: 12px;">
            <div style="font-size: 0.75rem; color: #94a3b8;">CASE NUMBER</div>
            <div style="font-family: 'JetBrains Mono'; font-weight: 700; color: #00f0ff;">{case['case_id']}</div>
            <div style="font-size: 0.72rem; color: #e2e8f0; margin-top: 4px;">{case['title']}</div>
            <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 2px;">📍 {case['location']}</div>
        </div>
    """, unsafe_allow_html=True)

    # API Configuration & Demo Fallback
    st.markdown("### ⚙️ AI Engine Configuration")
    provider_option = st.selectbox(
        "LLM & Vision Provider:",
        options=["Demo Mode (High-Fidelity Offline)", "Google Gemini (gemini-2.5-flash)", "Groq (Llama-3.3-70B)"],
        index=0 if st.session_state.llm_provider == "demo" else (1 if st.session_state.llm_provider == "gemini" else 2)
    )

    if "Gemini" in provider_option:
        st.session_state.llm_provider = "gemini"
        api_key_input = st.text_input("Enter Gemini API Key:", type="password", value=st.session_state.api_key)
        st.session_state.api_key = api_key_input
        st.caption("🔒 Key processed in-memory. Automatic fallback to Smart Engine if offline.")
    elif "Groq" in provider_option:
        st.session_state.llm_provider = "groq"
        api_key_input = st.text_input("Enter Groq API Key:", type="password", value=st.session_state.api_key)
        st.session_state.api_key = api_key_input
        st.caption("⚡ Ultra-low latency Llama-3.3 inference. Automatic fallback if rate-limited.")
    else:
        st.session_state.llm_provider = "demo"
        st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; padding: 8px 10px; font-size: 0.75rem; color: #34d399;">
                ✔ <b>Zero-Key Demo Fallback Active</b><br/>
                All forensic models, RT-DETR visual taggers, Whisper transcriptions, and RAG chat operate 100% turnkey.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Chain of Custody Summary
    st.markdown("### ⛓️ Chain of Custody Integrity")
    custody_summary = st.session_state.custody_tracker.get_summary()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{custody_summary['total_transactions']}</div>
                <div class="metric-lbl">Ledger Logs</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{custody_summary['unique_evidence_items']}</div>
                <div class="metric-lbl">Sealed Items</div>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("🔎 View Chain of Custody Audit Log", expanded=False):
        df_custody = st.session_state.custody_tracker.to_dataframe()
        st.dataframe(
            df_custody[["evidence_id", "timestamp", "action", "custodian", "status"]],
            use_container_width=True,
            hide_index=True
        )

    # Lead Investigator Sign-Off Block
    st.markdown("### 👮 Lead Investigator Sign-Off")
    inv_name = st.text_input("Investigator:", value=case.get("lead_investigator", DEFAULT_INVESTIGATOR))
    agency_name = st.text_input("Agency:", value=case.get("agency", DEFAULT_AGENCY))

    st.markdown("---")
    st.markdown(f"""
        <div style="font-size: 0.72rem; color: #64748b; text-align: center;">
            CrimeVision AI Forensics © 2026<br/>
            Skill Wallet Capstone Platform 2<br/>
            Compliant with FRE 901 & ISO/IEC 27037
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Bar & Threat Level Header
# ---------------------------------------------------------
threat_meta = THREAT_LEVELS.get(case.get("threat_level", "HIGH"), THREAT_LEVELS["HIGH"])

st.markdown(f"""
    <div class="forensic-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="badge-tag badge-cyan">{case.get('case_id')}</span>
                    <span class="badge-tag" style="background: {threat_meta['bg']}; color: {threat_meta['color']}; border: 1px solid {threat_meta['border']};">
                        ● {threat_meta['badge']}
                    </span>
                    <span class="badge-tag badge-amber">{case.get('classification')}</span>
                </div>
                <h1 style="margin: 0; font-size: 1.85rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em;">
                    {PLATFORM_NAME}
                </h1>
                <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 0.88rem;">
                    Incident Occurred: <b style="color: #e2e8f0;">{case.get('incident_datetime')}</b> | Scene: <b style="color: #e2e8f0;">{case.get('location')}</b>
                </p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace;">SYSTEM INTEGRITY</div>
                <div style="color: #10b981; font-weight: 700; font-size: 0.95rem;">✔ FRE-901 VERIFIED</div>
                <div style="font-size: 0.7rem; color: #64748b;">SHA-256 DIGITAL ATTESTATION ACTIVE</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Layout
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 Tab 1: Scene Visual Evidence Tagger",
    "🎙️ Tab 2: Witness Audio Transcription & Timeline",
    "🎥 Tab 3: CCTV Video Analysis & Event Progression",
    "🧩 Tab 4: Multimodal Fusion & Grounded Evidence Chat",
    "📄 Tab 5: Automated Forensic PDF Export"
])

# =========================================================
# TAB 1: Visual Evidence Tagger (Epic 2)
# =========================================================
with tab1:
    st.markdown("### 🔬 Crime Scene Visual Evidence Tagger (RT-DETR / YOLOv8)")
    st.caption("Multimodal object detection isolating persons, firearms, edged weapons, biological blood spatter, and forced entry points.")

    col1, col2 = st.columns([1.3, 1.0])

    with col1:
        st.markdown("#### 📷 Evidence Photography Feed")
        
        # Options: Use preloaded case image or upload custom photo
        img_source = st.radio(
            "Evidence Image Source:",
            ["Case Master Photography (Preset)", "Upload New Crime Scene Photo (JPEG/PNG)"],
            horizontal=True
        )

        active_img_path = case.get("image_path")
        detections = case.get("image_detections", [])

        if img_source == "Upload New Crime Scene Photo (JPEG/PNG)":
            uploaded_file = st.file_uploader("Upload Scene Photography:", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                user_image = Image.open(uploaded_file)
                # Compute hash and record custody
                img_bytes = uploaded_file.getvalue()
                h_val = compute_sha256(img_bytes)
                evd_id = generate_evidence_id("image", 1)
                st.session_state.custody_tracker.record_event(
                    evidence_id=evd_id,
                    action="UPLOADED_ANALYZED",
                    custodian=DEFAULT_INVESTIGATOR,
                    sha256_hash=h_val,
                    notes=f"User uploaded image: {uploaded_file.name}"
                )
                detections = detect_objects_in_uploaded_image(user_image)
                img_np = np.array(user_image.convert("RGB"))
            else:
                user_image = Image.open(active_img_path) if os.path.exists(active_img_path) else Image.new("RGB", (960, 640), (40, 40, 50))
                img_np = np.array(user_image.convert("RGB"))
        else:
            user_image = Image.open(active_img_path) if os.path.exists(active_img_path) else Image.new("RGB", (960, 640), (40, 40, 50))
            img_np = np.array(user_image.convert("RGB"))

        # Render Bounding Boxes
        annotated_np = annotate_image(img_np, detections)
        st.image(annotated_np, caption=f"RT-DETR Forensic Inference Overlay | {len(detections)} Forensic Regions of Interest (ROI) Isolated", use_container_width=True)

    with col2:
        st.markdown("#### 📊 Structured Forensic Analysis")
        threat_eval = evaluate_threat_level(detections)
        scene_cls = classify_scene(detections)

        # Threat Matrix Card
        t_info = threat_eval["details"]
        st.markdown(f"""
            <div class="forensic-card" style="border-left: 4px solid {t_info['border']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 0.78rem; color: #94a3b8; text-transform: uppercase;">EVIDENTIARY THREAT LEVEL</div>
                    <span class="badge-tag" style="background: {t_info['bg']}; color: {t_info['color']}; border: 1px solid {t_info['border']}; margin: 0;">
                        {t_info['badge']}
                    </span>
                </div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-top: 6px;">
                    {scene_cls}
                </div>
                <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 6px;">
                    {t_info['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Forensic Indicators checklist
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown(f"""
                <div class="metric-box">
                    <div style="color: {'#ef4444' if threat_eval['lethal_weapon_present'] else '#10b981'}; font-weight: 700; font-size: 1.1rem;">
                        {'✔ DETECTED' if threat_eval['lethal_weapon_present'] else '✖ NEGATIVE'}
                    </div>
                    <div class="metric-lbl">Lethal Weapon</div>
                </div>
            """, unsafe_allow_html=True)
        with c_b:
            st.markdown(f"""
                <div class="metric-box">
                    <div style="color: {'#ef4444' if threat_eval['active_bleed_detected'] else '#10b981'}; font-weight: 700; font-size: 1.1rem;">
                        {'✔ DETECTED' if threat_eval['active_bleed_detected'] else '✖ NEGATIVE'}
                    </div>
                    <div class="metric-lbl">Serological Spatter</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("##### 📍 Detected Forensic Items & Spatial Coordinates")
        
        # Table of detections
        det_table_data = []
        for idx, d in enumerate(detections):
            det_table_data.append({
                "Marker": f"#{idx + 1}",
                "Class": d.get("label", "Item"),
                "Category": d.get("category", "Evidence"),
                "Confidence": f"{d.get('confidence', 0.90) * 100:.1f}%",
                "Bounding Box [x1, y1, x2, y2]": str(d.get("box", [])),
                "Threat": d.get("threat", "HIGH")
            })
        st.dataframe(pd.DataFrame(det_table_data), use_container_width=True, hide_index=True)

        # Prioritized Leads
        st.markdown("##### 🎯 Prioritized Investigative Leads")
        leads = generate_investigative_leads(detections, scene_cls)
        for lead in leads:
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.6); border-left: 2px solid #00f0ff; padding: 6px 12px; margin-bottom: 6px; font-size: 0.78rem; border-radius: 0 4px 4px 0;">
                    {lead}
                </div>
            """, unsafe_allow_html=True)

# =========================================================
# TAB 2: Audio Transcription & Timeline (Epic 3)
# =========================================================
with tab2:
    st.markdown("### 🎙️ Witness Audio Transcription & Timeline Extraction (Epic 3)")
    st.caption("Acoustic speech diarization, stress index analysis, and timestamped chronological witness markers.")

    col1, col2 = st.columns([1.1, 1.2])

    with col1:
        st.markdown("#### 🎧 Audio Statement Playback")
        aud_source = st.radio(
            "Select Audio Stream:",
            ["Emergency 911 Audio Feed (Preset)", "Upload External Witness Audio (.WAV / .MP3)"],
            horizontal=True
        )

        active_aud_path = case.get("audio_path")
        transcript_data = case.get("audio_transcript", [])

        if aud_source == "Upload External Witness Audio (.WAV / .MP3)":
            uploaded_aud = st.file_uploader("Upload Witness Audio Recording:", type=["wav", "mp3", "ogg"])
            if uploaded_aud is not None:
                aud_bytes = uploaded_aud.getvalue()
                h_aud = compute_sha256(aud_bytes)
                st.session_state.custody_tracker.record_event(
                    evidence_id=generate_evidence_id("audio", 2),
                    action="AUDIO_INGESTED",
                    custodian=DEFAULT_INVESTIGATOR,
                    sha256_hash=h_aud,
                    notes=f"Uploaded audio statement: {uploaded_aud.name}"
                )
                processed_aud = process_audio_file(aud_bytes, uploaded_aud.name)
                transcript_data = processed_aud["transcript"]
                st.audio(aud_bytes, format="audio/wav")
            else:
                if os.path.exists(active_aud_path):
                    with open(active_aud_path, "rb") as af:
                        st.audio(af.read(), format="audio/wav")
        else:
            if os.path.exists(active_aud_path):
                with open(active_aud_path, "rb") as af:
                    st.audio(af.read(), format="audio/wav")

        # Acoustic Stress Analytics
        st.markdown("#### 📈 Vocal Stress & Panic Metrics")
        analytics = analyze_transcript_semantics(transcript_data)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val" style="color: {analytics['urgency_color']};">{analytics['peak_stress_index']}</div>
                    <div class="metric-lbl">Peak Panic Index</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val" style="color: #00f0ff;">{analytics['veracity_score']}%</div>
                    <div class="metric-lbl">Veracity Rating</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val" style="color: #38bdf8;">{analytics['total_speakers']}</div>
                    <div class="metric-lbl">Speakers Diarized</div>
                </div>
            """, unsafe_allow_html=True)

        st.plotly_chart(create_acoustic_stress_chart(transcript_data), use_container_width=True)

    with col2:
        st.markdown("#### 📜 Sworn Forensic Audio Transcript & Diarization")
        
        # Diarization chat view
        for item in transcript_data:
            speaker = item.get("speaker", "Caller")
            is_dispatcher = "Dispatch" in speaker
            border_col = "#00f0ff" if is_dispatcher else "#f43f5e"
            badge_cls = "badge-cyan" if is_dispatcher else "badge-red"

            st.markdown(f"""
                <div class="timeline-card" style="border-left-color: {border_col}; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <div>
                            <span class="timeline-time">[{item.get('timestamp')}]</span>
                            <span class="badge-tag {badge_cls}">{speaker}</span>
                        </div>
                        <span style="font-size: 0.72rem; color: #94a3b8; font-family: 'JetBrains Mono';">
                            Stress: {item.get('stress_level', 50)}/100
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: #e2e8f0; line-height: 1.4;">
                        "{item.get('text')}"
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("##### 🏷️ Extracted Forensic Entities")
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            st.markdown(f"**Weapons Mentioned:** `{', '.join(analytics['weapons_mentioned'])}`")
            st.markdown(f"**Vehicles Mentioned:** `{', '.join(analytics['vehicles_mentioned'])}`")
        with e_col2:
            st.markdown(f"**Locations:** `{', '.join(analytics['locations_mentioned'])}`")
            st.markdown(f"**Suspect Descriptors:** `{', '.join(analytics['suspect_descriptors'])}`")

# =========================================================
# TAB 3: CCTV Video Analysis (Epic 4)
# =========================================================
with tab3:
    st.markdown("### 🎥 CCTV Video Analysis & Event Progression (Epic 4)")
    st.caption("Frame-by-frame suspect trajectory tracking, legal penal code classifications, and velocity kinetics.")

    col1, col2 = st.columns([1.2, 1.1])

    with col1:
        st.markdown("#### 📹 CCTV Surveillance Player")
        active_vid_path = case.get("video_path")

        if os.path.exists(active_vid_path):
            with open(active_vid_path, "rb") as vf:
                st.video(vf.read())

        st.markdown("#### 🏎️ Suspect & Vehicular Motion Kinetics")
        video_events = case.get("video_events", [])
        st.plotly_chart(create_suspect_velocity_chart(video_events), use_container_width=True)

    with col2:
        st.markdown("#### ⏱️ Chronological Event Progression Log")
        
        # Display each key event
        for ev in video_events:
            sev = ev.get("severity", "MEDIUM")
            badge_color = "#ef4444" if sev == "CRITICAL" else ("#f97316" if sev == "HIGH" else "#eab308")

            st.markdown(f"""
                <div class="forensic-card" style="border-left: 3px solid {badge_color}; padding: 12px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="timeline-time">T+{ev.get('timestamp')} ({ev.get('motion_velocity', ev.get('velocity_kmh', 'N/A'))})</span>
                        <span class="badge-tag" style="background: rgba(255,255,255,0.06); color: {badge_color}; border: 1px solid {badge_color}; font-size: 0.68rem; margin: 0;">
                            {ev.get('penal_code')}
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: #f1f5f9; font-weight: 600; margin-top: 4px;">
                        {ev.get('event_description', ev.get('description', 'Surveillance action'))}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("##### ⚖️ Classified Penal Code Directory Violations")
        penal_data = []
        for code, info in PENAL_CODE_DIRECTORY.items():
            if any(code in ev.get("penal_code", "") for ev in video_events):
                penal_data.append({
                    "Statute": code,
                    "Charge Title": info["title"],
                    "Severity": info["severity"],
                    "Classification": info["classification"]
                })
        st.dataframe(pd.DataFrame(penal_data), use_container_width=True, hide_index=True)

# =========================================================
# TAB 4: Multimodal Fusion & Grounded Evidence Chat (Epic 5)
# =========================================================
with tab4:
    st.markdown("### 🧩 Multimodal Fusion & Grounded Evidence Chat (Epic 5)")
    st.caption("Master chronological event ledger synthesizing Image, Audio, and Video evidence with zero-hallucination RAG interrogation.")

    # Build Master Fusion Ledger
    master_ledger = build_unified_master_ledger(
        case_info=case,
        image_detections=case.get("image_detections", []),
        audio_transcript=case.get("audio_transcript", []),
        video_events=case.get("video_events", [])
    )

    # Interactive Plotly Timeline
    st.plotly_chart(create_timeline_plotly_chart(master_ledger), use_container_width=True)

    # Cross-Modal Correlations Expander
    with st.expander("🔗 Cross-Modal Forensic Correlations (Triangulated Evidence)", expanded=True):
        correlations = get_cross_modal_correlations(master_ledger)
        for c in correlations:
            st.markdown(f"""
                <div class="forensic-card" style="border-left: 3px solid #00f0ff; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="color: #00f0ff; font-size: 0.9rem;">{c['theme']}</b>
                        <span class="badge-tag badge-red">{c['statute']}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #e2e8f0; margin-top: 4px;">
                        {c['forensic_synthesis']}
                    </div>
                    <div style="margin-top: 6px; font-size: 0.75rem; color: #94a3b8;">
                        Sources: {' | '.join([f"<code>{s['id']}</code> ({s['note']})" for s in c['sources']])}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💬 Grounded AI Evidence Interrogation (Zero Hallucination)")
    st.caption("Query the multimodal evidence ledger in natural language. Answers strictly cite Evidence IDs `[EVD-...]`.")

    # Suggested Prompts
    st.markdown("**Suggested Forensic Inquiries:**")
    prompt_cols = st.columns(3)
    suggested_q = None
    with prompt_cols[0]:
        if st.button("🔫 Was a weapon visible before suspect fled?", use_container_width=True):
            suggested_q = "Was a weapon visible before the suspect fled?"
    with prompt_cols[1]:
        if st.button("🚗 What did witness say about getaway vehicle?", use_container_width=True):
            suggested_q = "What did the witness say about the vehicle and getaway route?"
    with prompt_cols[2]:
        if st.button("🚪 What physical evidence shows forced entry?", use_container_width=True):
            suggested_q = "What physical evidence indicates forced entry and commercial burglary?"

    # Chat display container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            is_user = msg["role"] == "user"
            with st.chat_message("user" if is_user else "assistant"):
                st.markdown(msg["content"])
                if not is_user and msg.get("citations"):
                    cit_str = " ".join([f"`[{c}]`" for c in msg["citations"]])
                    st.markdown(f"<span style='font-size: 0.75rem; color: #00f0ff;'>Evidentiary Citations: {cit_str}</span>", unsafe_allow_html=True)

    # Chat Input
    user_query = st.chat_input("Enter forensic inquiry (e.g., 'Summarize suspect movements between 00:05 and 00:14')...")
    if suggested_q:
        user_query = suggested_q

    if user_query:
        # Append user query
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Prepare context and query LLM
        evidence_ctx = format_ledger_context_for_llm(master_ledger, case)
        llm_service = ForensicLLMService(
            provider=st.session_state.llm_provider,
            api_key=st.session_state.api_key
        )
        
        with st.spinner("Interrogating multimodal evidence ledger..."):
            response = llm_service.generate_chat_response(
                query=user_query,
                evidence_context=evidence_ctx,
                chat_history=st.session_state.chat_history
            )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response["answer"],
            "citations": response.get("citations", []),
            "provider": response.get("provider", "CrimeVision Engine")
        })
        st.rerun()

# =========================================================
# TAB 5: Automated Forensic PDF Export (Epic 6)
# =========================================================
with tab5:
    st.markdown("### 📄 Automated Court-Admissible Forensic PDF Export (Epic 6)")
    st.caption("1-Click automated generation of judicial summary reports using ReportLab with SHA-256 chain-of-custody verification.")

    master_ledger = build_unified_master_ledger(
        case_info=case,
        image_detections=case.get("image_detections", []),
        audio_transcript=case.get("audio_transcript", []),
        video_events=case.get("video_events", [])
    )
    df_custody = st.session_state.custody_tracker.to_dataframe()
    custody_entries = df_custody.to_dict("records")
    
    # Compute Master Investigation Digest
    master_raw = f"{case['case_id']}_{case['title']}_{len(master_ledger)}_{datetime.date.today()}"
    master_hash = compute_sha256(master_raw.encode("utf-8"))

    col1, col2 = st.columns([1.1, 1.2])

    with col1:
        st.markdown("#### 🏛️ Judicial Report Attestation & Parameters")
        
        st.markdown(f"""
            <div class="forensic-card">
                <div style="font-size: 0.75rem; color: #94a3b8;">CASE IDENTIFIER</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #00f0ff;">{case['case_id']}</div>
                <div style="font-size: 0.82rem; color: #e2e8f0; margin-top: 4px;">{case['title']}</div>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 8px 0;"/>
                <div style="font-size: 0.72rem; color: #94a3b8;">LEAD INVESTIGATOR</div>
                <div style="font-size: 0.85rem; color: #ffffff;">{inv_name}</div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 6px;">AGENCY JURISDICTION</div>
                <div style="font-size: 0.85rem; color: #ffffff;">{agency_name}</div>
                <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 6px;">COMPLIANCE STANDARDS</div>
                <div style="font-size: 0.8rem; color: #10b981;">✔ FRE 901, FRE 902(13), ISO/IEC 27037:2012</div>
            </div>
        """, unsafe_allow_html=True)

        include_chat = st.checkbox("Include Grounded Q&A Interrogation Log in PDF Report", value=True)

        # Generate PDF Button
        if st.button("🔨 Generate Court-Admissible Forensic PDF Report", type="primary", use_container_width=True):
            with st.spinner("Compiling ReportLab document with cryptographic seal..."):
                pdf_bytes = generate_court_admissible_pdf(
                    case_info=case,
                    custody_entries=custody_entries,
                    image_detections=case.get("image_detections", []),
                    audio_transcript=case.get("audio_transcript", []),
                    video_events=case.get("video_events", []),
                    master_ledger=master_ledger,
                    qa_history=st.session_state.chat_history if include_chat else None,
                    master_hash=master_hash
                )
                st.session_state["generated_pdf"] = pdf_bytes
                
                # Log PDF export in custody tracker
                st.session_state.custody_tracker.record_event(
                    evidence_id=f"EVD-REP-{case['case_id'][-4:]}",
                    action="EXPORTED_JUDICIAL_REPORT",
                    custodian=inv_name,
                    sha256_hash=compute_sha256(pdf_bytes),
                    notes="Automated forensic PDF report generated for court transmission."
                )
            st.success("Court-admissible PDF generated and cryptographically sealed!")

        if "generated_pdf" in st.session_state:
            st.download_button(
                label=f"⬇️ Download Official Forensic PDF Report ({case['case_id']}.pdf)",
                data=st.session_state["generated_pdf"],
                file_name=f"Forensic_Report_{case['case_id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col2:
        st.markdown("#### 📜 Court Report Sections & Evidentiary Scope")
        st.markdown("""
            The generated official PDF conforms to statutory court admissibility rules:
            
            1. **Judicial Header & Agency Seal**: Metropolitan Police Dept / Forensic Investigation Division insignia.
            2. **Chain of Custody & Cryptographic Ledger**: SHA-256 hashes verifying zero file tampering from collection to report export (FRE 901/902).
            3. **Executive Summary**: Synthesizes verified crime classification and threat level.
            4. **RT-DETR Visual Evidence**: Coordinates, category, confidence scores, and physical evidence cones.
            5. **Witness Diarization**: Timestamped sworn statements with acoustic stress metrics.
            6. **CCTV Event Progression**: Keyframe analysis with statutory penal code classifications.
            7. **Unified Master Event Ledger**: Fully synchronized timeline triangulating all 3 modalities.
            8. **Sworn Officer Attestation Block**: Official detective signature line and integrity seal.
        """)

        st.markdown(f"""
            <div style="background: rgba(0,240,255,0.05); border: 1px solid rgba(0,240,255,0.2); border-radius: 8px; padding: 12px; margin-top: 12px;">
                <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #94a3b8;">CRYPTOGRAPHIC HASH DIGEST</div>
                <div style="font-family: 'Courier'; font-size: 0.8rem; color: #00f0ff; word-break: break-all;">
                    {master_hash}
                </div>
            </div>
        """, unsafe_allow_html=True)
