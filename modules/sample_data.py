"""
CrimeVision AI - Synthetic Forensic Cases & Multimodal Asset Generators
Provides realistic pre-loaded case files, synthetic crime scene imagery,
WAV audio recordings, and CCTV video clips for immediate turnkey operation.
"""
import os
import math
import wave
import struct
import numpy as np
import cv2
from PIL import Image
from typing import Dict, Any, List


def ensure_asset_dir(assets_dir: str = "assets") -> str:
    """Ensures assets directory exists and returns absolute path."""
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir


def generate_crime_scene_image_case1(filepath: str) -> str:
    """Generates realistic crime scene image for Case 1: Apex Jewelry Robbery."""
    width, height = 960, 640
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (35, 38, 48)

    for x in range(0, width, 60):
        cv2.line(img, (x, 0), (x, height), (45, 50, 62), 1)
    for y in range(0, height, 60):
        cv2.line(img, (0, y), (width, y), (45, 50, 62), 1)

    np.random.seed(42)
    for _ in range(35):
        pt1 = (np.random.randint(480, 720), np.random.randint(300, 520))
        pt2 = (pt1[0] + np.random.randint(-15, 15), pt1[1] + np.random.randint(-15, 15))
        pt3 = (pt1[0] + np.random.randint(-15, 15), pt1[1] + np.random.randint(-15, 15))
        cv2.fillPoly(img, [np.array([pt1, pt2, pt3])], (160, 190, 210))
        cv2.polylines(img, [np.array([pt1, pt2, pt3])], True, (210, 230, 255), 1)

    center_spatter = (320, 380)
    for _ in range(45):
        rad = np.random.uniform(2, 65)
        angle = np.random.uniform(0, 2 * np.pi)
        sx = int(center_spatter[0] + rad * np.cos(angle))
        sy = int(center_spatter[1] + rad * np.sin(angle) * 0.7)
        size = np.random.randint(2, 6)
        cv2.circle(img, (sx, sy), size, (25, 25, 160), -1)
    cv2.ellipse(img, center_spatter, (28, 16), 25, 0, 360, (20, 20, 140), -1)

    gun_pts = np.array([
        [680, 420], [740, 420], [740, 440], [715, 440], [710, 480], [690, 475], [698, 440], [680, 440]
    ], np.int32)
    cv2.fillPoly(img, [gun_pts], (20, 20, 25))
    cv2.polylines(img, [gun_pts], True, (60, 60, 70), 2)

    casing_rect = (760, 450, 12, 6)
    cv2.rectangle(img, (casing_rect[0], casing_rect[1]),
                  (casing_rect[0] + casing_rect[2], casing_rect[1] + casing_rect[3]), (50, 170, 220), -1)

    cv2.rectangle(img, (800, 80), (920, 520), (55, 60, 75), -1)
    cv2.rectangle(img, (805, 85), (915, 515), (25, 28, 38), -1)
    cv2.line(img, (802, 280), (810, 310), (120, 130, 140), 4)

    def draw_evidence_cone(x, y, num):
        pts = np.array([[x, y], [x - 24, y + 42], [x + 24, y + 42]], np.int32)
        cv2.fillPoly(img, [pts], (20, 210, 240))
        cv2.polylines(img, [pts], True, (10, 150, 180), 2)
        cv2.putText(img, str(num), (x - 7, y + 33), cv2.FONT_HERSHEY_DUPLEX, 0.9, (15, 15, 20), 2)

    draw_evidence_cone(725, 370, 1)
    draw_evidence_cone(785, 405, 2)
    draw_evidence_cone(830, 240, 3)
    draw_evidence_cone(320, 310, 4)

    cv2.rectangle(img, (0, 0), (width, 45), (15, 18, 25), -1)
    cv2.line(img, (0, 45), (width, 45), (0, 240, 255), 2)
    cv2.putText(img, "METROPOLITAN POLICE DEPT | CASE #2026-CR-8841: APEX JEWELRY VAULT ROBBERY",
                (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 240, 255), 1)

    cv2.rectangle(img, (width - 240, height - 35), (width - 20, height - 15), (20, 25, 35), -1)
    for i in range(10):
        color = (240, 240, 240) if i % 2 == 0 else (30, 30, 30)
        cv2.rectangle(img, (width - 235 + i * 21, height - 32), (width - 235 + (i + 1) * 21, height - 18), color, -1)
    cv2.putText(img, "FORENSIC SCALE (10cm)", (width - 235, height - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 175, 195), 1)

    cv2.imwrite(filepath, img)
    return filepath


