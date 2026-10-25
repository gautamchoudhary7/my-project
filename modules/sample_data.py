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
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, List


def ensure_asset_dir(assets_dir: str = "assets") -> str:
    """Ensures assets directory exists and returns absolute path."""
    os.makedirs(assets_dir, exist_ok=True)
    return assets_dir


def generate_crime_scene_image(filepath: str, case_title: str) -> str:
    """Generates a realistic forensic crime scene photography image with markers."""
    width, height = 960, 640
    # Background: dark interior warehouse / room with subtle concrete texture
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (35, 38, 48)  # Slate dark floor

    # Draw tiled floor grid
    for x in range(0, width, 60):
        cv2.line(img, (x, 0), (x, height), (45, 50, 62), 1)
    for y in range(0, height, 60):
        cv2.line(img, (0, y), (width, y), (45, 50, 62), 1)

    # Draw broken glass shards on floor (Point of Entry)
    np.random.seed(42)
    for _ in range(35):
        pt1 = (np.random.randint(480, 720), np.random.randint(300, 520))
        pt2 = (pt1[0] + np.random.randint(-15, 15), pt1[1] + np.random.randint(-15, 15))
        pt3 = (pt1[0] + np.random.randint(-15, 15), pt1[1] + np.random.randint(-15, 15))
        cv2.fillPoly(img, [np.array([pt1, pt2, pt3])], (160, 190, 210))
        cv2.polylines(img, [np.array([pt1, pt2, pt3])], True, (210, 230, 255), 1)

    # Draw blood spatter pattern (Serology)
    center_spatter = (320, 380)
    for _ in range(45):
        rad = np.random.uniform(2, 65)
        angle = np.random.uniform(0, 2 * np.pi)
        sx = int(center_spatter[0] + rad * np.cos(angle))
        sy = int(center_spatter[1] + rad * np.sin(angle) * 0.7)
        size = np.random.randint(2, 6)
        cv2.circle(img, (sx, sy), size, (25, 25, 160), -1)
    cv2.ellipse(img, center_spatter, (28, 16), 25, 0, 360, (20, 20, 140), -1)

    # Draw firearm (Handgun silhouette) on pavement
    gun_pts = np.array([
        [680, 420], [740, 420], [740, 440], [715, 440], [710, 480], [690, 475], [698, 440], [680, 440]
    ], np.int32)
    cv2.fillPoly(img, [gun_pts], (20, 20, 25))
    cv2.polylines(img, [gun_pts], True, (60, 60, 70), 2)

    # Draw spent 9mm casing near gun
    casing_rect = (760, 450, 12, 6)
    cv2.rectangle(img, (casing_rect[0], casing_rect[1]),
                  (casing_rect[0] + casing_rect[2], casing_rect[1] + casing_rect[3]), (50, 170, 220), -1)

    # Draw pried door frame / entry point on top right
    cv2.rectangle(img, (800, 80), (920, 520), (55, 60, 75), -1)
    cv2.rectangle(img, (805, 85), (915, 515), (25, 28, 38), -1)
    # Pry mark with splintered wood/metal
    cv2.line(img, (802, 280), (810, 310), (120, 130, 140), 4)

    # Draw yellow forensic evidence cones (#1, #2, #3, #4)
    def draw_evidence_cone(x, y, num):
        # Yellow triangle cone
        pts = np.array([[x, y], [x - 24, y + 42], [x + 24, y + 42]], np.int32)
        cv2.fillPoly(img, [pts], (20, 210, 240))  # BGR yellow
        cv2.polylines(img, [pts], True, (10, 150, 180), 2)
        cv2.putText(img, str(num), (x - 7, y + 33), cv2.FONT_HERSHEY_DUPLEX, 0.9, (15, 15, 20), 2)

    draw_evidence_cone(725, 370, 1)  # Firearm cone
    draw_evidence_cone(785, 405, 2)  # Casing cone
    draw_evidence_cone(830, 240, 3)  # Forced Entry cone
    draw_evidence_cone(320, 310, 4)  # Blood Spatter cone

    # Top banner: Police Department Crime Scene Header & Scale Bar
    cv2.rectangle(img, (0, 0), (width, 45), (15, 18, 25), -1)
    cv2.line(img, (0, 45), (width, 45), (0, 240, 255), 2)
    cv2.putText(img, f"METROPOLITAN POLICE DEPT - CRIME SCENE INVESTIGATION DIVISION | {case_title.upper()}",
                (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 240, 255), 1)

    # Bottom scale bar
    cv2.rectangle(img, (width - 240, height - 35), (width - 20, height - 15), (20, 25, 35), -1)
    for i in range(10):
        color = (240, 240, 240) if i % 2 == 0 else (30, 30, 30)
        cv2.rectangle(img, (width - 235 + i * 21, height - 32), (width - 235 + (i + 1) * 21, height - 18), color, -1)
    cv2.putText(img, "FORENSIC SCALE (10cm)", (width - 235, height - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 175, 195), 1)

    cv2.imwrite(filepath, img)
    return filepath


