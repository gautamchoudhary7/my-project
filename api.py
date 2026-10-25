"""
CrimeVision AI - Forensic REST API Microservice (Flask)
Platform ID: 6ac4c9851dcde6d7857c163b
Provides RESTful endpoints for multimodal analysis, timeline fusion, and report generation.
"""
import io
import os
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image

from modules.config import PLATFORM_NAME, PLATFORM_ID, VERSION, CATEGORY
from modules.sample_data import get_preloaded_cases
from modules.visual_analyzer import detect_objects_in_uploaded_image, evaluate_threat_level, classify_scene
from modules.audio_analyzer import analyze_transcript_semantics
from modules.fusion_rag import build_unified_master_ledger, format_ledger_context_for_llm
from modules.llm_service import ForensicLLMService
from modules.pdf_report import generate_court_admissible_pdf
from modules.custody import compute_sha256

app = Flask(__name__)
CORS(app)


@app.route("/api/v1/health", methods=["GET"])
def health_check():
    """Returns microservice health and platform metadata."""
    return jsonify({
        "status": "ONLINE",
        "platform_name": PLATFORM_NAME,
        "platform_id": PLATFORM_ID,
        "version": VERSION,
        "category": CATEGORY,
        "standards": ["FRE 901", "FRE 902", "ISO/IEC 27037"]
    })


@app.route("/api/v1/cases", methods=["GET"])
def list_cases():
    """Lists all available forensic case files."""
    cases = get_preloaded_cases()
    summary = []
    for cid, c in cases.items():
        summary.append({
            "case_id": c["case_id"],
            "title": c["title"],
            "classification": c["classification"],
            "threat_level": c["threat_level"],
            "incident_datetime": c["incident_datetime"],
            "location": c["location"]
        })
    return jsonify({"cases": summary, "count": len(summary)})


@app.route("/api/v1/cases/<case_id>", methods=["GET"])
def get_case(case_id):
    """Retrieves full case multimodal file details."""
    cases = get_preloaded_cases()
    if case_id not in cases:
        return jsonify({"error": f"Case {case_id} not found"}), 404
    c = cases[case_id]
    # Return serializable dict (excluding binary objects)
    return jsonify({
        "case_id": c["case_id"],
        "title": c["title"],
        "classification": c["classification"],
        "threat_level": c["threat_level"],
        "incident_datetime": c["incident_datetime"],
        "location": c["location"],
        "lead_investigator": c["lead_investigator"],
        "detections_count": len(c.get("image_detections", [])),
        "transcript_count": len(c.get("audio_transcript", [])),
        "video_events_count": len(c.get("video_events", []))
    })


@app.route("/api/v1/analyze/image", methods=["POST"])
def analyze_image_endpoint():
    """Performs visual object detection on submitted image."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided in multipart form data"}), 400

    file = request.files['image']
    img = Image.open(file.stream)
    detections = detect_objects_in_uploaded_image(img)
    threat = evaluate_threat_level(detections)
    classification = classify_scene(detections)

    return jsonify({
        "detections": detections,
        "threat_evaluation": threat,
        "scene_classification": classification,
        "sha256": compute_sha256(file.read())
    })


@app.route("/api/v1/timeline", methods=["POST"])
def timeline_endpoint():
    """Fuses multimodal inputs into a master chronological ledger."""
    data = request.get_json() or {}
    case_id = data.get("case_id", "CASE-2026-CR-8841")
    cases = get_preloaded_cases()
    c = cases.get(case_id, list(cases.values())[0])

    master_ledger = build_unified_master_ledger(
        case_info=c,
        image_detections=c.get("image_detections", []),
        audio_transcript=c.get("audio_transcript", []),
        video_events=c.get("video_events", [])
    )
    return jsonify({"case_id": case_id, "master_ledger": master_ledger, "total_events": len(master_ledger)})


@app.route("/api/v1/chat", methods=["POST"])
def chat_endpoint():
    """Executes grounded RAG interrogation against evidence ledger."""
    data = request.get_json() or {}
    query = data.get("query", "Summarize the primary weapon evidence")
    case_id = data.get("case_id", "CASE-2026-CR-8841")
    provider = data.get("provider", "demo")
    api_key = data.get("api_key", "")

    cases = get_preloaded_cases()
    c = cases.get(case_id, list(cases.values())[0])
    master_ledger = build_unified_master_ledger(
        case_info=c,
        image_detections=c.get("image_detections", []),
        audio_transcript=c.get("audio_transcript", []),
        video_events=c.get("video_events", [])
    )
    ctx = format_ledger_context_for_llm(master_ledger, c)
    llm = ForensicLLMService(provider=provider, api_key=api_key)
    res = llm.generate_chat_response(query, ctx)
    return jsonify(res)


@app.route("/api/v1/export-report", methods=["POST"])
def export_report_endpoint():
    """Generates court-admissible ReportLab PDF for requested case."""
    data = request.get_json() or {}
    case_id = data.get("case_id", "CASE-2026-CR-8841")
    cases = get_preloaded_cases()
    c = cases.get(case_id, list(cases.values())[0])

    master_ledger = build_unified_master_ledger(
        case_info=c,
        image_detections=c.get("image_detections", []),
        audio_transcript=c.get("audio_transcript", []),
        video_events=c.get("video_events", [])
    )

    pdf_bytes = generate_court_admissible_pdf(
        case_info=c,
        custody_entries=[],
        image_detections=c.get("image_detections", []),
        audio_transcript=c.get("audio_transcript", []),
        video_events=c.get("video_events", []),
        master_ledger=master_ledger,
        master_hash=compute_sha256(b"REPORT_EXPORT")
    )

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Forensic_Report_{case_id}.pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
