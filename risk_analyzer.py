"""
FAIRLENS - Risk Analyzer

This module connects the FAIRLENS data classifier,
AI analysis prompts, Groq API, and risk framework.

Main responsibilities:

1. Validate user input.
2. Detect data requests from the provided text.
3. Build the AI analysis prompt.
4. Send the request to the Groq AI model.
5. Parse the AI's JSON response.
6. Validate and normalize the response.
7. Add deterministic information from the local classifier.
8. Return a structured FAIRLENS risk report.

FAIRLENS provides privacy risk analysis and is not a legal
compliance or legal advice system.
"""

import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq

from data_classifier import (
    DataRequest,
    classify_data_requests,
    generate_summary,
)

from prompts import (
    SYSTEM_PROMPT,
    build_analysis_prompt,
)

from risk_framework import (
    DataClassification,
    NecessityLevel,
    RiskCategory,
    RiskLevel,
)


# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------

load_dotenv()


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# Groq model used for FAIRLENS analysis.
#
# If you later want to change the model, you can pass a different
# model name to analyze_with_ai() or run_risk_analysis().
#
# This model is intended for fast, structured analysis.
DEFAULT_MODEL = "llama-3.3-70b-versatile"


# Maximum amount of text accepted from the user.
MAX_USER_TEXT_LENGTH = 50000


# -------------------------------------------------------------------
# Valid values from FAIRLENS framework
# -------------------------------------------------------------------

VALID_RISK_LEVELS = {
    level.value
    for level in RiskLevel
}


VALID_NECESSITY_LEVELS = {
    level.value
    for level in NecessityLevel
}


VALID_CLASSIFICATIONS = {
    classification.value
    for classification in DataClassification
}


# -------------------------------------------------------------------
# Input validation
# -------------------------------------------------------------------

def validate_inputs(
    service_description: str,
    user_text: str,
) -> None:
    """
    Validate user input before starting the AI analysis.

    Raises:
        ValueError:
            If required input is missing or invalid.
    """

    # Check service description.
    if not service_description:
        raise ValueError(
            "Please describe what the website or service does."
        )

    # Check user-provided text.
    if not user_text:
        raise ValueError(
            "Please paste the website text, signup form, "
            "privacy notice, or data collection statement."
        )

    # Remove surrounding whitespace.
    service_description = service_description.strip()
    user_text = user_text.strip()

    # Check minimum service description length.
    if len(service_description) < 5:
        raise ValueError(
            "The service description is too short. "
            "Please provide more context."
        )

    # Check minimum text length.
    if len(user_text) < 10:
        raise ValueError(
            "The text provided is too short to analyze."
        )

    # Prevent unnecessarily large inputs.
    if len(user_text) > MAX_USER_TEXT_LENGTH:
        raise ValueError(
            "The provided text is too long. "
            "Please analyze a smaller section of the privacy policy "
            "or data collection notice."
        )


# -------------------------------------------------------------------
# Groq client
# -------------------------------------------------------------------

def get_groq_client() -> Groq:
    """
    Create a Groq client using the GROQ_API_KEY environment variable.

    Returns:
        Configured Groq client.

    Raises:
        ValueError:
            If the Groq API key is not available.
    """

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Please add your Groq API key to the .env file."
        )

    return Groq(
        api_key=api_key
    )


# -------------------------------------------------------------------
# AI response parsing
# -------------------------------------------------------------------

def parse_json_response(
    response_text: str,
) -> Dict[str, Any]:
    """
    Parse the AI response as JSON.

    The AI is instructed to return JSON only.
    This function also handles accidental Markdown code fences.
    """

    if not response_text:
        raise ValueError(
            "The AI returned an empty response."
        )

    cleaned = response_text.strip()

    # Remove Markdown JSON code fences.
    if cleaned.startswith(
        "```json"
    ):
        cleaned = cleaned[
            7:
        ]

    elif cleaned.startswith(
        "```"
    ):
        cleaned = cleaned[
            3:
        ]

    if cleaned.endswith(
        "```"
    ):
        cleaned = cleaned[
            :-3
        ]

    cleaned = cleaned.strip()

    # Attempt JSON parsing.
    try:

        result = json.loads(
            cleaned
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "The AI returned an invalid JSON response."
        ) from error

    # The top-level response must be a dictionary.
    if not isinstance(
        result,
        dict,
    ):
        raise ValueError(
            "The AI response must be a JSON object."
        )

    return result


# -------------------------------------------------------------------
# Normalize risk level
# -------------------------------------------------------------------

def normalize_risk_level(
    value: Any,
) -> str:
    """
    Normalize a risk level returned by the AI.

    Invalid or missing values default to Medium rather than
    silently treating an uncertain result as Low risk.
    """

    if not isinstance(
        value,
        str,
    ):
        return RiskLevel.MEDIUM.value

    normalized = value.strip().title()

    if normalized in VALID_RISK_LEVELS:
        return normalized

    return RiskLevel.MEDIUM.value


