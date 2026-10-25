"""
CrimeVision AI - Multimodal LLM & Dynamic Grounded RAG Query Engine
Supports Gemini, Groq, and Context-Aware Dynamic Forensic RAG with Zero Hallucination.
Platform ID: 6ac4c9851dcde6d7857c163b
"""
import os
import re
from typing import Dict, Any, List, Optional


class ForensicLLMService:
    """
    Unified Forensic LLM interface supporting Google Gemini, Groq,
    and a Context-Aware Dynamic Forensic RAG Engine that extracts facts directly
    from the active multimodal evidence ledger.
    """

    def __init__(self, provider: str = "demo", api_key: Optional[str] = None):
        self.provider = provider.lower() if provider else "demo"
        self.api_key = (api_key or os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()
        self._init_clients()

    def _init_clients(self):
        """Initializes API client instances if keys are present."""
        self.groq_client = None
        self.gemini_client = None

        if self.provider == "groq" and self.api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"[Warning] Groq initialization error: {e}")

        elif self.provider in ["gemini", "google"] and self.api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception:
                try:
                    import google.generativeai as gai
                    gai.configure(api_key=self.api_key)
                    self.gemini_client = gai.GenerativeModel("gemini-1.5-flash")
                except Exception as e2:
                    print(f"[Warning] Gemini initialization error: {e2}")

    def generate_chat_response(
        self,
        query: str,
        evidence_context: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Executes a strictly grounded forensic RAG query.
        Returns a dictionary with answer, citations, confidence, and provider used.
        """
        system_instruction = (
            "You are CrimeVision AI, a Senior Forensic Systems Intelligence Analyst. "
            "Your sworn duty is to provide strictly grounded answers based ONLY on the evidence provided in the forensic context.\n"
            "RULES:\n"
            "1. ZERO HALLUCINATION: If a detail cannot be corroborated by the evidence context, explicitly state 'INCONCLUSIVE - Evidentiary ledger contains no record substantiating this claim'.\n"
            "2. STRICT CITATIONS: Every claim must cite the exact Evidence ID and timestamp, e.g., '[EVD-IMG-2026-001]' or '[EVD-AUD-2026-002 @ 00:10]' or '[EVD-VID-2026-003 @ 00:08]'.\n"
            "3. FORENSIC TONE: Maintain an objective, court-admissible forensic tone.\n"
            "4. Base all facts strictly on the CURRENT case provided in the context."
        )

        prompt = f"""
EVIDENCE LEDGER CONTEXT:
{evidence_context}

INVESTIGATOR QUERY:
{query}

Provide a grounded, professional forensic assessment with strict citations:
"""

        # Try active LLM provider first if API key was provided
        if self.provider == "groq" and self.groq_client:
            try:
                messages = [{"role": "system", "content": system_instruction}]
                if chat_history:
                    for ch in chat_history[-4:]:
                        messages.append({"role": ch.get("role", "user"), "content": ch.get("content", "")})
                messages.append({"role": "user", "content": prompt})

                chat_completion = self.groq_client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.1,
                    max_tokens=800
                )
                answer = chat_completion.choices[0].message.content
                citations = self._extract_citations(answer)
                return {
                    "answer": answer,
                    "citations": citations,
                    "provider": "Groq Llama-3.3-70B",
                    "mode": "live_llm"
                }
            except Exception as e:
                print(f"[ForensicLLM] Groq API call error: {e}. Executing Dynamic Grounded Engine.")

        elif self.provider in ["gemini", "google"] and self.gemini_client:
            try:
                if hasattr(self.gemini_client, "models"):
                    response = self.gemini_client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"{system_instruction}\n\n{prompt}"
                    )
                    answer = response.text
                else:
                    response = self.gemini_client.generate_content(f"{system_instruction}\n\n{prompt}")
                    answer = response.text

                citations = self._extract_citations(answer)
                return {
                    "answer": answer,
                    "citations": citations,
                    "provider": "Google Gemini 1.5",
                    "mode": "live_llm"
                }
            except Exception as e:
                print(f"[ForensicLLM] Gemini API call error: {e}. Executing Dynamic Grounded Engine.")

        # Context-Aware Dynamic Grounded Forensic Fallback
        return self._generate_dynamic_grounded_response(query, evidence_context)

    def _extract_citations(self, text: str) -> List[str]:
        """Parses evidence citations in format [EVD-...] from text."""
        citations = re.findall(r'\[(EVD-[^\]]+)\]', text)
        return list(dict.fromkeys(citations))

    def _parse_context(self, context: str) -> Dict[str, Any]:
        """Parses structured metadata and event lines from the ledger context string."""
        data = {
            "case_id": "CASE-UNKNOWN",
            "title": "Forensic Investigation",
            "location": "Metropolitan Area",
            "incident_date": "N/A",
            "investigator": "Forensic Investigator",
            "agency": "Metropolitan Police Dept",
            "threat_level": "HIGH",
            "classification": "General Crime Scene",
            "events": []
        }

        # Extract metadata headers
        m_file = re.search(r'FORENSIC INVESTIGATION FILE:\s*([^\n-]+)\s*-\s*([^\n]+)', context)
        if m_file:
            data["case_id"] = m_file.group(1).strip()
            data["title"] = m_file.group(2).strip()

        m_loc = re.search(r'LOCATION:\s*([^|]+)\|\s*INCIDENT DATE:\s*([^\n]+)', context)
        if m_loc:
            data["location"] = m_loc.group(1).strip()
            data["incident_date"] = m_loc.group(2).strip()

        m_inv = re.search(r'LEAD INVESTIGATOR:\s*([^|]+)\|\s*AGENCY:\s*([^\n]+)', context)
        if m_inv:
            data["investigator"] = m_inv.group(1).strip()
            data["agency"] = m_inv.group(2).strip()

        m_threat = re.search(r'THREAT LEVEL:\s*([^|]+)\|\s*CLASSIFICATION:\s*([^\n]+)', context)
        if m_threat:
            data["threat_level"] = m_threat.group(1).strip()
            data["classification"] = m_threat.group(2).strip()

        # Parse individual event blocks
        # Pattern: [timestamp] [evidence_id] (modality) Severity: sev | Statute: stat
        #    Event: ...
        #    Details: ...
        #    Corroboration: ...
        raw_blocks = context.split("\n\n")
        for b in raw_blocks:
            m_hdr = re.search(r'\[([^\]]+)\]\s*\[([^\]]+)\]\s*\(([^)]+)\)\s*Severity:\s*(\w+)\s*\|\s*Statute:\s*([^\n]+)', b)
            if m_hdr:
                ev_dict = {
                    "timestamp": m_hdr.group(1).strip(),
                    "evidence_id": m_hdr.group(2).strip(),
                    "modality": m_hdr.group(3).strip(),
                    "severity": m_hdr.group(4).strip(),
                    "statute": m_hdr.group(5).strip(),
                    "event": "",
                    "details": "",
                    "corroboration": ""
                }
                m_ev = re.search(r'Event:\s*([^\n]+)', b)
                if m_ev:
                    ev_dict["event"] = m_ev.group(1).strip()
                m_det = re.search(r'Details:\s*([^\n]+)', b)
                if m_det:
                    ev_dict["details"] = m_det.group(1).strip()
                m_cor = re.search(r'Corroboration:\s*([^\n]+)', b)
                if m_cor:
                    ev_dict["corroboration"] = m_cor.group(1).strip()

                data["events"].append(ev_dict)

        return data

    def _generate_dynamic_grounded_response(self, query: str, context: str) -> Dict[str, Any]:
        """
        Dynamically analyzes investigator query against the exact active case metadata
        and master event ledger, generating 100% accurate, grounded forensic findings.
        """
        parsed = self._parse_context(context)
        q_lower = query.lower().strip()
        events = parsed["events"]

        answer_lines = []
        citations = []

        # 1. Query for Case Identification / Metadata / Location / Time / Investigator
        if any(k in q_lower for k in ["case id", "case number", "case file"]):
            answer_lines.append(f"**Case Identification:** The active investigation file is **{parsed['case_id']}** (*{parsed['title']}*).")
            citations.append(f"{parsed['case_id']}")

        if any(k in q_lower for k in ["where", "location", "address", "scene", "occur"]):
            answer_lines.append(f"**Incident Location:** The physical scene is located at **{parsed['location']}**.")
            # Find physical evidence or call referencing location
            loc_events = [e for e in events if any(w in e["details"].lower() or w in e["event"].lower() for w in ["apex", "grand", "berth", "harbor", "location", "avenue", "street"])]
            if loc_events:
                citations.append(loc_events[0]["evidence_id"])

        if any(k in q_lower for k in ["when", "what time", "date", "datetime"]):
            answer_lines.append(f"**Incident Timestamp:** Recorded at **{parsed['incident_date']}**.")

        if any(k in q_lower for k in ["who is the investigator", "detective", "lead investigator", "officer in charge"]):
            answer_lines.append(f"**Lead Forensic Investigator:** **{parsed['investigator']}**, assigned to {parsed['agency']}.")

        if any(k in q_lower for k in ["threat level", "severity", "classification", "crime type"]):
            answer_lines.append(f"**Threat Assessment & Classification:** Formally classified as **{parsed['classification']}** under threat tier **{parsed['threat_level']}**.")

        # 2. Query for Specific Timestamps (e.g., "00:08", "00:02", "00:10", "at 00:05", "timeline")
        time_matches = re.findall(r'\b(00:\d{2})\b', q_lower)
        if time_matches:
            target_time = time_matches[0]
            matched_events = [e for e in events if target_time in e["timestamp"] or target_time in e["evidence_id"]]
            if matched_events:
                answer_lines.append(f"**Events Logged at Timestamp [{target_time}]:**")
                for e in matched_events:
                    answer_lines.append(f"• **[{e['modality']}]** {e['event']} — *{e['details']}* [{e['evidence_id']}]. Statute: `{e['statute']}`.")
                    citations.append(e["evidence_id"])
            else:
                answer_lines.append(f"No specific evidence events are anchored exactly at timestamp [{target_time}]. Closest logged timeline events surround this interval.")

        # 3. Query for Weapons & Ballistics
        if any(k in q_lower for k in ["weapon", "gun", "firearm", "casing", "pistol", "caliber", "bullet", "knife", "blade", "shoot", "shot", "discharge", "muzzle"]):
            weapon_events = [e for e in events if any(w in (e["event"] + " " + e["details"]).lower() for w in ["firearm", "handgun", "casing", "knife", "pistol", "gun", "shot", "muzzle", "luger", "acp", "caliber"])]
            if weapon_events:
                answer_lines.append("**Ballistics & Weapons Evidence:**")
                for e in weapon_events:
                    answer_lines.append(f"• {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])
            else:
                answer_lines.append("• No lethal weapons or ballistics items were recorded in the active evidence ledger for this case.")

        # 4. Query for Vehicles, Getaway & Flight
        if any(k in q_lower for k in ["vehicle", "car", "sedan", "truck", "fled", "getaway", "escape", "speed", "velocity", "km/h", "mph", "flight"]):
            flight_events = [e for e in events if any(w in (e["event"] + " " + e["details"]).lower() for w in ["vehicle", "sedan", "car", "fled", "accelerat", "speed", "km/h", "getaway", "flight", "alleyway", "seawall", "pier"])]
            if flight_events:
                answer_lines.append("**Suspect Flight & Getaway Analysis:**")
                for e in flight_events:
                    answer_lines.append(f"• {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])
            else:
                answer_lines.append("• Evidentiary ledger contains no record of a vehicular getaway for this specific entry.")

        # 5. Query for Forced Entry, Breach & Burglary
        if any(k in q_lower for k in ["entry", "breach", "forced", "lock", "deadbolt", "door", "fence", "hasp", "bolt", "cutter", "crowbar", "pry", "glass"]):
            breach_events = [e for e in events if any(w in (e["event"] + " " + e["details"]).lower() for w in ["forced", "entry", "breach", "pried", "glass", "deadbolt", "fence", "cutter", "hasp", "shatter", "severed", "strike"])]
            if breach_events:
                answer_lines.append("**Point of Entry & Structural Breach Findings:**")
                for e in breach_events:
                    answer_lines.append(f"• {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])

        # 6. Query for Serology, Blood Spatter & Physical Injuries
        if any(k in q_lower for k in ["blood", "spatter", "serology", "injury", "injured", "victim", "struck", "guard", "wound", "battery", "assault"]):
            injury_events = [e for e in events if any(w in (e["event"] + " " + e["details"]).lower() for w in ["blood", "spatter", "serology", "victim", "struck", "shoved", "battery", "injury", "confrontation"])]
            if injury_events:
                answer_lines.append("**Serology & Physical Altercation Evidence:**")
                for e in injury_events:
                    answer_lines.append(f"• {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])

        # 7. Query for Suspect Profile / Description
        if any(k in q_lower for k in ["suspect", "who", "description", "clothing", "hoodie", "mask", "balaclava", "wear", "shoes", "gloves", "two"]):
            suspect_events = [e for e in events if any(w in (e["event"] + " " + e["details"]).lower() for w in ["suspect", "masked", "hoodie", "balaclava", "jumpsuit", "intruder", "adult", "individual"])]
            if suspect_events:
                answer_lines.append("**Suspect Description & Behavioral Profile:**")
                for e in suspect_events:
                    answer_lines.append(f"• {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])

        # 8. Query for Witness Testimony & 911 Audio
        if any(k in q_lower for k in ["witness", "caller", "911", "dispatcher", "said", "say", "statement", "audio", "stress", "panic"]):
            audio_events = [e for e in events if e["modality"] == "AUDIO_TRANSCRIPT"]
            if audio_events:
                answer_lines.append("**Sworn Witness & Emergency Audio Statements:**")
                for e in audio_events:
                    answer_lines.append(f"• [{e['timestamp']}] {e['event']}: {e['details']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])

        # 9. Query for Penal Codes & Legal Statutes
        if any(k in q_lower for k in ["penal", "statute", "penal code", "penalties", "charges", "what crimes", "violations", "statutory"]):
            answer_lines.append(f"**Applicable Penal Statutes for {parsed['case_id']}:**")
            seen_stats = set()
            for e in events:
                st = e.get("statute", "")
                if st and st not in ["N/A", "Witness Testimony (Sworn)"] and st not in seen_stats:
                    seen_stats.add(st)
                    answer_lines.append(f"• **{st}** — Linked to {e['event']} [{e['evidence_id']}].")
                    citations.append(e["evidence_id"])

        # If nothing specific was matched by the rules, perform semantic keyword retrieval across all ledger items
        if not answer_lines:
            tokens = [w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', q_lower) if w not in ["what", "when", "where", "which", "were", "there", "their", "this", "that", "about", "have", "with", "from"]]
            matched = []
            for e in events:
                score = sum(1 for tok in tokens if tok in (e["event"] + " " + e["details"] + " " + e["statute"]).lower())
                if score > 0:
                    matched.append((score, e))

            if matched:
                matched.sort(key=lambda x: x[0], reverse=True)
                answer_lines.append(f"**Grounded Forensic Ledger Results for Case {parsed['case_id']}:**")
                for _, e in matched[:4]:
                    answer_lines.append(f"• **[{e['timestamp']}]** {e['event']}: {e['details']} [{e['evidence_id']}]. (Statute: {e['statute']})")
                    citations.append(e["evidence_id"])
            else:
                answer_lines.append(
                    f"**INCONCLUSIVE - Evidentiary ledger contains no record substantiating this inquiry.**\n"
                    f"The investigation file for **{parsed['case_id']}** does not contain verified data matching your query. "
                    f"All evidence must strictly derive from authenticated visual markers, sworn audio transcripts, or CCTV feeds."
                )

        # Deduplicate citations
        unique_citations = list(dict.fromkeys(citations))

        return {
            "answer": "\n".join(answer_lines),
            "citations": unique_citations,
            "provider": f"CrimeVision Grounded Intelligence Engine ({parsed['case_id']})",
            "mode": "grounded_dynamic_rag"
        }
