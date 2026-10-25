"""
CrimeVision AI - Configuration, Forensic Taxonomies & Global Constants
Platform ID: 6ac4c9851dcde6d7857c163b
"""
from typing import Dict, Any

PLATFORM_NAME = "CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform"
PLATFORM_ID = "6ac4c9851dcde6d7857c163b"
CATEGORY = "Generative AI | Criminal Justice & Public Safety"
VERSION = "2.4.0-PROD"

DEFAULT_AGENCY = "Metropolitan Police Department – Forensic Science Division"
DEFAULT_LAB = "Digital Evidence & Multimedia Analysis Section (DEMAS)"
DEFAULT_INVESTIGATOR = "Det. Marcus Vance (Badge #8421)"
DEFAULT_SUPERVISOR = "Capt. Sarah Jenkins (Forensics Bureau Commander)"

THREAT_LEVELS = {
    "CRITICAL": {
        "color": "#ef4444",
        "bg": "rgba(239, 68, 68, 0.15)",
        "border": "#ef4444",
        "badge": "CRITICAL THREAT",
        "description": "Lethal weapon discharged, direct physical threat, or active violence in progress."
    },
    "HIGH": {
        "color": "#f97316",
        "bg": "rgba(249, 115, 22, 0.15)",
        "border": "#f97316",
        "badge": "HIGH RISK",
        "description": "Visible brandished firearm/weapon, violent breach, or suspect actively fleeing."
    },
    "MEDIUM": {
        "color": "#eab308",
        "bg": "rgba(234, 179, 8, 0.15)",
        "border": "#eab308",
        "badge": "MEDIUM RISK",
        "description": "Forced entry detected, unauthorized intrusion, or escalated verbal hostility."
    },
    "LOW": {
        "color": "#10b981",
        "bg": "rgba(16, 185, 129, 0.15)",
        "border": "#10b981",
        "badge": "LOW RISK",
        "description": "Routine surveillance, baseline movements, or secondary perimeter evidence."
    }
}

SCENE_CLASSIFICATIONS = [
    "Armed Robbery (PC § 211)",
    "Commercial Burglary (PC § 459)",
    "Homicide Investigation (PC § 187)",
    "Assault with a Deadly Weapon (PC § 245)",
    "Malicious Vandalism & Trespass (PC § 594)",
    "Suspicious Activity & Perimeter Breach"
]

PENAL_CODE_DIRECTORY: Dict[str, Dict[str, str]] = {
    "PC 211": {
        "title": "Armed Robbery",
        "classification": "Felony",
        "severity": "CRITICAL",
        "definition": "Felonious taking of personal property in possession of another from his person or immediate presence against will by means of force or fear with deadly weapon."
    },
    "PC 245(a)(2)": {
        "title": "Assault with a Firearm",
        "classification": "Felony",
        "severity": "CRITICAL",
        "definition": "Unlawful attempt coupled with present ability to commit violent injury on person of another using firearm."
    },
    "PC 459": {
        "title": "Commercial Burglary",
        "classification": "Felony",
        "severity": "HIGH",
        "definition": "Forced or unauthorized entry into building, store or warehouse with intent to commit grand or petit larceny or felony."
    },
    "PC 187": {
        "title": "Homicide / Murder Investigation",
        "classification": "Felony (Capital)",
        "severity": "CRITICAL",
        "definition": "Unlawful killing of a human being with malice aforethought."
    },
    "PC 594": {
        "title": "Malicious Vandalism",
        "classification": "Misdemeanor/Felony",
        "severity": "MEDIUM",
        "definition": "Maliciously defacing, damaging, or destroying real or personal property not owned by perpetrator."
    },
    "PC 148(a)(1)": {
        "title": "Resisting / Evading Law Enforcement",
        "classification": "Misdemeanor/Felony",
        "severity": "HIGH",
        "definition": "Willfully resisting, delaying, or obstructing public officer or EMT in discharge or attempt to discharge duty."
    }
}

FORENSIC_CLASSES = {
    "person_suspect": {"label": "Suspect (Armed/Masked)", "color": (255, 69, 58), "hex": "#ff453a", "category": "Suspect Identification"},
    "person_victim": {"label": "Victim / Witness", "color": (48, 209, 88), "hex": "#30d158", "category": "Persons"},
    "firearm_handgun": {"label": "Handgun (Semi-Auto)", "color": (255, 59, 48), "hex": "#ff3b30", "category": "Ballistics / Weapon"},
    "firearm_casing": {"label": "Spent Casing (9mm Luger)", "color": (255, 159, 10), "hex": "#ff9f0a", "category": "Ballistics / Evidence"},
    "edged_weapon": {"label": "Edged Weapon (Tactical Knife)", "color": (255, 69, 58), "hex": "#ff453a", "category": "Edged Weapons"},
    "blood_spatter": {"label": "Blood Spatter (Impact Pattern)", "color": (191, 90, 242), "hex": "#bf5af2", "category": "Serology & Spatter"},
    "forced_entry": {"label": "Forced Entry (Pried Deadbolt)", "color": (100, 210, 255), "hex": "#64d2ff", "category": "Point of Entry"},
    "broken_glass": {"label": "Shattered Safety Glass", "color": (94, 92, 230), "hex": "#5e5ce6", "category": "Point of Entry"},
    "vehicle_getaway": {"label": "Getaway Sedan (Dark Grey)", "color": (255, 214, 10), "hex": "#ffd60a", "category": "Vehicles"}
}

APP_CSS = """
<style>
/* Modern Sleek Dark Forensic UI Styling */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0b0f19;
    color: #e2e8f0;
}

.stApp {
    background: radial-gradient(circle at 15% 15%, rgba(0, 240, 255, 0.03) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(239, 68, 68, 0.03) 0%, transparent 40%),
                #0b0f19;
}

/* Forensic Badges & Headers */
.forensic-header {
    background: linear-gradient(135deg, rgba(21, 28, 46, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.badge-tag {
    display: inline-block;
    padding: 4px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 6px;
    margin-right: 8px;
}

.badge-cyan {
    background: rgba(0, 240, 255, 0.12);
    color: #00f0ff;
    border: 1px solid rgba(0, 240, 255, 0.4);
}

.badge-red {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.5);
}

.badge-green {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.5);
}

.badge-amber {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.5);
}

/* Card Containers */
.forensic-card {
    background: #151c2e;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 16px;
    transition: all 0.2s ease-in-out;
}

.forensic-card:hover {
    border-color: rgba(0, 240, 255, 0.3);
    box-shadow: 0 4px 20px rgba(0, 240, 255, 0.05);
}

/* Timeline Cards */
.timeline-card {
    border-left: 3px solid #00f0ff;
    background: rgba(21, 28, 46, 0.7);
    padding: 12px 18px;
    margin-bottom: 12px;
    border-radius: 0 8px 8px 0;
}

.timeline-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #00f0ff;
    font-weight: 700;
}

.evidence-id-pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 4px;
    padding: 2px 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #94a3b8;
}

/* Metrics & Stats */
.metric-box {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
}
.metric-val {
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #00f0ff;
}
.metric-lbl {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Streamlit Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.8);
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    height: 44px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 6px;
    color: #94a3b8;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0 16px;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(14, 165, 233, 0.2) 100%) !important;
    color: #00f0ff !important;
    border: 1px solid rgba(0, 240, 255, 0.4) !important;
}
</style>
"""
