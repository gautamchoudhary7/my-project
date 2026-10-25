# CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform
**Skill Wallet Capstone Project 2 | Platform ID: `6ac4c9851dcde6d7857c163b`**  
**Category:** Generative AI | Criminal Justice & Public Safety  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![ReportLab](https://img.shields.io/badge/ReportLab-5.1-orange.svg)](https://www.reportlab.com/)
[![RT--DETR%20%2F%20YOLOv8](https://img.shields.io/badge/Vision-RT--DETR%20%2F%20YOLOv8-green.svg)](https://github.com/ultralytics/ultralytics)
[![Whisper](https://img.shields.io/badge/Audio-OpenAI%20Whisper-blueviolet.svg)](https://openai.com/research/whisper)
[![Compliance](https://img.shields.io/badge/Judicial-FRE%20901%20%2F%20902-success.svg)](#judicial-admissibility-compliance)

---

## 🏛️ Executive Summary & Objective

**CrimeVision AI** is an automated forensic intelligence platform designed for municipal police departments, federal investigative bodies, and digital forensics laboratories. The platform automates crime scene reconstruction by fusing image, video, and audio evidence into a synchronized chronological master event ledger. 

By integrating **RT-DETR / YOLOv8** computer vision, **OpenAI Whisper** audio diarization, **OpenCV** frame tracking, and **grounded RAG query intelligence (Gemini 2.5 / Groq Llama-3.3 / Smart Offline Fallback)**, CrimeVision AI eliminates investigative silos, prevents human transcription bias, eliminates hallucinations via strict evidentiary citation, and outputs 1-click **court-admissible PDF reports** compliant with Federal Rules of Evidence (FRE 901 & 902).

---

## 📋 Kanban Epics Mapping

| Epic | Module Name | Scope & Key Capabilities | Status |
| :--- | :--- | :--- | :---: |
| **Prerequisites** | `Flask / PyTorch / Whisper` | Environment setup, REST microservice (`api.py`), PyTorch runtime, core ML dependencies. | ✅ Complete |
| **Epic 1** | `Initialization & Env` | Secure API key ingestion (Gemini / Groq / Demo mode), Chain-of-Custody SHA-256 ledger, tamper verification. | ✅ Complete |
| **Epic 2** | `Visual Evidence Tagger` | RT-DETR / YOLOv8 object detection (persons, firearms, edged weapons, blood spatter, forced entry), threat classification, investigative leads. | ✅ Complete |
| **Epic 3** | `Audio Transcription` | Witness & 911 audio ingestion, speaker diarization, acoustic stress index, entity extraction, timeline markers. | ✅ Complete |
| **Epic 4** | `CCTV Video Tracking` | Frame sampling, suspect trajectory tracking, velocity kinetics, statutory penal code classification (§ 211, § 245, § 459). | ✅ Complete |
| **Epic 5** | `Multimodal Timeline Fusion` | Master chronological ledger, cross-modal triangulation, zero-hallucination RAG evidence chat with strict `[EVD-...]` citations. | ✅ Complete |
| **Epic 6** | `Dashboard & PDF Export` | Streamlit forensic dark dashboard, 1-click court-admissible ReportLab PDF generator with cryptographic seals & officer attestation. | ✅ Complete |

---

## 🏗️ System Architecture & Multimodal Fusion Pipeline

```
                                  CRIMEVISION AI ARCHITECTURE
                                  
     [ Scene Photography ]          [ 911 / Witness Audio ]           [ CCTV Surveillance Video ]
              │                                │                                    │
              ▼                                ▼                                    ▼
       ┌───────────────┐               ┌───────────────┐                    ┌───────────────┐
       │ RT-DETR /     │               │ OpenAI Whisper│                    │ OpenCV Frame  │
       │ YOLOv8 Vision │               │ Diarization   │                    │ Tracking      │
       └───────┬───────┘               └───────┬───────┘                    └───────┬───────┘
               │                               │                                    │
       • Weapons / Ballistics           • 911 Timestamps                    • Suspect Trajectories
       • Blood Spatter Patterns         • Speaker Diarization               • Vehicle Kinetics (km/h)
       • Forced Entry Breaches          • Vocal Stress Index                • Statutory Penal Codes
               │                               │                                    │
               └───────────────────────┬───────┴────────────────────────────────────┘
                                       ▼
                       ┌────────────────────────────────┐
                       │  UNIFIED MASTER EVENT LEDGER   │
                       │ (Chronological Synchronization)│
                       └───────────────┬────────────────┘
                                       │
               ┌───────────────────────┴────────────────────────┐
               ▼                                                ▼
   ┌───────────────────────┐                        ┌───────────────────────┐
   │  Grounded Evidence    │                        │ Court-Admissible      │
   │  RAG Conversational   │                        │ ReportLab PDF Engine  │
   │  (Zero Hallucination) │                        │ (FRE 901 Sealed)      │
   └───────────────────────┘                        └───────────────────────┘
```

---

## 🛠️ Core Modules Deep Dive

### 1. Configuration & Forensic Chain-of-Custody (`modules/custody.py`, `modules/config.py`)
- **API Security:** Supports Google Gemini (`gemini-2.5-flash`), Groq (`llama-3.3-70b-versatile`), and an automatic **Smart Offline Fallback Engine** that guarantees 100% turnkey evaluation with zero external API dependencies.
- **Cryptographic Tamper-Evidence:** Generates immutable SHA-256 hashes for all uploaded evidence items. Any file manipulation invalidates the digital seal in compliance with **ISO/IEC 27037:2012**.
- **Audit Ledger:** Records timestamped custodian transfers, evidence identifiers (`EVD-IMG-2026-001`, `EVD-AUD-2026-002`, `EVD-VID-2026-003`), and lead detective sign-offs.

### 2. Tab 1: Crime Scene Visual Evidence Tagger (`modules/visual_analyzer.py`)
- **RT-DETR / YOLOv8 Detection:** Localizes firearms (handguns, shell casings), edged weapons (knives), biological serology (blood spatter patterns), and forced entry points (pried deadbolts, shattered glass).
- **Spatial Bounding Annotations:** High-contrast forensic bounding boxes with tactical corner brackets, class labels, confidence scores, and normalized pixel coordinates.
- **Automated Threat Matrix:** Dynamically computes scene threat tier (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and legal crime classification (`Armed Robbery PC § 211`, `Commercial Burglary PC § 459`, `Aggravated Assault PC § 245`).
- **Prioritized Detective Leads:** Outputs actionable operational steps (e.g., NIBIN ballistics processing, LCN touch DNA swabbing, mikrosil tool mark casting).

### 3. Tab 2: Witness Audio Transcription & Timeline (`modules/audio_analyzer.py`)
- **Acoustic Diarization:** Isolates speaker turns (`Speaker 1 [Dispatcher]`, `Speaker 2 [Witness/Caller]`).
- **Acoustic Vocal Stress Engine:** Calculates peak stress metrics (0-100), acute panic thresholds (>80), and witness veracity confidence scores.
- **Entity Extraction:** Mines weapons, vehicles, license plates, locations, and suspect clothing attributes.
- **Chronological Markers:** Emits temporal anchors `[00:02]`, `[00:06]`, `[00:10]` directly into the master fusion ledger.

### 4. Tab 3: CCTV Video Analysis & Event Progression (`modules/video_analyzer.py`)
- **OpenCV Keyframe Sampling:** Extracts frames at calibrated temporal intervals across surveillance video streams.
- **Trajectory & Kinetic Tracking:** Computes suspect velocity (km/h) and vehicle escape acceleration with automated detection of high-speed felonious flight (>40 km/h).
- **Penal Code Directory Linkage:** Automatically tags frames with penal statutes:
  * `PC § 211` – Armed Robbery (Felony)
  * `PC § 245(a)(2)` – Assault with a Firearm (Felony)
  * `PC § 459` – Commercial Burglary (Felony)
  * `PC § 148(a)(1)` – Resisting / Evading Law Enforcement (Felony Flight)

### 5. Tab 4: Multimodal Fusion & Grounded Evidence Chat (`modules/fusion_rag.py`)
- **Master Unified Ledger:** Chronologically synchronizes visual scene photography, 911 audio statements, and CCTV surveillance frames.
- **Cross-Modal Triangulation:** Automatically matches verbal witness testimony to video keyframe actions and physical scene ballistic markers.
- **Zero-Hallucination RAG Interrogation:** Conversational interface strictly constrained to verified ledger facts. Every generated answer provides bracketed evidence citations (e.g., `[EVD-IMG-2026-001]`, `[EVD-AUD-2026-002 @ 00:10]`, `[EVD-VID-2026-003 @ 00:08]`).

### 6. Tab 5: Automated Forensic PDF Export (`modules/pdf_report.py`)
- **Judicial Styling:** Built using **ReportLab** with official police department insignia, running headers, two-pass `NumberedCanvas` page numbering, and clean alternating table layouts.
- **Evidentiary Content:**
  * Chain of Custody & SHA-256 integrity block
  * Executive Summary & Threat Matrix
  * RT-DETR detection coordinates & confidence scores
  * Sworn witness audio transcripts & speaker tags
  * CCTV frame progression & penal code directory violations
  * Master Chronological Event Timeline
  * Sworn Officer Attestation & Digital Signature block
- **1-Click Download:** Generates court-ready PDF directly into user memory buffer without filesystem leakage.

### 7. Companion Forensic REST API Microservice (`api.py`)
- Implements production Flask REST microservice exposing:
  * `GET /api/v1/health` – System telemetry, platform ID, and standard certifications.
  * `GET /api/v1/cases` – Summary catalog of all active forensic cases.
  * `GET /api/v1/cases/<case_id>` – Comprehensive case details.
  * `POST /api/v1/analyze/image` – Multipart form upload for RT-DETR visual object detection.
  * `POST /api/v1/timeline` – Multimodal chronological event ledger fusion.
  * `POST /api/v1/chat` – Grounded RAG query interrogation.
  * `POST /api/v1/export-report` – Automated ReportLab judicial PDF generation endpoint.

---

## ⚖️ Judicial Admissibility Compliance

CrimeVision AI is designed from the ground up to satisfy stringent courtroom evidentiary standards:

1. **Federal Rule of Evidence 901 (Authenticating or Identifying Evidence):**  
   Every media file ingested is indexed with a cryptographic SHA-256 hash upon collection. Any subsequent byte modification is immediately flagged by the tamper detection engine.
2. **Federal Rule of Evidence 902(13) & 902(14) (Self-Authenticating Digital Records):**  
   The platform produces verified digital certifications of records generated by an electronic process with officer sign-off.
3. **Daubert Standard for Scientific Reliability:**  
   AI object detection models output explicit confidence percentages and spatial coordinate bounding boxes, avoiding black-box assertions.
4. **Zero-Hallucination Guardrails:**  
   The RAG interrogation engine is forbidden from interpolating uncorroborated facts. Where evidence is absent, the model explicitly returns `"INCONCLUSIVE - Evidence does not substantiate this claim"`.

---

## 🚀 Quickstart & Installation

### Hardware & System Requirements
- **OS:** Windows 10/11, macOS (Monterey+), or Linux (Ubuntu 20.04+)
- **Processor:** Intel Core i5 (8th Gen+) / AMD Ryzen 5 or Apple Silicon M-series
- **RAM:** Minimum 8 GB (Recommended: 16 GB)
- **Python:** 3.9, 3.10, 3.11, 3.12, or 3.13

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-org/crimevision-ai.git
cd "c:\crimevision AI"

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run Forensic Unit Tests
```bash
python tests/test_forensics.py
```
*All 7 unit tests will execute, validating hashing, object detection, audio parsing, video kinetics, fusion ledger, PDF generation, and REST endpoints.*

### 4. Launch the Streamlit Forensic Platform
```bash
python -m streamlit run app.py
```
Open your browser to `http://localhost:8501`. The application will boot immediately with rich preloaded forensic cases (`CASE-2026-CR-8841: Armed Robbery at Apex Jewelry Vault` and `CASE-2026-CR-4192: Commercial Burglary & Weapon Discharge`).

### 5. (Optional) Run Companion Flask REST Microservice
```bash
python api.py
```
Microservice will be active on `http://localhost:5000`.

---

## 🧪 Turnkey Preloaded Cases Included

The platform includes synthetic, high-fidelity media assets preloaded into `assets/`:
1. **Case #2026-CR-8841: Armed Robbery & Battery at Apex Jewelry Vault**
   - **Scene Photography:** High-resolution crime scene showing broken display glass, spent 9mm shell casing, polymer handgun, forced door deadbolt, and forensic markers #1-#4.
   - **Emergency Audio:** 16-second 911 dispatch audio with acoustic stress fluctuations and speaker diarization.
   - **Surveillance CCTV:** 8-second 10fps alleyway video showing suspect arrival, firearm presentation, and rapid vehicular getaway.
2. **Case #2026-CR-4192: Midnight Commercial Burglary & Weapon Discharge**
   - Cargo berth breach investigation featuring hydraulic bolt-cutter tool marks, .45 ACP shell casing, and night watchman distress call.

---

## 📑 File Structure

```
c:\crimevision AI\
├── app.py                      # Main Streamlit Forensic Intelligence Dashboard
├── api.py                      # Flask REST API Microservice (Health, Vision, RAG, PDF)
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive documentation & judicial standards
├── .streamlit/
│   └── config.toml             # Custom high-tech dark forensic theme
├── modules/
│   ├── __init__.py
│   ├── config.py               # Constants, penal codes, threat matrices, styling CSS
│   ├── custody.py              # Cryptographic Chain of Custody & SHA-256 tracking
│   ├── visual_analyzer.py      # RT-DETR / YOLOv8 Object detection & scene captioning
│   ├── audio_analyzer.py       # Whisper speech transcription, stress & entity extraction
│   ├── video_analyzer.py       # CCTV keyframe sampling, velocity & penal codes
│   ├── fusion_rag.py           # Unified master event ledger & grounded evidence RAG
│   ├── pdf_report.py           # Court-admissible ReportLab PDF generator
│   ├── sample_data.py          # Preloaded cases & synthetic forensic media generators
│   └── utils.py                # Plotly timelines, stress graphs, velocity curves
├── tests/
│   ├── __init__.py
│   └── test_forensics.py       # Comprehensive 7-point forensic test suite
└── assets/                     # Synthetic crime scene imagery, audio WAVs, CCTV MP4s
```

---

## 🛡️ License & Platform Metadata
- **Platform Name:** CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform
- **Platform ID:** `6ac4c9851dcde6d7857c163b`
- **Category:** Generative AI | Criminal Justice & Public Safety
- **Version:** `2.4.0-PROD`
- **Lead Architect:** Senior Forensic Systems Architect
