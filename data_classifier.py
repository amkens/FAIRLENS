"""
FAIRLENS - Data Classifier

This module identifies and classifies types of data that a website,
application, or digital service may request from users.

The classifier provides a rule-based baseline. FAIRLENS can later
combine these results with AI-powered contextual analysis to determine
whether a particular data request is necessary, sensitive, or
potentially excessive.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from risk_framework import (
    DataClassification,
    NecessityLevel,
    is_sensitive_data,
)


# -------------------------------------------------------------------
# Data structure
# -------------------------------------------------------------------

@dataclass
class DataRequest:
    """
    Represents a single data request detected in user-provided text.
    """

    name: str
    classification: DataClassification
    matched_terms: List[str] = field(default_factory=list)

    sensitive: bool = False

    necessity: NecessityLevel = (
        NecessityLevel.UNCLEAR
    )

    confidence: float = 0.0

    context: str = ""


# -------------------------------------------------------------------
# Data classification rules
# -------------------------------------------------------------------

DATA_PATTERNS: Dict[DataClassification, List[str]] = {

    DataClassification.CONTACT: [
        r"\bemail\b",
        r"\be-mail\b",
        r"\bemail address\b",
        r"\bphone\b",
        r"\bphone number\b",
        r"\bmobile number\b",
        r"\btelephone\b",
        r"\bcontact number\b",
    ],

    DataClassification.BASIC_PERSONAL: [
        r"\bfull name\b",
        r"\bfirst name\b",
        r"\blast name\b",
        r"\bname\b",
        r"\bdate of birth\b",
        r"\bdob\b",
        r"\bage\b",
        r"\bgender\b",
    ],

    DataClassification.IDENTIFICATION: [
        r"\bpassport\b",
        r"\bpassport number\b",
        r"\bgovernment id\b",
        r"\bgovernment identification\b",
        r"\bnational id\b",
        r"\bnational identification\b",
        r"\bdriver'?s license\b",
        r"\blicense number\b",
        r"\bsocial security number\b",
        r"\bssn\b",
        r"\btax id\b",
        r"\btax identification\b",
    ],

    DataClassification.FINANCIAL: [
        r"\bincome\b",
        r"\bannual income\b",
        r"\bsalary\b",
        r"\bbank account\b",
        r"\bbank account number\b",
        r"\baccount number\b",
        r"\bcredit card\b",
        r"\bdebit card\b",
        r"\bcard number\b",
        r"\bfinancial information\b",
        r"\bfinancial data\b",
        r"\bpayment information\b",
    ],

    DataClassification.HEALTH: [
        r"\bhealth information\b",
        r"\bhealth data\b",
        r"\bmedical information\b",
        r"\bmedical history\b",
        r"\bmedical condition\b",
        r"\bhealth condition\b",
        r"\bdiagnosis\b",
        r"\bdisability\b",
        r"\bmedication\b",
        r"\bprescription\b",
    ],

    DataClassification.BIOMETRIC: [
        r"\bfingerprint\b",
        r"\bfacial recognition\b",
        r"\bface scan\b",
        r"\bface recognition\b",
        r"\biris scan\b",
        r"\bvoiceprint\b",
        r"\bbiometric\b",
        r"\bbiometric data\b",
    ],

    DataClassification.LOCATION: [
        r"\blocation\b",
        r"\bprecise location\b",
        r"\bgps\b",
        r"\bgps location\b",
        r"\blive location\b",
        r"\bgeolocation\b",
        r"\blocation data\b",
    ],

    DataClassification.DEMOGRAPHIC: [
        r"\brace\b",
        r"\bethnicity\b",
        r"\bcountry of origin\b",
        r"\bnationality\b",
        r"\bsexual orientation\b",
        r"\bmarital status\b",
        r"\bfamily status\b",
    ],

    DataClassification.EMPLOYMENT: [
        r"\bemployment\b",
        r"\bemployment status\b",
        r"\bemployer\b",
        r"\bjob title\b",
        r"\boccupation\b",
        r"\bwork history\b",
        r"\bemployment history\b",
    ],

    DataClassification.EDUCATION: [
        r"\beducation\b",
        r"\beducational background\b",
        r"\bschool\b",
        r"\buniversity\b",
        r"\bcollege\b",
        r"\bdegree\b",
        r"\bacademic history\b",
    ],

    DataClassification.ONLINE_ACTIVITY: [
        r"\bbrowsing history\b",
        r"\bsearch history\b",
        r"\bsearch activity\b",
        r"\bwebsite activity\b",
        r"\bonline activity\b",
        r"\bclick history\b",
        r"\bviewing history\b",
    ],

    DataClassification.DEVICE_DATA: [
        r"\bdevice id\b",
        r"\bdevice identifier\b",
        r"\bip address\b",
        r"\bip address data\b",
        r"\bbrowser information\b",
        r"\bdevice information\b",
        r"\boperating system\b",
        r"\bcookies\b",
        r"\bcookie data\b",
    ],

    DataClassification.SOCIAL: [
        r"\bcontacts\b",
        r"\bcontact list\b",
        r"\bfriends list\b",
        r"\bsocial connections\b",
        r"\bsocial media\b",
        r"\bsocial media account\b",
    ],

    DataClassification.POLITICAL: [
        r"\bpolitical affiliation\b",
        r"\bpolitical opinion\b",
        r"\bpolitical views\b",
        r"\bpolitical party\b",
    ],

    DataClassification.RELIGIOUS: [
        r"\breligion\b",
        r"\breligious belief\b",
        r"\breligious affiliation\b",
        r"\bfaith\b",
    ],

    DataClassification.SEXUAL_ORIENTATION: [
        r"\bsexual orientation\b",
        r"\bsexual identity\b",
    ],
}


# -------------------------------------------------------------------
# Default necessity assumptions
# -------------------------------------------------------------------

DEFAULT_NECESSITY: Dict[
    DataClassification,
    NecessityLevel
] = {

    DataClassification.CONTACT:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.BASIC_PERSONAL:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.IDENTIFICATION:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.FINANCIAL:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.HEALTH:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.BIOMETRIC:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.LOCATION:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.DEMOGRAPHIC:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.EMPLOYMENT:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.EDUCATION:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.ONLINE_ACTIVITY:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.DEVICE_DATA:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.SOCIAL:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.POLITICAL:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.RELIGIOUS:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.SEXUAL_ORIENTATION:
        NecessityLevel.CONTEXT_DEPENDENT,

    DataClassification.UNKNOWN:
        NecessityLevel.UNCLEAR,
}


# -------------------------------------------------------------------
# Text normalization
# -------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize user-provided text before classification.

    Converts text to lowercase and removes unnecessary whitespace.
    """

    if not text:
        return ""

    normalized = text.lower()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()


