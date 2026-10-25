"""
CrimeVision AI - Interactive Visualizations, Analytics & UI Utilities
Plotly Timeline, Acoustic Stress Waveforms, Velocity Tracking & Visual Badges.
"""
from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_timeline_plotly_chart(master_ledger: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders an interactive high-contrast forensic chronological timeline using Plotly.
    """
    timeline_items = [item for item in master_ledger if item.get("seconds", -1.0) >= 0]
    if not timeline_items:
        # Fallback if only fixed scene evidence
        timeline_items = master_ledger

    df = pd.DataFrame(timeline_items)
    
    # Map colors
    color_map = {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MEDIUM": "#eab308",
        "LOW": "#10b981"
    }

    fig = go.Figure()

    # Add chronological scatter points
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        sub_df = df[df["severity"] == sev]
        if not sub_df.empty:
            fig.add_trace(go.Scatter(
                x=sub_df["seconds"],
                y=sub_df["modality"].str.replace("_", " "),
                mode="markers+text",
                name=f"{sev} Priority",
                marker=dict(
                    size=16,
                    color=color_map.get(sev, "#00f0ff"),
                    symbol="diamond" if sev == "CRITICAL" else "circle",
                    line=dict(width=2, color="#ffffff")
                ),
                text=sub_df["timestamp"],
                textposition="top center",
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Time: %{customdata[1]} (T+%{x}s)<br>"
                    "ID: %{customdata[2]}<br>"
                    "Statute: %{customdata[3]}<br>"
                    "Summary: %{customdata[4]}<extra></extra>"
                ),
                customdata=sub_df[["modality_badge", "timestamp", "evidence_id", "legal_penal_code", "event_summary"]].values
            ))

    # Add connecting chronological path line
    sorted_df = df.sort_values(by="seconds")
    fig.add_trace(go.Scatter(
        x=sorted_df["seconds"],
        y=sorted_df["modality"].str.replace("_", " "),
        mode="lines",
        line=dict(color="rgba(0, 240, 255, 0.35)", width=2, dash="dot"),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.update_layout(
        title=dict(
            text="CHRONOLOGICAL MULTIMODAL FORENSIC PROGRESSION (T+00:00 to T+00:25)",
            font=dict(color="#00f0ff", size=14, family="JetBrains Mono")
        ),
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        xaxis=dict(
            title="Incident Elapsed Time (Seconds)",
            gridcolor="#1e293b",
            color="#94a3b8",
            zerolinecolor="#334155"
        ),
        yaxis=dict(
            title="Evidence Modality Stream",
            gridcolor="#1e293b",
            color="#94a3b8"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#e2e8f0")
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        height=320
    )
    return fig


def create_acoustic_stress_chart(audio_transcript: List[Dict[str, Any]]) -> go.Figure:
    """Renders acoustic vocal stress & panic curve across witness timeline."""
    times = [item.get("timestamp", "00:00") for item in audio_transcript]
    stress_levels = [item.get("stress_level", 50) for item in audio_transcript]
    speakers = [item.get("speaker", "Caller") for item in audio_transcript]

    fig = go.Figure()
    
    # Stress curve
    fig.add_trace(go.Scatter(
        x=times,
        y=stress_levels,
        mode="lines+markers",
        name="Vocal Stress Index",
        line=dict(color="#f43f5e", width=3),
        marker=dict(size=10, color="#f43f5e"),
        fill="tozeroy",
        fillcolor="rgba(244, 63, 94, 0.15)",
        hovertemplate="Speaker: %{text}<br>Stress: %{y}/100<br>Timestamp: %{x}<extra></extra>",
        text=speakers
    ))

    # Add panic threshold indicator
    fig.add_hline(y=80, line_dash="dash", line_color="#ef4444", annotation_text="Acute Panic Threshold (>80)", annotation_font_color="#ef4444")
    fig.add_hline(y=50, line_dash="dot", line_color="#eab308", annotation_text="Elevated Tension (>50)", annotation_font_color="#eab308")

    fig.update_layout(
        title=dict(
            text="ACOUSTIC VOCAL STRESS & PANIC TRAJECTORY",
            font=dict(color="#00f0ff", size=13, family="JetBrains Mono")
        ),
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        xaxis=dict(title="Timestamp (MM:SS)", gridcolor="#1e293b", color="#94a3b8"),
        yaxis=dict(title="Stress Metric (0-100)", range=[0, 105], gridcolor="#1e293b", color="#94a3b8"),
        margin=dict(l=30, r=30, t=50, b=30),
        height=260
    )
    return fig


def create_suspect_velocity_chart(video_events: List[Dict[str, Any]]) -> go.Figure:
    """Renders suspect / vehicle velocity acceleration curve."""
    times = [v.get("timestamp", "00:00") for v in video_events]
    velocities = [float(v.get("velocity_kmh", 0.0) or float(str(v.get("motion_velocity", "0")).split()[0])) for v in video_events]
    events = [v.get("event_title", v.get("description", "Event")) for v in video_events]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=times,
        y=velocities,
        mode="lines+markers+text",
        name="Velocity (km/h)",
        line=dict(color="#00f0ff", width=3),
        marker=dict(size=11, color="#00f0ff"),
        text=[f"{v:.1f} km/h" for v in velocities],
        textposition="top center",
        fill="tozeroy",
        fillcolor="rgba(0, 240, 255, 0.12)",
        hovertemplate="Event: %{text}<br>Velocity: %{y} km/h<br>Time: %{x}<extra></extra>"
    ))

    fig.add_hline(y=40, line_dash="dash", line_color="#ef4444", annotation_text="High-Speed Flight Threshold (>40 km/h)", annotation_font_color="#ef4444")

    fig.update_layout(
        title=dict(
            text="SUSPECT / VEHICULAR MOTION VELOCITY TREND",
            font=dict(color="#00f0ff", size=13, family="JetBrains Mono")
        ),
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        xaxis=dict(title="Surveillance Timestamp (MM:SS)", gridcolor="#1e293b", color="#94a3b8"),
        yaxis=dict(title="Speed (km/h)", gridcolor="#1e293b", color="#94a3b8"),
        margin=dict(l=30, r=30, t=50, b=30),
        height=260
    )
    return fig
