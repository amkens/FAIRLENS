"""
FAIRLENS - AI Analysis Prompts

This module contains the prompts used to guide the AI analysis
performed by FAIRLENS.

The AI is responsible for contextual reasoning. It should not
simply label data as "sensitive" and assume that it is risky.

Instead, it must consider:

- What the service does
- Why the data may be needed
- Whether the data appears necessary
- Whether the data is sensitive
- Whether the service collects more data than needed
- How clearly the data collection is explained
- Whether user consent is meaningful
- Whether data may be shared with third parties
"""


# -------------------------------------------------------------------
# System Prompt
# -------------------------------------------------------------------

SYSTEM_PROMPT = """
You are FAIRLENS, an AI-assisted privacy and data collection
risk analysis system.

Your purpose is to help users understand what personal information
a website, application, or digital service is asking them to provide.

You analyze:

1. Data necessity
2. Data sensitivity
3. Data minimization
4. Transparency
5. Consent and user choice
6. Third-party data sharing

IMPORTANT PRINCIPLES:

- Do not automatically assume that sensitive data is unnecessary.
- A data type may be sensitive but still reasonably necessary depending
  on the service and its purpose.
- Always consider the context of the service before judging necessity.
- If the purpose is unclear, classify necessity as "Unclear" rather
  than making an unsupported assumption.
- Distinguish between "sensitive" and "potentially excessive".
- Do not claim that a website is violating a law unless the evidence
  clearly supports such a conclusion.
- FAIRLENS provides a risk-oriented analysis, not legal advice.
- Be cautious about making definitive claims.
- Explain the reasoning behind every significant risk finding.
- Focus on helping users understand what they should investigate
  or question.

You must return your analysis as valid JSON following the exact
structure requested by the user prompt.
"""


# -------------------------------------------------------------------
# Main Analysis Prompt
# -------------------------------------------------------------------

ANALYSIS_PROMPT = """
Analyze the following website or digital service for potential
privacy and data collection risks.

SERVICE DESCRIPTION:
{service_description}

USER-PROVIDED TEXT:
{user_text}

The user-provided text may contain:

- Signup forms
- Registration questions
- Data collection notices
- Privacy policy excerpts
- Consent statements
- Cookie notices
- Permission requests
- Third-party data sharing statements

Your task is to analyze the provided information and identify
potential privacy risks.

For every detected data request:

1. Identify the data being requested.
2. Classify the type of data.
3. Determine whether the data is sensitive.
4. Assess whether the data appears necessary for the stated
   purpose of the service.
5. Explain why the data may or may not be necessary.
6. Identify whether the request may violate the principle of
   data minimization.
7. Identify any concerns about transparency.
8. Identify any concerns about consent or user choice.
9. Identify whether the text suggests data sharing with
   third parties.

IMPORTANT:

A sensitive data request is NOT automatically a high-risk request.

For example:

- A bank requesting financial information may be reasonable.
- A healthcare service requesting health information may be reasonable.
- A weather application requesting precise location may be
  context-dependent.
- A simple calculator application requesting precise location
  may be potentially excessive.

Always consider the stated purpose of the service.

If the purpose of a data request cannot be determined,
use "Unclear" rather than assuming the data is unnecessary.

Also analyze the overall privacy posture of the service.

Identify:

- The overall privacy risk level.
- The main privacy concerns.
- The most important data requests that users should review.
- Recommended actions for the user.

Do not provide legal conclusions.

Return ONLY valid JSON using the following structure:

{{
    "overall_risk": {{
        "level": "Low | Medium | High | Critical",
        "score": 0,
        "summary": "Short explanation of the overall risk."
    }},

    "data_requests": [
        {{
            "data_name": "Name of requested data",
            "classification": "Data classification",
            "sensitive": true,
            "necessity": "Likely Necessary | Context-Dependent | Potentially Excessive | Unclear",
            "risk_level": "Low | Medium | High | Critical",
            "reasoning": "Explain why this data request received this assessment.",
            "minimization_concern": true,
            "recommended_action": "What the user should consider or investigate."
        }}
    ],

    "risk_categories": {{
        "data_necessity": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }},

        "data_sensitivity": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }},

        "data_minimization": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }},

        "transparency": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }},

        "consent": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }},

        "data_sharing": {{
            "level": "Low | Medium | High | Critical",
            "score": 0,
            "reason": "Explanation"
        }}
    }},

    "key_findings": [
        "Important finding 1",
        "Important finding 2"
    ],

    "recommended_actions": [
        "Recommended action 1",
        "Recommended action 2"
    ]
}}
"""