def generate_audio_file(filepath: str, duration_sec: int = 15) -> str:
    """Generates a synthetic realistic dispatch/witness WAV audio file."""
    sample_rate = 44100
    num_samples = sample_rate * duration_sec
    channels = 1
    sampwidth = 2

    # Open wav file for writing
    with wave.open(filepath, 'w') as wav:
        wav.setparams((channels, sampwidth, sample_rate, num_samples, 'NONE', 'not compressed'))
        frames = bytearray()

        for i in range(num_samples):
            t = float(i) / sample_rate
            # Simulated emergency radio audio with carrier wave, squelch, and modulation
            carrier = 0.08 * math.sin(2.0 * math.pi * 440.0 * t)  # Beep tone
            speech_sim = 0.45 * (
                math.sin(2.0 * math.pi * 220.0 * t + math.sin(2.0 * math.pi * 5.0 * t)) *
                math.sin(2.0 * math.pi * 600.0 * t) *
                math.exp(-((t % 2.5 - 1.2) ** 2) / 0.5)
            )
            # Add subtle radio hiss
            noise = 0.02 * ((hash(i) % 2000) / 1000.0 - 1.0)
            
            # Dispatch radio burst at t = 0 to 0.4 and 7.0 to 7.3
            burst = 0.25 * math.sin(2.0 * math.pi * 1200.0 * t) if (t < 0.3 or (7.0 < t < 7.3)) else 0.0

            sample = carrier + speech_sim + noise + burst
            sample = max(-0.95, min(0.95, sample))
            ival = int(sample * 32767.0)
            frames.extend(struct.pack('<h', ival))

        wav.writeframes(frames)
    return filepath


