"""
FAIRLENS - Privacy Risk Framework

This module defines the core privacy and data-collection
risk categories used by FAIRLENS.

FAIRLENS analyzes website forms, signup flows, and privacy
notices to identify potentially sensitive, excessive, or
unclear data collection practices.
"""

from enum import Enum
from typing import Dict, List


class RiskLevel(str, Enum):
    """
    Standard risk levels used throughout FAIRLENS.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class RiskCategory(str, Enum):
    """
    Core privacy risk dimensions evaluated by FAIRLENS.
    """

    DATA_NECESSITY = "Data Necessity"
    DATA_SENSITIVITY = "Data Sensitivity"
    DATA_MINIMIZATION = "Data Minimization"
    TRANSPARENCY = "Transparency"
    CONSENT = "Consent & User Choice"
    DATA_SHARING = "Third-Party Data Sharing"


class DataClassification(str, Enum):
    """
    Classification of information that a website or service
    may request from users.
    """

    BASIC_PERSONAL = "Basic Personal Data"
    CONTACT = "Contact Information"
    IDENTIFICATION = "Identification Data"
    FINANCIAL = "Financial Data"
    HEALTH = "Health Data"
    BIOMETRIC = "Biometric Data"
    LOCATION = "Location Data"
    DEMOGRAPHIC = "Demographic Data"
    EMPLOYMENT = "Employment Data"
    EDUCATION = "Education Data"
    ONLINE_ACTIVITY = "Online Activity"
    DEVICE_DATA = "Device Data"
    SOCIAL = "Social / Relationship Data"
    POLITICAL = "Political Data"
    RELIGIOUS = "Religious Data"
    SEXUAL_ORIENTATION = "Sexual Orientation Data"
    UNKNOWN = "Unknown"


class NecessityLevel(str, Enum):
    """
    Indicates how necessary a requested piece of data appears
    to be for the stated purpose of a service.
    """

    LIKELY_NECESSARY = "Likely Necessary"
    CONTEXT_DEPENDENT = "Context-Dependent"
    POTENTIALLY_EXCESSIVE = "Potentially Excessive"
    UNCLEAR = "Unclear"


class ConsentLevel(str, Enum):
    """
    Describes the quality of user choice and consent.
    """

    CLEAR = "Clear"
    PARTIAL = "Partial"
    BROAD = "Broad"
    FORCED = "Potentially Forced"
    UNCLEAR = "Unclear"


# -------------------------------------------------------------------
# Risk category descriptions
# -------------------------------------------------------------------

RISK_CATEGORY_DESCRIPTIONS: Dict[RiskCategory, str] = {
    RiskCategory.DATA_NECESSITY: (
        "Evaluates whether the requested information appears reasonably "
        "necessary for the stated purpose of the service."
    ),

    RiskCategory.DATA_SENSITIVITY: (
        "Evaluates whether the service requests sensitive, personal, "
        "financial, health, biometric, location, or other high-impact data."
    ),

    RiskCategory.DATA_MINIMIZATION: (
        "Evaluates whether the service appears to collect more information "
        "than is reasonably required to provide its core functionality."
    ),

    RiskCategory.TRANSPARENCY: (
        "Evaluates whether the purpose and use of collected data are clearly "
        "explained to the user."
    ),

    RiskCategory.CONSENT: (
        "Evaluates whether users are given clear, meaningful, and voluntary "
        "choices regarding how their data is collected and used."
    ),

    RiskCategory.DATA_SHARING: (
        "Evaluates whether user data may be shared with third parties, "
        "partners, advertisers, or other external organizations."
    ),
}


# -------------------------------------------------------------------
# Sensitive data categories
# -------------------------------------------------------------------

SENSITIVE_DATA_CATEGORIES: List[DataClassification] = [
    DataClassification.FINANCIAL,
    DataClassification.HEALTH,
    DataClassification.BIOMETRIC,
    DataClassification.LOCATION,
    DataClassification.POLITICAL,
    DataClassification.RELIGIOUS,
    DataClassification.SEXUAL_ORIENTATION,
]


# -------------------------------------------------------------------
# Risk scoring
# -------------------------------------------------------------------

RISK_SCORES: Dict[RiskLevel, int] = {
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 2,
    RiskLevel.HIGH: 3,
    RiskLevel.CRITICAL: 4,
}


def get_risk_score(risk_level: RiskLevel) -> int:
    """
    Convert a risk level into a numerical score.

    Args:
        risk_level: A FAIRLENS RiskLevel.

    Returns:
        Integer score from 1 to 4.
    """

    return RISK_SCORES[risk_level]


def calculate_overall_risk(risk_levels: List[RiskLevel]) -> RiskLevel:
    """
    Calculate an overall risk level from multiple risk assessments.

    The highest individual risk level is used as the overall risk.
    This conservative approach ensures that a critical privacy issue
    is not hidden by several low-risk findings.

    Args:
        risk_levels: List of individual RiskLevel values.

    Returns:
        The highest applicable RiskLevel.
    """

    if not risk_levels:
        return RiskLevel.LOW

    highest_score = max(
        get_risk_score(level)
        for level in risk_levels
    )

    for level, score in RISK_SCORES.items():
        if score == highest_score:
            return level

    return RiskLevel.LOW


# -------------------------------------------------------------------
# Data classification helpers
# -------------------------------------------------------------------

def is_sensitive_data(
    classification: DataClassification,
) -> bool:
    """
    Determine whether a data classification is considered sensitive.

    Args:
        classification: A DataClassification value.

    Returns:
        True if the category is considered sensitive.
    """

    return classification in SENSITIVE_DATA_CATEGORIES


def get_necessity_description(
    necessity_level: NecessityLevel,
) -> str:
    """
    Provide a human-readable explanation of a necessity classification.
    """

    descriptions = {
        NecessityLevel.LIKELY_NECESSARY: (
            "The information appears reasonably necessary for the "
            "service's stated purpose."
        ),

        NecessityLevel.CONTEXT_DEPENDENT: (
            "The necessity of this information depends on the specific "
            "purpose and context in which the service operates."
        ),

        NecessityLevel.POTENTIALLY_EXCESSIVE: (
            "The information may not be necessary for the core purpose "
            "of the service and should be reviewed."
        ),

        NecessityLevel.UNCLEAR: (
            "It is unclear why this information is required based on "
            "the available information."
        ),
    }

    return descriptions[necessity_level]