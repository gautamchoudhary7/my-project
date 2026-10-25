"""
CrimeVision AI - Comprehensive Forensic Test Suite
Validates Chain of Custody, RT-DETR Detections, Whisper Analytics,
Video Tracking, Multimodal Fusion Ledger, and ReportLab PDF Export.
"""
import os
import sys
import unittest

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from PIL import Image

from modules.custody import ChainOfCustodyTracker, compute_sha256, generate_evidence_id
from modules.sample_data import get_preloaded_cases
from modules.visual_analyzer import (
    annotate_image, evaluate_threat_level, classify_scene,
    generate_investigative_leads
)
from modules.audio_analyzer import analyze_transcript_semantics
from modules.video_analyzer import get_video_progression_summary
from modules.fusion_rag import (
    build_unified_master_ledger, format_ledger_context_for_llm,
    get_cross_modal_correlations
)
from modules.llm_service import ForensicLLMService
from modules.pdf_report import generate_court_admissible_pdf


class TestCrimeVisionForensics(unittest.TestCase):
    """Forensic verification test cases."""

    def setUp(self):
        self.cases = get_preloaded_cases()
        self.case = self.cases["CASE-2026-CR-8841"]

    def test_01_chain_of_custody_and_sha256(self):
        """Verifies cryptographic SHA-256 integrity and tamper detection."""
        tracker = ChainOfCustodyTracker(
            case_id="TEST-CASE-01",
            lead_investigator="Det. Marcus Vance",
            agency="Metro Forensics"
        )
        sample_data = b"FORENSIC_RAW_EVIDENCE_STREAM_DATA"
        h_val = compute_sha256(sample_data)
        self.assertEqual(len(h_val), 64)

        evd_id = generate_evidence_id("image", 1)
        self.assertTrue(evd_id.startswith("EVD-IMG"))

        entry = tracker.record_event(
            evidence_id=evd_id,
            action="COLLECTED",
            custodian="Det. Vance",
            sha256_hash=h_val,
            notes="Secured from primary floor"
        )
        self.assertEqual(entry["evidence_id"], evd_id)

        # Verify integrity
        verify_ok = tracker.verify_item(evd_id, sample_data)
        self.assertTrue(verify_ok["verified"])
        self.assertFalse(verify_ok["tamper_detected"])

        # Tampered data test
        tampered_data = b"TAMPERED_FORENSIC_DATA"
        verify_bad = tracker.verify_item(evd_id, tampered_data)
        self.assertFalse(verify_bad["verified"])
        self.assertTrue(verify_bad["tamper_detected"])

    def test_02_visual_threat_and_classification(self):
        """Tests RT-DETR detection interpretation and scene classification."""
        detections = self.case["image_detections"]
        self.assertGreaterEqual(len(detections), 4)

        threat = evaluate_threat_level(detections)
        self.assertEqual(threat["level"], "CRITICAL")
        self.assertTrue(threat["lethal_weapon_present"])
        self.assertTrue(threat["breach_point_identified"])

        scene_cls = classify_scene(detections)
        self.assertIn("Armed Robbery", scene_cls)

        leads = generate_investigative_leads(detections, scene_cls)
        self.assertGreater(len(leads), 3)

        # Test image annotation rendering
        dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
        annotated = annotate_image(dummy_img, detections)
        self.assertEqual(annotated.shape, dummy_img.shape)

    def test_03_audio_whisper_and_stress_analytics(self):
        """Tests acoustic transcript parsing and semantic entity extraction."""
        transcript = self.case["audio_transcript"]
        analytics = analyze_transcript_semantics(transcript)

        self.assertGreaterEqual(analytics["peak_stress_index"], 90)
        self.assertIn("CODE 3", analytics["urgency_rating"])
        self.assertGreater(analytics["veracity_score"], 80)
        self.assertTrue(len(analytics["weapons_mentioned"]) > 0)
        self.assertTrue(len(analytics["vehicles_mentioned"]) > 0)

    def test_04_video_progression_and_penal_codes(self):
        """Tests CCTV video progression analysis and penal statute linkage."""
        video_events = self.case["video_events"]
        summary = get_video_progression_summary(video_events)

        self.assertGreaterEqual(summary["total_keyframes"], 4)
        self.assertGreaterEqual(summary["critical_events_count"], 1)
        self.assertTrue(summary["flight_detected"])

    def test_05_multimodal_fusion_and_rag(self):
        """Tests unified master event ledger creation and grounded RAG query engine."""
        master_ledger = build_unified_master_ledger(
            case_info=self.case,
            image_detections=self.case["image_detections"],
            audio_transcript=self.case["audio_transcript"],
            video_events=self.case["video_events"]
        )
        self.assertGreater(len(master_ledger), 8)

        # Verify chronological order
        seconds_list = [item["seconds"] for item in master_ledger]
        self.assertEqual(seconds_list, sorted(seconds_list))

        # Check cross-modal correlations
        correlations = get_cross_modal_correlations(master_ledger)
        self.assertGreaterEqual(len(correlations), 2)

        # Test Grounded RAG query
        ctx = format_ledger_context_for_llm(master_ledger, self.case)
        llm = ForensicLLMService(provider="demo")
        res = llm.generate_chat_response("Was a weapon visible before the suspect fled?", ctx)
        self.assertIn("answer", res)
        self.assertGreater(len(res["citations"]), 0)
        self.assertTrue(any("EVD-" in c for c in res["citations"]))

    def test_06_court_admissible_pdf_export(self):
        """Validates compilation of court-admissible ReportLab PDF document."""
        master_ledger = build_unified_master_ledger(
            case_info=self.case,
            image_detections=self.case["image_detections"],
            audio_transcript=self.case["audio_transcript"],
            video_events=self.case["video_events"]
        )
        pdf_bytes = generate_court_admissible_pdf(
            case_info=self.case,
            custody_entries=[],
            image_detections=self.case["image_detections"],
            audio_transcript=self.case["audio_transcript"],
            video_events=self.case["video_events"],
            master_ledger=master_ledger,
            master_hash=compute_sha256(b"TEST_INTEGRITY_DIGEST")
        )
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_07_flask_rest_api(self):
        """Validates Flask REST API endpoints."""
        from api import app
        client = app.test_client()

        # Health endpoint
        res = client.get("/api/v1/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "ONLINE")
        self.assertEqual(data["platform_id"], "6ac4c9851dcde6d7857c163b")

        # Cases list endpoint
        res_cases = client.get("/api/v1/cases")
        self.assertEqual(res_cases.status_code, 200)
        data_cases = res_cases.get_json()
        self.assertGreaterEqual(data_cases["count"], 2)

        # Timeline endpoint
        res_timeline = client.post("/api/v1/timeline", json={"case_id": "CASE-2026-CR-8841"})
        self.assertEqual(res_timeline.status_code, 200)
        data_timeline = res_timeline.get_json()
        self.assertGreater(data_timeline["total_events"], 5)

        # Grounded Chat endpoint
        res_chat = client.post("/api/v1/chat", json={
            "query": "Was a weapon visible?",
            "case_id": "CASE-2026-CR-8841",
            "provider": "demo"
        })
        self.assertEqual(res_chat.status_code, 200)
        data_chat = res_chat.get_json()
        self.assertIn("answer", data_chat)
        self.assertTrue(len(data_chat["citations"]) > 0)


if __name__ == "__main__":
    unittest.main()
