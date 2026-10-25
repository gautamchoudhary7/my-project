"""
CrimeVision AI - Forensic Chain of Custody & Cryptographic Integrity Module
Maintains tamper-evident SHA-256 hashing and chronological chain of custody logs.
"""
import hashlib
import datetime
from typing import List, Dict, Any, Optional
import pandas as pd


def compute_sha256(data: bytes) -> str:
    """Computes a standard hexadecimal SHA-256 hash of raw byte data."""
    if not data:
        return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def generate_evidence_id(category: str, sequence_num: int, case_year: str = "2026") -> str:
    """Generates a standardized judicial evidence identifier."""
    prefix_map = {
        "image": "EVD-IMG",
        "audio": "EVD-AUD",
        "video": "EVD-VID",
        "report": "EVD-REP",
        "physical": "EVD-PHY"
    }
    prefix = prefix_map.get(category.lower(), "EVD-GEN")
    return f"{prefix}-{case_year}-{sequence_num:03d}"


class ChainOfCustodyTracker:
    """Manages the legal chain-of-custody log for forensic items in a case."""

    def __init__(self, case_id: str, lead_investigator: str, agency: str):
        self.case_id = case_id
        self.lead_investigator = lead_investigator
        self.agency = agency
        self.log_entries: List[Dict[str, Any]] = []

    def record_event(
        self,
        evidence_id: str,
        action: str,
        custodian: str,
        sha256_hash: str,
        notes: str,
        status: str = "VERIFIED",
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Appends a tamper-evident chain of custody event."""
        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        entry = {
            "entry_index": len(self.log_entries) + 1,
            "evidence_id": evidence_id,
            "timestamp": timestamp,
            "action": action,
            "custodian": custodian,
            "sha256_hash": sha256_hash,
            "status": status,
            "notes": notes
        }
        self.log_entries.append(entry)
        return entry

    def verify_item(self, evidence_id: str, current_bytes: bytes) -> Dict[str, Any]:
        """Checks if current item bytes match the initially logged SHA-256 hash."""
        current_hash = compute_sha256(current_bytes)
        initial_entry = next((e for e in self.log_entries if e["evidence_id"] == evidence_id), None)
        
        if not initial_entry:
            return {
                "verified": False,
                "reason": f"No initial custody record found for evidence ID {evidence_id}",
                "current_hash": current_hash
            }

        is_match = (current_hash.lower() == initial_entry["sha256_hash"].lower())
        return {
            "verified": is_match,
            "stored_hash": initial_entry["sha256_hash"],
            "current_hash": current_hash,
            "tamper_detected": not is_match
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Converts custody entries to a Pandas DataFrame for display."""
        if not self.log_entries:
            return pd.DataFrame(columns=[
                "entry_index", "evidence_id", "timestamp", "action", "custodian", "sha256_hash", "status", "notes"
            ])
        return pd.DataFrame(self.log_entries)

    def get_summary(self) -> Dict[str, Any]:
        """Returns statistical summary of custody items."""
        unique_items = len(set(e["evidence_id"] for e in self.log_entries))
        return {
            "total_transactions": len(self.log_entries),
            "unique_evidence_items": unique_items,
            "latest_custodian": self.log_entries[-1]["custodian"] if self.log_entries else self.lead_investigator,
            "last_action_time": self.log_entries[-1]["timestamp"] if self.log_entries else "N/A"
        }