# -------------------------------------------------------------------
# Extract context
# -------------------------------------------------------------------

def extract_context(
    text: str,
    start: int,
    end: int,
    window: int = 80,
) -> str:
    """
    Extract a small section of text surrounding a matched term.

    This helps the AI understand how a piece of data is being requested.
    """

    context_start = max(
        0,
        start - window,
    )

    context_end = min(
        len(text),
        end + window,
    )

    return text[
        context_start:context_end
    ].strip()


# -------------------------------------------------------------------
# Classify data requests
# -------------------------------------------------------------------

def classify_data_requests(
    text: str,
) -> List[DataRequest]:
    """
    Detect and classify data requests from user-provided text.

    Args:
        text:
            Text copied from a website form, signup page,
            privacy notice, or data collection statement.

    Returns:
        A list of DataRequest objects.
    """

    if not text or not text.strip():
        return []

    normalized_text = normalize_text(text)

    detected: Dict[
        Tuple[DataClassification, str],
        DataRequest
    ] = {}

    for classification, patterns in DATA_PATTERNS.items():

        for pattern in patterns:

            matches = re.finditer(
                pattern,
                normalized_text,
                flags=re.IGNORECASE,
            )

            for match in matches:

                matched_term = match.group(
                    0
                ).strip()

                key = (
                    classification,
                    matched_term,
                )

                if key not in detected:

                    request = DataRequest(
                        name=matched_term,
                        classification=classification,
                        matched_terms=[
                            matched_term
                        ],
                        sensitive=is_sensitive_data(
                            classification
                        ),
                        necessity=DEFAULT_NECESSITY.get(
                            classification,
                            NecessityLevel.UNCLEAR,
                        ),
                        confidence=0.85,
                        context=extract_context(
                            normalized_text,
                            match.start(),
                            match.end(),
                        ),
                    )

                    detected[key] = request

                else:

                    if (
                        matched_term
                        not in detected[key].matched_terms
                    ):

                        detected[key].matched_terms.append(
                            matched_term
                        )

    return list(
        detected.values()
    )


# -------------------------------------------------------------------
# Group results by classification
# -------------------------------------------------------------------

def group_by_classification(
    requests: List[DataRequest],
) -> Dict[
    DataClassification,
    List[DataRequest]
]:
    """
    Group detected data requests by their classification.
    """

    grouped: Dict[
        DataClassification,
        List[DataRequest]
    ] = {}

    for request in requests:

        if request.classification not in grouped:

            grouped[
                request.classification
            ] = []

        grouped[
            request.classification
        ].append(request)

    return grouped


# -------------------------------------------------------------------
# Get sensitive data requests
# -------------------------------------------------------------------

def get_sensitive_requests(
    requests: List[DataRequest],
) -> List[DataRequest]:
    """
    Return only requests classified as sensitive.
    """

    return [
        request
        for request in requests
        if request.sensitive
    ]


# -------------------------------------------------------------------
# Generate classification summary
# -------------------------------------------------------------------

def generate_summary(
    requests: List[DataRequest],
) -> Dict[str, int]:
    """
    Generate high-level statistics about detected data requests.
    """

    return {
        "total_requests": len(
            requests
        ),

        "sensitive_requests": len(
            get_sensitive_requests(
                requests
            )
        ),

        "unique_categories": len(
            set(
                request.classification
                for request in requests
            )
        ),
    }