# -------------------------------------------------------------------
# Focused Prompt: Data Necessity
# -------------------------------------------------------------------

NECESSITY_ANALYSIS_PROMPT = """
Evaluate whether the following data request appears necessary
for the stated service.

SERVICE:
{service_description}

DATA REQUEST:
{data_request}

Consider:

- Is this information directly required to provide the core service?
- Could the service reasonably function without this information?
- Could the information be optional rather than mandatory?
- Is the request justified by the stated purpose?
- Is the request common and reasonable for this type of service?

Classify the necessity as exactly one of:

- Likely Necessary
- Context-Dependent
- Potentially Excessive
- Unclear

Provide a short explanation.

Do not make legal claims.
Do not assume that sensitive data is automatically unnecessary.
"""


# -------------------------------------------------------------------
# Focused Prompt: Consent Analysis
# -------------------------------------------------------------------

CONSENT_ANALYSIS_PROMPT = """
Analyze the following text for consent and user-choice concerns.

TEXT:
{user_text}

Look for:

- Clear consent requests
- Separate consent options
- Optional versus mandatory choices
- Broad or vague consent
- Bundled consent
- Pre-selected options
- Forced consent
- Ability to refuse optional data collection
- Ability to withdraw consent

Classify the consent quality as one of:

- Clear
- Partial
- Broad
- Potentially Forced
- Unclear

Explain the reasoning.

Do not make legal conclusions.
"""


# -------------------------------------------------------------------
# Focused Prompt: Transparency Analysis
# -------------------------------------------------------------------

TRANSPARENCY_ANALYSIS_PROMPT = """
Analyze the following text for transparency concerns.

TEXT:
{user_text}

Evaluate whether the user is clearly informed about:

- What data is being collected
- Why the data is being collected
- How the data will be used
- How long the data may be retained
- Whether data may be shared
- Who may receive the data
- Whether automated decision-making is involved

Identify vague or unclear statements.

Classify transparency risk as:

- Low
- Medium
- High
- Critical

Explain the reasoning without making legal conclusions.
"""


# -------------------------------------------------------------------
# Focused Prompt: Data Sharing Analysis
# -------------------------------------------------------------------

DATA_SHARING_ANALYSIS_PROMPT = """
Analyze the following text for possible third-party data sharing.

TEXT:
{user_text}

Look for references to:

- Third-party companies
- Business partners
- Service providers
- Advertisers
- Analytics providers
- Data brokers
- Affiliates
- Marketing partners
- "Trusted partners"
- "Selected partners"
- Selling or sharing personal information

Determine whether the text clearly explains:

1. Who receives the data.
2. Why the data is shared.
3. What types of data are shared.
4. Whether users can opt out.

Classify the data-sharing risk as:

- Low
- Medium
- High
- Critical

Explain the reasoning.

Do not make legal conclusions.
"""


# -------------------------------------------------------------------
# Prompt Formatting Helpers
# -------------------------------------------------------------------

def build_analysis_prompt(
    service_description: str,
    user_text: str,
) -> str:
    """
    Insert user-provided information into the main analysis prompt.
    """

    return ANALYSIS_PROMPT.format(
        service_description=service_description.strip(),
        user_text=user_text.strip(),
    )


def build_necessity_prompt(
    service_description: str,
    data_request: str,
) -> str:
    """
    Build a focused prompt for evaluating data necessity.
    """

    return NECESSITY_ANALYSIS_PROMPT.format(
        service_description=service_description.strip(),
        data_request=data_request.strip(),
    )


def build_consent_prompt(
    user_text: str,
) -> str:
    """
    Build a focused prompt for analyzing consent.
    """

    return CONSENT_ANALYSIS_PROMPT.format(
        user_text=user_text.strip(),
    )


def build_transparency_prompt(
    user_text: str,
) -> str:
    """
    Build a focused prompt for analyzing transparency.
    """

    return TRANSPARENCY_ANALYSIS_PROMPT.format(
        user_text=user_text.strip(),
    )


def build_data_sharing_prompt(
    user_text: str,
) -> str:
    """
    Build a focused prompt for analyzing third-party data sharing.
    """

    return DATA_SHARING_ANALYSIS_PROMPT.format(
        user_text=user_text.strip(),
    )