def generate_video_file(filepath: str, duration_sec: int = 8, fps: int = 10) -> str:
    """Generates a realistic CCTV surveillance MP4 video file with tracking overlays."""
    width, height = 640, 360
    total_frames = duration_sec * fps
    
    # Use mp4v or avc1 codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    for frame_idx in range(total_frames):
        t = frame_idx / fps
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 24, 32)  # Low-light alleyway ambience

        # Draw alley walls & ground
        cv2.line(frame, (0, 240), (width, 240), (45, 52, 65), 2)
        cv2.line(frame, (120, 0), (120, 240), (35, 40, 50), 2)
        cv2.line(frame, (520, 0), (520, 240), (35, 40, 50), 2)

        # Draw getaway vehicle at top alleyway (idling or moving away)
        car_x = int(140 + t * 45)
        car_y = 190
        cv2.rectangle(frame, (car_x, car_y), (car_x + 95, car_y + 35), (55, 60, 68), -1)
        # Car tail lights red
        cv2.circle(frame, (car_x + 90, car_y + 12), 4, (30, 30, 220), -1)
        cv2.circle(frame, (car_x + 90, car_y + 24), 4, (30, 30, 220), -1)

        # Suspect motion: enters from right, approaches, brandishes, flees
        suspect_x = int(480 - t * 35) if t < 4.0 else int(340 + (t - 4.0) * 55)
        suspect_y = 180
        # Suspect bounding box simulation
        cv2.rectangle(frame, (suspect_x - 18, suspect_y - 50), (suspect_x + 18, suspect_y + 50), (40, 45, 55), -1)
        # Head
        cv2.circle(frame, (suspect_x, suspect_y - 55), 14, (70, 75, 85), -1)

        # AI Object Detection Tracking Box
        box_color = (0, 0, 255) if (2.5 <= t <= 5.5) else (0, 240, 255)
        label = "PERSON: SUSPECT [WEAPON BRANDISHED]" if (2.5 <= t <= 5.5) else "PERSON: SUSPECT #1"
        cv2.rectangle(frame, (suspect_x - 24, suspect_y - 75), (suspect_x + 24, suspect_y + 55), box_color, 2)
        cv2.rectangle(frame, (suspect_x - 24, suspect_y - 95), (suspect_x + 130, suspect_y - 75), box_color, -1)
        cv2.putText(frame, label, (suspect_x - 20, suspect_y - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.32, (10, 10, 15), 1)

        # CCTV camera HUD overlay
        timestamp_str = f"CAM-04 [REAR ALLEY] | 2026-10-24 23:42:{15 + int(t):02d} EST"
        cv2.putText(frame, "● REC [LIVE_FEED]", (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 60, 240), 1)
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

    # Generate synthetic sample files if they do not exist
    if not os.path.exists(img_case1):
        generate_crime_scene_image(img_case1, "Apex Jewelry Vault Robbery")
    if not os.path.exists(aud_case1):
        generate_audio_file(aud_case1, duration_sec=16)
    if not os.path.exists(vid_case1):
        generate_video_file(vid_case1, duration_sec=8, fps=10)

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
                    "confidence": 0.91
                },
                {
                    "timestamp": "00:05",
                    "frame_sec": 5.0,
                    "event_description": "Suspect (black hoodie, balaclava) disembarks and approaches service entrance with leverage tool.",
                    "penal_code": "PC 459 (Forced Intrusion)",
                    "severity": "HIGH",
                    "motion_velocity": "7.8 km/h",
                    "confidence": 0.95
                },
                {
                    "timestamp": "00:08",
                    "frame_sec": 8.0,
                    "event_description": "Suspect draws concealed firearm from waistband, forces entry through deadbolt latch.",
                    "penal_code": "PC 211 / PC 245(a)(2) (Armed Robbery / Assault with Firearm)",
                    "severity": "CRITICAL",
                    "motion_velocity": "9.4 km/h",
                    "confidence": 0.97
                },
                {
                    "timestamp": "00:11",
                    "frame_sec": 11.0,
                    "event_description": "Physical confrontation detected; victim shoved to ground near east display case.",
                    "penal_code": "PC 242 (Battery with Aggravation)",
                    "severity": "CRITICAL",
                    "motion_velocity": "14.2 km/h",
                    "confidence": 0.93
                },
                {
                    "timestamp": "00:14",
                    "frame_sec": 14.0,
                    "event_description": "Suspect re-emerges carrying loaded duffel; enters vehicle which accelerates at high velocity eastbound.",
                    "penal_code": "PC 148(a)(1) (Evading Arrest - Felonious Flight)",
                    "severity": "HIGH",
                    "motion_velocity": "58.0 km/h",
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
            "image_path": img_case1,
            "audio_path": aud_case1,
            "video_path": vid_case1,
            "image_detections": [
                {
                    "class_name": "forced_entry",
                    "label": "Broken Perimeter Hasps",
                    "category": "Point of Entry",
                    "confidence": 0.941,
                    "box": [500, 200, 680, 360],
                    "norm_box": [0.521, 0.312, 0.708, 0.562],
                    "threat": "HIGH",
                    "penal_code": "PC 459",
                    "notes": "Hydraulic bolt-cutter shears detected on heavy galvanized chain"
                },
                {
                    "class_name": "firearm_casing",
                    "label": "Spent .45 ACP Casing",
                    "category": "Ballistics / Evidence",
                    "confidence": 0.912,
                    "box": [620, 380, 650, 410],
                    "norm_box": [0.645, 0.593, 0.677, 0.640],
                    "threat": "CRITICAL",
                    "penal_code": "PC 245",
                    "notes": "Federal Hydra-Shok casing recovered adjacent to perimeter gate"
                }
            ],
            "audio_transcript": [
                {
                    "timestamp": "00:03",
                    "speaker": "Speaker 1 (Harbor Security)",
                    "text": "Control, we have an intrusion alert at Berth 14 fence line.",
                    "sentiment": "Tense",
                    "stress_level": 65,
                    "entities": ["Berth 14", "Intrusion Alert"]
                },
                {
                    "timestamp": "00:08",
                    "speaker": "Speaker 1 (Harbor Security)",
                    "text": "Shot fired! Repeat, single gunshot heard near container stack C-3! Requesting immediate police backup!",
                    "sentiment": "Extreme Danger",
                    "stress_level": 98,
                    "entities": ["Gunshot Discharged", "Container Stack C-3", "Request Backup"]
                }
            ],
            "video_events": [
                {
                    "timestamp": "00:02",
                    "frame_sec": 2.0,
                    "event_description": "Perimeter fence breached via bolt-cutters by two individuals in dark clothing.",
                    "penal_code": "PC 459 (Burglary)",
                    "severity": "HIGH",
                    "motion_velocity": "4.5 km/h",
                    "confidence": 0.94
                },
                {
                    "timestamp": "00:07",
                    "frame_sec": 7.0,
                    "event_description": "Muzzle flash detected at north angle of container row; security guard retreats.",
                    "penal_code": "PC 245(a)(2) (Assault with Deadly Weapon)",
                    "severity": "CRITICAL",
                    "motion_velocity": "11.2 km/h",
                    "confidence": 0.98
                }
            ],
            "investigative_leads": [
                "Process hydraulic bolt cutter tool markings against forensic tool-mark database.",
                "Scan harbor gate RFID logs for unauthorized badge scans within 30 minutes of incident.",
                "Recover spent .45 caliber projectile from shipping container steel siding."
            ]
        }
    }
    return cases
