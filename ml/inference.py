"""
Prototype malware inference engine.

For the minimal MVP this uses heuristics (entropy, suspicious extensions, EICAR).
Replace with trained RF + CNN models from EMBER in production.
"""
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path

SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar"}
EICAR_SIGNATURE = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


@dataclass
class ScanResult:
    classification: str  # "clean" or "malicious"
    confidence: float
    reasons: list[str]
    model_version: str = "heuristic-v1.0"


def _entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = {}
    for byte in data:
        freq[byte] = freq.get(byte, 0) + 1
    entropy = 0.0
    length = len(data)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy


def scan_bytes(content: bytes, filename: str = "") -> ScanResult:
    reasons = []
    malicious_score = 0.0

    ext = Path(filename).suffix.lower()
    if ext in SUSPICIOUS_EXTENSIONS:
        malicious_score += 0.4
        reasons.append(f"Suspicious file extension: {ext}")

    if EICAR_SIGNATURE in content:
        malicious_score = 1.0
        reasons = ["EICAR antivirus test file detected"]

    entropy = _entropy(content[:65536])
    if entropy > 7.5:
        malicious_score += 0.3
        reasons.append(f"High entropy section detected ({entropy:.2f})")

    if b"CreateRemoteThread" in content or b"VirtualAlloc" in content:
        malicious_score += 0.35
        reasons.append("Suspicious API strings found in file content")

    # Low confidence fail-safe
    confidence = min(max(malicious_score, 1 - malicious_score), 0.99)
    if malicious_score == 0:
        confidence = max(0.85, 1 - malicious_score)

    threshold = 0.7
    if malicious_score >= threshold:
        classification = "malicious"
        if not reasons:
            reasons.append("Heuristic analysis flagged suspicious patterns")
    elif malicious_score >= 0.4:
        classification = "malicious"
        confidence = max(confidence, 0.55)
        reasons.append("Low-confidence suspicious patterns — quarantined by fail-safe")
    else:
        classification = "clean"
        reasons = ["No threats were found"]

    return ScanResult(
        classification=classification,
        confidence=round(confidence, 4),
        reasons=reasons,
    )


def scan_file_path(path: str) -> ScanResult:
    with open(path, "rb") as f:
        content = f.read()
    return scan_bytes(content, filename=os.path.basename(path))