# -------------------------------------------------------------------
# Normalize necessity
# -------------------------------------------------------------------

def normalize_necessity(
    value: Any,
) -> str:
    """
    Normalize a necessity classification returned by the AI.
    """

    if not isinstance(
        value,
        str,
    ):
        return NecessityLevel.UNCLEAR.value

    normalized = value.strip()

    if normalized in VALID_NECESSITY_LEVELS:
        return normalized

    return NecessityLevel.UNCLEAR.value


# -------------------------------------------------------------------
# Normalize data classification
# -------------------------------------------------------------------

def normalize_classification(
    value: Any,
) -> str:
    """
    Normalize a data classification returned by the AI.

    Unknown classifications are mapped to Unknown.
    """

    if not isinstance(
        value,
        str,
    ):
        return DataClassification.UNKNOWN.value

    normalized = value.strip()

    if normalized in VALID_CLASSIFICATIONS:
        return normalized

    return DataClassification.UNKNOWN.value


# -------------------------------------------------------------------
# Normalize score
# -------------------------------------------------------------------

def normalize_score(
    value: Any,
) -> int:
    """
    Normalize a risk score to a value between 0 and 4.
    """

    try:

        score = int(
            value
        )

    except (
        TypeError,
        ValueError,
    ):

        return 0

    return max(
        0,
        min(
            score,
            4,
        ),
    )


# -------------------------------------------------------------------
# Normalize risk categories
# -------------------------------------------------------------------

def normalize_risk_categories(
    categories: Any,
) -> Dict[str, Dict[str, Any]]:
    """
    Validate and normalize the six FAIRLENS risk categories.
    """

    if not isinstance(
        categories,
        dict,
    ):
        categories = {}

    category_mapping = {
        "data_necessity":
            RiskCategory.DATA_NECESSITY.value,

        "data_sensitivity":
            RiskCategory.DATA_SENSITIVITY.value,

        "data_minimization":
            RiskCategory.DATA_MINIMIZATION.value,

        "transparency":
            RiskCategory.TRANSPARENCY.value,

        "consent":
            RiskCategory.CONSENT.value,

        "data_sharing":
            RiskCategory.DATA_SHARING.value,
    }

    normalized = {}

    for key in category_mapping:

        category_data = categories.get(
            key,
            {},
        )

        if not isinstance(
            category_data,
            dict,
        ):
            category_data = {}

        normalized[key] = {
            "level":
                normalize_risk_level(
                    category_data.get(
                        "level"
                    )
                ),

            "score":
                normalize_score(
                    category_data.get(
                        "score"
                    )
                ),

            "reason":
                str(
                    category_data.get(
                        "reason",
                        "No explanation provided.",
                    )
                ),
        }

    return normalized


# -------------------------------------------------------------------
# Normalize data requests
# -------------------------------------------------------------------

def normalize_data_requests(
    data_requests: Any,
) -> List[Dict[str, Any]]:
    """
    Validate and normalize individual data request findings.
    """

    if not isinstance(
        data_requests,
        list,
    ):
        return []

    normalized = []

    for item in data_requests:

        if not isinstance(
            item,
            dict,
        ):
            continue

        normalized.append(
            {
                "data_name":
                    str(
                        item.get(
                            "data_name",
                            "Unknown data",
                        )
                    ),

                "classification":
                    normalize_classification(
                        item.get(
                            "classification"
                        )
                    ),

                "sensitive":
                    bool(
                        item.get(
                            "sensitive",
                            False,
                        )
                    ),

                "necessity":
                    normalize_necessity(
                        item.get(
                            "necessity"
                        )
                    ),

                "risk_level":
                    normalize_risk_level(
                        item.get(
                            "risk_level"
                        )
                    ),

                "reasoning":
                    str(
                        item.get(
                            "reasoning",
                            "No reasoning provided.",
                        )
                    ),

                "minimization_concern":
                    bool(
                        item.get(
                            "minimization_concern",
                            False,
                        )
                    ),

                "recommended_action":
                    str(
                        item.get(
                            "recommended_action",
                            "Review why this information is being requested.",
                        )
                    ),
            }
        )

    return normalized


# -------------------------------------------------------------------
# Normalize complete AI result
# -------------------------------------------------------------------