def generate_crime_scene_image_case2(filepath: str) -> str:
    """Generates realistic crime scene image for Case 2: Harbor Berth 14 Commercial Burglary."""
    width, height = 960, 640
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (25, 30, 38)

    cv2.rectangle(img, (600, 80), (940, 520), (30, 70, 130), -1)
    cv2.rectangle(img, (605, 85), (935, 515), (20, 50, 100), -1)
    for x in range(630, 920, 30):
        cv2.line(img, (x, 90), (x, 510), (45, 90, 150), 3)
    cv2.putText(img, "CARGO CONTAINER C-3", (620, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 230, 255), 2)
    cv2.circle(img, (720, 280), 8, (15, 15, 20), -1)
    cv2.circle(img, (720, 280), 12, (90, 120, 160), 1)

    for x in range(40, 480, 25):
        cv2.line(img, (x, 60), (x + 35, 540), (70, 80, 95), 1)
        cv2.line(img, (x + 35, 60), (x, 540), (70, 80, 95), 1)

    cv2.circle(img, (260, 320), 75, (25, 30, 38), -1)
    cv2.line(img, (200, 260), (220, 300), (160, 170, 190), 3)
    cv2.line(img, (320, 260), (300, 300), (160, 170, 190), 3)

    cv2.line(img, (220, 440), (310, 490), (180, 40, 30), 6)
    cv2.line(img, (240, 490), (290, 440), (180, 40, 30), 6)
    cv2.circle(img, (265, 465), 10, (100, 110, 120), -1)

    casing_rect = (520, 420, 14, 8)
    cv2.rectangle(img, (casing_rect[0], casing_rect[1]),
                  (casing_rect[0] + casing_rect[2], casing_rect[1] + casing_rect[3]), (50, 180, 240), -1)

    def draw_evidence_cone(x, y, num):
        pts = np.array([[x, y], [x - 24, y + 42], [x + 24, y + 42]], np.int32)
        cv2.fillPoly(img, [pts], (20, 210, 240))
        cv2.polylines(img, [pts], True, (10, 150, 180), 2)
        cv2.putText(img, str(num), (x - 7, y + 33), cv2.FONT_HERSHEY_DUPLEX, 0.9, (15, 15, 20), 2)

    draw_evidence_cone(270, 370, 1)
    draw_evidence_cone(530, 360, 2)
    draw_evidence_cone(720, 220, 3)

    cv2.rectangle(img, (0, 0), (width, 45), (15, 18, 25), -1)
    cv2.line(img, (0, 45), (width, 45), (0, 240, 255), 2)
    cv2.putText(img, "METROPOLITAN POLICE DEPT | CASE #2026-CR-4192: HARBOR BERTH 14 COMMERCIAL BURGLARY",
                (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (230, 240, 255), 1)

    cv2.rectangle(img, (width - 240, height - 35), (width - 20, height - 15), (20, 25, 35), -1)
    for i in range(10):
        color = (240, 240, 240) if i % 2 == 0 else (30, 30, 30)
        cv2.rectangle(img, (width - 235 + i * 21, height - 32), (width - 235 + (i + 1) * 21, height - 18), color, -1)
    cv2.putText(img, "FORENSIC SCALE (10cm)", (width - 235, height - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 175, 195), 1)

    cv2.imwrite(filepath, img)
    return filepath


def generate_audio_file(filepath: str, duration_sec: int = 15, freq_type: str = "dispatch") -> str:
    """Generates a synthetic realistic dispatch/witness WAV audio file."""
    sample_rate = 44100
    num_samples = sample_rate * duration_sec
    channels = 1
    sampwidth = 2

    with wave.open(filepath, 'w') as wav:
        wav.setparams((channels, sampwidth, sample_rate, num_samples, 'NONE', 'not compressed'))
        frames = bytearray()

        for i in range(num_samples):
            t = float(i) / sample_rate
            base_f = 440.0 if freq_type == "dispatch" else 330.0
            carrier = 0.08 * math.sin(2.0 * math.pi * base_f * t)
            speech_sim = 0.45 * (
                math.sin(2.0 * math.pi * (220.0 if freq_type == "dispatch" else 180.0) * t + math.sin(2.0 * math.pi * 5.0 * t)) *
                math.sin(2.0 * math.pi * 600.0 * t) *
                math.exp(-((t % 2.5 - 1.2) ** 2) / 0.5)
            )
            noise = 0.02 * ((hash(i) % 2000) / 1000.0 - 1.0)
            burst = 0.25 * math.sin(2.0 * math.pi * 1200.0 * t) if (t < 0.3 or (7.0 < t < 7.3)) else 0.0

            sample = carrier + speech_sim + noise + burst
            sample = max(-0.95, min(0.95, sample))
            ival = int(sample * 32767.0)
            frames.extend(struct.pack('<h', ival))

        wav.writeframes(frames)
    return filepath


def generate_video_file_case1(filepath: str, duration_sec: int = 8, fps: int = 10) -> str:
    """Generates CCTV video for Case 1: Apex Jewelry Alleyway."""
    width, height = 640, 360
    total_frames = duration_sec * fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    for frame_idx in range(total_frames):
        t = frame_idx / fps
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 24, 32)

        cv2.line(frame, (0, 240), (width, 240), (45, 52, 65), 2)
        cv2.line(frame, (120, 0), (120, 240), (35, 40, 50), 2)
        cv2.line(frame, (520, 0), (520, 240), (35, 40, 50), 2)

        car_x = int(140 + t * 45)
        car_y = 190
        cv2.rectangle(frame, (car_x, car_y), (car_x + 95, car_y + 35), (55, 60, 68), -1)
        cv2.circle(frame, (car_x + 90, car_y + 12), 4, (30, 30, 220), -1)
        cv2.circle(frame, (car_x + 90, car_y + 24), 4, (30, 30, 220), -1)

        suspect_x = int(480 - t * 35) if t < 4.0 else int(340 + (t - 4.0) * 55)
        suspect_y = 180
        cv2.rectangle(frame, (suspect_x - 18, suspect_y - 50), (suspect_x + 18, suspect_y + 50), (40, 45, 55), -1)
        cv2.circle(frame, (suspect_x, suspect_y - 55), 14, (70, 75, 85), -1)

        box_color = (0, 0, 255) if (2.5 <= t <= 5.5) else (0, 240, 255)
        label = "PERSON: SUSPECT [WEAPON BRANDISHED]" if (2.5 <= t <= 5.5) else "PERSON: SUSPECT #1"
        cv2.rectangle(frame, (suspect_x - 24, suspect_y - 75), (suspect_x + 24, suspect_y + 55), box_color, 2)
        cv2.rectangle(frame, (suspect_x - 24, suspect_y - 95), (suspect_x + 130, suspect_y - 75), box_color, -1)
        cv2.putText(frame, label, (suspect_x - 20, suspect_y - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, (10, 10, 15), 1)

        timestamp_str = f"CAM-04 [REAR ALLEY] | 2026-10-24 23:42:{15 + int(t):02d} EST"
        cv2.putText(frame, "● REC [LIVE_FEED]", (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 60, 240), 1)
        cv2.putText(frame, timestamp_str, (170, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 230, 245), 1)
        cv2.putText(frame, f"FPS: {fps}.0 | FRAME: {frame_idx:04d} | AI TRACK: ACTIVE",
                    (20, height - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 240, 255), 1)

        out.write(frame)

    out.release()
    return filepath


def generate_video_file_case2(filepath: str, duration_sec: int = 8, fps: int = 10) -> str:
    """Generates CCTV video for Case 2: Harbor Berth 14 Perimeter."""
    width, height = 640, 360
    total_frames = duration_sec * fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    for frame_idx in range(total_frames):
        t = frame_idx / fps
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (15, 20, 28)

        cv2.rectangle(frame, (380, 60), (620, 280), (30, 60, 110), -1)
        cv2.putText(frame, "CONTAINER C-3", (400, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 190, 230), 1)

        for x in range(20, 320, 20):
            cv2.line(frame, (x, 100), (x, 290), (45, 55, 68), 1)

        intruder_x = int(140 + t * 25)
        intruder_y = 210
        cv2.rectangle(frame, (intruder_x - 14, intruder_y - 40), (intruder_x + 14, intruder_y + 40), (30, 35, 42), -1)
        cv2.circle(frame, (intruder_x, intruder_y - 45), 11, (50, 55, 65), -1)

        if 4.0 <= t <= 4.5:
            cv2.circle(frame, (intruder_x + 25, intruder_y - 20), 18, (120, 240, 255), -1)
            cv2.putText(frame, "MUZZLE FLASH", (intruder_x - 30, intruder_y - 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 80, 255), 1)

        cv2.rectangle(frame, (intruder_x - 20, intruder_y - 60), (intruder_x + 20, intruder_y + 45), (0, 180, 255), 2)
        cv2.putText(frame, "INTRUDER #1 [PC 459]", (intruder_x - 20, intruder_y - 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 180, 255), 1)

        timestamp_str = f"CAM-08 [CARGO BERTH 14] | 2026-10-23 02:18:{40 + int(t):02d} EST"
        cv2.putText(frame, "● REC [HARBOR_NET]", (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 60, 240), 1)
        cv2.putText(frame, timestamp_str, (170, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 230, 245), 1)
        cv2.putText(frame, f"FPS: {fps}.0 | FRAME: {frame_idx:04d} | AI TRACK: ACTIVE",
                    (20, height - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 240, 255), 1)

        out.write(frame)

    out.release()
    return filepath


def get_preloaded_cases() -> Dict[str, Dict[str, Any]]:
    """Returns the dictionary of complete turnkey sample forensic cases."""
    assets_dir = ensure_asset_dir()
    
    img_case1 = os.path.join(assets_dir, "case1_crime_scene.jpg")
    aud_case1 = os.path.join(assets_dir, "case1_witness_audio.wav")
    vid_case1 = os.path.join(assets_dir, "case1_cctv_alley.mp4")

    img_case2 = os.path.join(assets_dir, "case2_crime_scene.jpg")
    aud_case2 = os.path.join(assets_dir, "case2_witness_audio.wav")
    vid_case2 = os.path.join(assets_dir, "case2_cctv_berth.mp4")

    if not os.path.exists(img_case1):
        generate_crime_scene_image_case1(img_case1)
    if not os.path.exists(aud_case1):
        generate_audio_file(aud_case1, duration_sec=16, freq_type="dispatch")
    if not os.path.exists(vid_case1):
        generate_video_file_case1(vid_case1, duration_sec=8, fps=10)

    if not os.path.exists(img_case2):
        generate_crime_scene_image_case2(img_case2)
    if not os.path.exists(aud_case2):
        generate_audio_file(aud_case2, duration_sec=14, freq_type="harbor")
    if not os.path.exists(vid_case2):
        generate_video_file_case2(vid_case2, duration_sec=8, fps=10)

    cases = {
        "CASE-2026-CR-8841": {
            "case_id": "CASE-2026-CR-8841",
            "title": "Armed Robbery & Battery at Apex Jewelry Vault",
            "classification": "Armed Robbery (PC § 211)",
            "threat_level": "CRITICAL",
            "incident_datetime": "2026-10-24 23:42:15 EST",
            "location": "Apex Fine Jewelry, 482 Grand Avenue, District 4",
            "lead_investigator": "Det. Marcus Vance (Badge #8421)",
            "agency": "Metropolitan Police Dept - Major Crimes Division",
            "image_path": img_case1,
            "audio_path": aud_case1,
            "video_path": vid_case1,
            "image_detections": [
                {
                    "class_name": "person_suspect",
                    "label": "Suspect (Armed/Masked)",
                    "category": "Suspect Identification",
                    "confidence": 0.942,
                    "box": [420, 180, 560, 490],
                    "norm_box": [0.437, 0.281, 0.583, 0.765],
                    "threat": "CRITICAL",
                    "penal_code": "PC 211",
                    "notes": "Male adult, dark balaclava, hooded tactical jacket, brandishing firearm"
                },
                {
                    "class_name": "firearm_handgun",
                    "label": "Handgun (Semi-Auto)",
                    "category": "Ballistics / Weapon",
                    "confidence": 0.968,
                    "box": [680, 420, 740, 480],
                    "norm_box": [0.708, 0.656, 0.771, 0.750],
                    "threat": "CRITICAL",
                    "penal_code": "PC 245(a)(2)",
                    "notes": "Black compact polymer frame semi-automatic pistol, slide locked back"
                },
                {
                    "class_name": "firearm_casing",
                    "label": "Spent Casing (9mm Luger)",
                    "category": "Ballistics / Evidence",
                    "confidence": 0.895,
                    "box": [755, 445, 780, 465],
                    "norm_box": [0.786, 0.695, 0.812, 0.726],
                    "threat": "HIGH",
                    "penal_code": "PC 245",
                    "notes": "Brass 9x19mm headstamp, corroborates single discharge event"
                },
                {
                    "class_name": "forced_entry",
                    "label": "Forced Entry (Pried Deadbolt)",
                    "category": "Point of Entry",
                    "confidence": 0.923,
                    "box": [800, 240, 915, 330],
                    "norm_box": [0.833, 0.375, 0.953, 0.515],
                    "threat": "HIGH",
                    "penal_code": "PC 459",
                    "notes": "Sheared secondary strike plate, fresh tool impressions matching pry bar"
                },
                {
                    "class_name": "blood_spatter",
                    "label": "Blood Spatter (Impact Pattern)",
                    "category": "Serology & Spatter",
                    "confidence": 0.887,
                    "box": [290, 330, 390, 430],
                    "norm_box": [0.302, 0.515, 0.406, 0.672],
                    "threat": "CRITICAL",
                    "penal_code": "PC 242",
                    "notes": "Radial distribution indicative of blunt trauma or gunshot trajectory"
                }
            ],
            "audio_transcript": [
                {
                    "timestamp": "00:02",
                    "speaker": "Speaker 1 (911 Dispatcher)",
                    "text": "911 Emergency, state your location and emergency.",
                    "sentiment": "Calm / Authoritative",
                    "stress_level": 15,
                    "entities": []
                },
                {
                    "timestamp": "00:06",
                    "speaker": "Speaker 2 (Store Manager - Witness)",
                    "text": "Apex Jewelry, 482 Grand Avenue! We are undergoing an armed robbery right now!",
                    "sentiment": "High Panic",
                    "stress_level": 92,
                    "entities": ["Apex Jewelry", "482 Grand Avenue", "Armed Robbery"]
                },
                {
                    "timestamp": "00:10",
                    "speaker": "Speaker 2 (Store Manager - Witness)",
                    "text": "A masked man just kicked open the rear vault door and pulled a black semi-automatic pistol!",
                    "sentiment": "Severe Distress",
                    "stress_level": 96,
                    "entities": ["Masked Suspect", "Rear Vault Door", "Black Semi-Automatic Pistol"]
                },
                {
                    "timestamp": "00:15",
                    "speaker": "Speaker 2 (Store Manager - Witness)",
                    "text": "He smashed the center glass cases, struck the security guard, and shoved diamond trays into a dark duffel bag!",
                    "sentiment": "Severe Distress",
                    "stress_level": 94,
                    "entities": ["Center Glass Cases", "Security Guard", "Diamond Trays", "Dark Duffel Bag"]
                },
                {
                    "timestamp": "00:20",
                    "speaker": "Speaker 1 (911 Dispatcher)",
                    "text": "Units are in route Code 3. Which direction did the suspect flee?",
                    "sentiment": "Urgent Command",
                    "stress_level": 40,
                    "entities": ["Units En Route Code 3"]
                },
                {
                    "timestamp": "00:24",
                    "speaker": "Speaker 2 (Store Manager - Witness)",
                    "text": "He ran out into the east alleyway and jumped into a dark grey sedan heading eastbound toward Highway 9!",
                    "sentiment": "Panic / High Adrenaline",
                    "stress_level": 88,
                    "entities": ["East Alleyway", "Dark Grey Sedan", "Eastbound Highway 9"]
                }
            ],
            "video_events": [
                {
                    "timestamp": "00:02",
                    "frame_sec": 2.0,
                    "event_description": "Dark grey 4-door sedan arrives with headlights extinguished; idles in rear loading bay.",
                    "penal_code": "PC 459 (Commercial Burglary - Prep)",
                    "severity": "MEDIUM",
                    "motion_velocity": "3.2 km/h",
                    "velocity_kmh": 3.2,
                    "confidence": 0.91
                },
                {
                    "timestamp": "00:05",
                    "frame_sec": 5.0,
                    "event_description": "Suspect (black hoodie, balaclava) disembarks and approaches service entrance with leverage tool.",
                    "penal_code": "PC 459 (Forced Intrusion)",
                    "severity": "HIGH",
                    "motion_velocity": "7.8 km/h",
                    "velocity_kmh": 7.8,
                    "confidence": 0.95
                },
                {
                    "timestamp": "00:08",
                    "frame_sec": 8.0,
                    "event_description": "Suspect draws concealed firearm from waistband, forces entry through deadbolt latch.",
                    "penal_code": "PC 211 / PC 245(a)(2) (Armed Robbery / Assault with Firearm)",
                    "severity": "CRITICAL",
                    "motion_velocity": "9.4 km/h",
                    "velocity_kmh": 9.4,
                    "confidence": 0.97
                },
                {
                    "timestamp": "00:11",
                    "frame_sec": 11.0,
                    "event_description": "Physical confrontation detected; victim shoved to ground near east display case.",
                    "penal_code": "PC 242 (Battery with Aggravation)",
                    "severity": "CRITICAL",
                    "motion_velocity": "14.2 km/h",
                    "velocity_kmh": 14.2,
                    "confidence": 0.93
                },
                {
                    "timestamp": "00:14",
                    "frame_sec": 14.0,
                    "event_description": "Suspect re-emerges carrying loaded duffel; enters vehicle which accelerates at high velocity eastbound.",
                    "penal_code": "PC 148(a)(1) (Evading Arrest - Felonious Flight)",
                    "severity": "HIGH",
                    "motion_velocity": "58.0 km/h",
                    "velocity_kmh": 58.0,
                    "confidence": 0.96
                }
            ],
            "investigative_leads": [
                "Issue BOLO (Be On the Lookout) for late-model dark grey sedan with front passenger-side alloy rim damage, last seen speeding eastbound toward Highway 9 corridor.",
                "Ballistics processing: Fast-track NIBIN database entry for 9mm Luger shell casing [EVD-IMG-2026-001 / Casing #2] to cross-reference recent local shooting incidents.",
                "DNA / Serological profiling: Swab pry marks on secondary door latch [EVD-IMG-2026-001 / Marker #3] for touch DNA deposited during mechanical forced entry.",
                "Impound and preserve CCTV camera feeds along Grand Ave & 5th Street intersection between 23:40 and 23:50 EST to recover getaway license plate sequence.",
                "Subpoena regional cell tower dumps (Apex cell sector 4B) for active IMSI registrations between 23:35 and 23:50 EST."
            ]
        },
        "CASE-2026-CR-4192": {
            "case_id": "CASE-2026-CR-4192",
            "title": "Midnight Commercial Burglary & Weapon Discharge",
            "classification": "Commercial Burglary (PC § 459)",
            "threat_level": "HIGH",
            "incident_datetime": "2026-10-23 02:18:40 EST",
            "location": "Nexus Logistics Cargo Berth 14, Industrial Harbor",
            "lead_investigator": "Det. Marcus Vance (Badge #8421)",
            "agency": "Metropolitan Police Dept - Major Crimes Division",
            "image_path": img_case2,
            "audio_path": aud_case2,
            "video_path": vid_case2,
            "image_detections": [
                {
                    "class_name": "forced_entry",
                    "label": "Hydraulic Bolt-Cutter Breach (Perimeter Fence)",
                    "category": "Point of Entry",
                    "confidence": 0.954,
                    "box": [220, 260, 360, 480],
                    "norm_box": [0.229, 0.406, 0.375, 0.750],
                    "threat": "HIGH",
                    "penal_code": "PC 459",
                    "notes": "Industrial chain link severed using heavy hydraulic jaws; tool discarded at fence base"
                },
                {
                    "class_name": "firearm_casing",
                    "label": "Spent .45 ACP Casing (Federal Hydra-Shok)",
                    "category": "Ballistics / Evidence",
                    "confidence": 0.928,
                    "box": [510, 410, 545, 435],
                    "norm_box": [0.531, 0.640, 0.567, 0.679],
                    "threat": "CRITICAL",
                    "penal_code": "PC 245(a)(2)",
                    "notes": "Heavy caliber .45 Auto spent casing recovered on asphalt 4 meters from container C-3"
                },
                {
                    "class_name": "forced_entry",
                    "label": "Bullet Defect (Container C-3 Steel Siding)",
                    "category": "Ballistics / Structural",
                    "confidence": 0.912,
                    "box": [705, 265, 740, 300],
                    "norm_box": [0.734, 0.414, 0.771, 0.468],
                    "threat": "CRITICAL",
                    "penal_code": "PC 245",
                    "notes": "Penetrating entry defect with lead wipe and striations angled downward at 12 degrees"
                }
            ],
            "audio_transcript": [
                {
                    "timestamp": "00:03",
                    "speaker": "Speaker 1 (Harbor Security Guard)",
                    "text": "Control, Berth 14 security. We have an active intrusion alert along the south perimeter fence.",
                    "sentiment": "Tense",
                    "stress_level": 68,
                    "entities": ["Berth 14", "South Perimeter Fence", "Intrusion Alert"]
                },
                {
                    "timestamp": "00:07",
                    "speaker": "Speaker 1 (Harbor Security Guard)",
                    "text": "Two individuals cutting chain link with heavy bolt cutters! They are wearing dark jumpsuits and masks!",
                    "sentiment": "High Urgency",
                    "stress_level": 84,
                    "entities": ["Two Individuals", "Bolt Cutters", "Dark Jumpsuits", "Masks"]
                },
                {
                    "timestamp": "00:11",
                    "speaker": "Speaker 1 (Harbor Security Guard)",
                    "text": "Shot fired! Repeat, single gunshot discharged near shipping container C-3! I am taking cover behind forklift 4!",
                    "sentiment": "Acute Terror",
                    "stress_level": 98,
                    "entities": ["Gunshot Discharged", "Container C-3", "Taking Cover", "Forklift 4"]
                },
                {
                    "timestamp": "00:16",
                    "speaker": "Speaker 2 (Central Dispatch)",
                    "text": "All available harbor patrol units respond Code 3 to Berth 14. Harbor Gate 2 is being sealed.",
                    "sentiment": "Authoritative",
                    "stress_level": 35,
                    "entities": ["Harbor Patrol Units Code 3", "Harbor Gate 2"]
                },
                {
                    "timestamp": "00:20",
                    "speaker": "Speaker 1 (Harbor Security Guard)",
                    "text": "Suspects fled on foot along the seawall towards Pier 7! They dropped the bolt cutters on the pavement!",
                    "sentiment": "Adrenaline Surge",
                    "stress_level": 89,
                    "entities": ["Fled On Foot", "Seawall", "Pier 7", "Dropped Bolt Cutters"]
                }
            ],
            "video_events": [
                {
                    "timestamp": "00:02",
                    "frame_sec": 2.0,
                    "event_description": "Perimeter chain link fence severed by two individuals carrying industrial hydraulic cutter.",
                    "penal_code": "PC 459 (Burglary & Forced Entry)",
                    "severity": "HIGH",
                    "motion_velocity": "4.2 km/h",
                    "velocity_kmh": 4.2,
                    "confidence": 0.94
                },
                {
                    "timestamp": "00:05",
                    "frame_sec": 5.0,
                    "event_description": "Intruders enter Berth 14 staging apron moving toward high-value electronics container C-3.",
                    "penal_code": "PC 459 (Unlawful Entry)",
                    "severity": "HIGH",
                    "motion_velocity": "7.5 km/h",
                    "velocity_kmh": 7.5,
                    "confidence": 0.95
                },
                {
                    "timestamp": "00:08",
                    "frame_sec": 8.0,
                    "event_description": "Muzzle flash detected at north corner of container C-3; projectile strikes steel siding.",
                    "penal_code": "PC 245(a)(2) (Assault with Deadly Weapon / Firearm Discharge)",
                    "severity": "CRITICAL",
                    "motion_velocity": "11.2 km/h",
                    "velocity_kmh": 11.2,
                    "confidence": 0.98
                },
                {
                    "timestamp": "00:12",
                    "frame_sec": 12.0,
                    "event_description": "Security guard retreats behind forklift; intruders abandon tools and flee along seawall at rapid pace.",
                    "penal_code": "PC 148(a)(1) (Evading Security & Law Enforcement)",
                    "severity": "HIGH",
                    "motion_velocity": "24.6 km/h",
                    "velocity_kmh": 24.6,
                    "confidence": 0.96
                }
            ],
            "investigative_leads": [
                "Tool-mark impression analysis: Process cutting blades of abandoned bolt cutters against AFTE reference collection.",
                "Ballistics extraction: Safely extract .45 caliber copper-jacketed bullet core lodged in container C-3 corrugated siding.",
                "Harbor perimeter surveillance: Subpoena Pier 7 maritime cameras and tugboat logs between 02:15 and 02:35 EST.",
                "DNA swabbing: Swab rubberized handles of hydraulic bolt cutters for touch epithelial cells.",
                "Access control audit: Review Berth 14 electronic badge swiping logs for employee credential cloning."
            ]
        }
    }
    return cases