def normalize_analysis_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize the complete AI response into the FAIRLENS format.
    """

    # Extract overall risk.
    overall = result.get(
        "overall_risk",
        {},
    )

    if not isinstance(
        overall,
        dict,
    ):
        overall = {}

    # Extract key findings.
    key_findings = result.get(
        "key_findings",
        [],
    )

    if not isinstance(
        key_findings,
        list,
    ):
        key_findings = []

    # Extract recommended actions.
    recommended_actions = result.get(
        "recommended_actions",
        [],
    )

    if not isinstance(
        recommended_actions,
        list,
    ):
        recommended_actions = []

    return {
        "overall_risk": {
            "level":
                normalize_risk_level(
                    overall.get(
                        "level"
                    )
                ),

            "score":
                normalize_score(
                    overall.get(
                        "score"
                    )
                ),

            "summary":
                str(
                    overall.get(
                        "summary",
                        "No overall risk summary was provided.",
                    )
                ),
        },

        "data_requests":
            normalize_data_requests(
                result.get(
                    "data_requests",
                    [],
                )
        ),

        "risk_categories":
            normalize_risk_categories(
                result.get(
                    "risk_categories",
                    {},
                )
        ),

        "key_findings": [
            str(
                finding
            )
            for finding in key_findings
        ],

        "recommended_actions": [
            str(
                action
            )
            for action in recommended_actions
        ],
    }


# -------------------------------------------------------------------
# Merge local classifier results
# -------------------------------------------------------------------

def merge_classifier_results(
    analysis: Dict[str, Any],
    detected_requests: List[DataRequest],
) -> Dict[str, Any]:
    """
    Combine deterministic classifier information with AI findings.

    The local classifier provides additional information about
    detected data categories and sensitivity.

    AI-generated contextual reasoning remains the primary source
    for necessity and overall risk interpretation.
    """

    ai_requests = analysis.get(
        "data_requests",
        [],
    )

    # Create a lookup dictionary using the detected data name.
    classifier_lookup = {
        request.name.lower():
            request
        for request in detected_requests
    }

    for item in ai_requests:

        data_name = str(
            item.get(
                "data_name",
                "",
            )
        ).lower()

        local_match = classifier_lookup.get(
            data_name
        )

        if local_match:

            # Use deterministic local classification
            # when an exact match is available.
            item[
                "classification"
            ] = local_match.classification.value

            item[
                "sensitive"
            ] = local_match.sensitive

    return analysis


# -------------------------------------------------------------------
# Analyze with Groq AI
# -------------------------------------------------------------------

def analyze_with_ai(
    service_description: str,
    user_text: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send the user's information to the Groq AI model and return
    a normalized FAIRLENS analysis.

    Args:
        service_description:
            Description of the website or digital service.

        user_text:
            Pasted signup form, privacy notice, or data collection text.

        model:
            Optional Groq model name.

    Returns:
        Structured FAIRLENS analysis.
    """

    # ---------------------------------------------------------------
    # Step 1: Validate user input
    # ---------------------------------------------------------------

    validate_inputs(
        service_description,
        user_text,
    )

    # ---------------------------------------------------------------
    # Step 2: Run deterministic local data classification
    # ---------------------------------------------------------------

    detected_requests = classify_data_requests(
        user_text
    )

    # ---------------------------------------------------------------
    # Step 3: Create Groq client
    # ---------------------------------------------------------------

    client = get_groq_client()

    # ---------------------------------------------------------------
    # Step 4: Build AI analysis prompt
    # ---------------------------------------------------------------

    prompt = build_analysis_prompt(
        service_description,
        user_text,
    )

    # ---------------------------------------------------------------
    # Step 5: Send request to Groq
    # ---------------------------------------------------------------

    response = client.chat.completions.create(
        model=model or DEFAULT_MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        temperature=0.1,

        response_format={
            "type": "json_object"
        },
    )

    # ---------------------------------------------------------------
    # Step 6: Extract AI response
    # ---------------------------------------------------------------

    response_text = (
        response
        .choices[0]
        .message
        .content
    )

    if not response_text:
        raise ValueError(
            "Groq returned an empty response."
        )

    # ---------------------------------------------------------------
    # Step 7: Parse AI JSON
    # ---------------------------------------------------------------

    parsed_result = parse_json_response(
        response_text
    )

    # ---------------------------------------------------------------
    # Step 8: Normalize AI response
    # ---------------------------------------------------------------

    normalized_result = normalize_analysis_result(
        parsed_result
    )

    # ---------------------------------------------------------------
    # Step 9: Merge deterministic classifier results
    # ---------------------------------------------------------------

    final_result = merge_classifier_results(
        normalized_result,
        detected_requests,
    )

    # ---------------------------------------------------------------
    # Step 10: Add local classifier summary
    # ---------------------------------------------------------------

    final_result[
        "detected_data_summary"
    ] = generate_summary(
        detected_requests
    )

    return final_result


# -------------------------------------------------------------------
# Safe wrapper for application use
# -------------------------------------------------------------------

def run_risk_analysis(
    service_description: str,
    user_text: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Safely run FAIRLENS analysis.

    This wrapper is intended to be called by app.py.

    Instead of crashing the Gradio interface, errors are returned
    in a structured format that the UI can display.
    """

    try:

        result = analyze_with_ai(
            service_description,
            user_text,
            model,
        )

        return {
            "success": True,
            "error": None,
            "result": result,
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(
                error
            ),
            "result": None,
        }
