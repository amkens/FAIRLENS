"""
FAIRLENS - Analyzer Test

This script tests the complete FAIRLENS backend pipeline:

1. User input
2. Data classification
3. AI prompt generation
4. OpenAI API call
5. JSON parsing
6. Risk analysis
7. Final structured result

Run this file from the FAIRLENS project folder with:

    python3 test_analyzer.py
"""

import json

from risk_analyzer import run_risk_analysis


# -------------------------------------------------------------------
# Test Input
# -------------------------------------------------------------------

SERVICE_DESCRIPTION = """
An online clothing and fashion shopping website where users can
create an account, browse products, receive personalized
recommendations, and place orders.
"""


USER_TEXT = """
To create an account and receive personalized recommendations,
please provide the following information:

- Full name
- Email address
- Phone number
- Date of birth
- Gender
- Annual income
- Precise location
- Access to your contacts
- Browsing history
- Device information

We may share your information with trusted partners, advertising
partners, analytics providers, and other third-party service
providers to improve our services and provide personalized
advertising.

By continuing, you agree to our collection and use of your
personal information.
"""


# -------------------------------------------------------------------
# Run Test
# -------------------------------------------------------------------

def main():
    """
    Run a complete FAIRLENS backend test.
    """

    print("=" * 60)
    print("FAIRLENS - AI Privacy Risk Scanner")
    print("=" * 60)

    print("\nTesting service:")
    print(SERVICE_DESCRIPTION.strip())

    print("\nSending data for analysis...")
    print("-" * 60)

    result = run_risk_analysis(
        service_description=SERVICE_DESCRIPTION,
        user_text=USER_TEXT,
    )

    # ---------------------------------------------------------------
    # Handle failure
    # ---------------------------------------------------------------

    if not result["success"]:

        print("\n❌ FAIRLENS ANALYSIS FAILED")
        print("-" * 60)
        print(
            "Error:",
            result["error"],
        )

        return

    # ---------------------------------------------------------------
    # Handle successful analysis
    # ---------------------------------------------------------------

    analysis = result["result"]

    print("\n✅ FAIRLENS ANALYSIS COMPLETED")
    print("=" * 60)

    # ---------------------------------------------------------------
    # Overall Risk
    # ---------------------------------------------------------------

    overall_risk = analysis.get(
        "overall_risk",
        {},
    )

    print("\n🔍 OVERALL RISK")
    print("-" * 60)

    print(
        "Risk Level:",
        overall_risk.get(
            "level",
            "Unknown",
        ),
    )

    print(
        "Risk Score:",
        overall_risk.get(
            "score",
            "Unknown",
        ),
    )

    print(
        "Summary:",
        overall_risk.get(
            "summary",
            "No summary available.",
        ),
    )

    # ---------------------------------------------------------------
    # Detected Data Summary
    # ---------------------------------------------------------------

    data_summary = analysis.get(
        "detected_data_summary",
        {},
    )

    print("\n📊 DETECTED DATA SUMMARY")
    print("-" * 60)

    print(
        "Total detected requests:",
        data_summary.get(
            "total_requests",
            0,
        ),
    )

    print(
        "Sensitive requests:",
        data_summary.get(
            "sensitive_requests",
            0,
        ),
    )

    print(
        "Unique data categories:",
        data_summary.get(
            "unique_categories",
            0,
        ),
    )

    # ---------------------------------------------------------------
    # Individual Data Requests
    # ---------------------------------------------------------------

    data_requests = analysis.get(
        "data_requests",
        [],
    )

    print("\n🔐 DATA REQUESTS")
    print("-" * 60)

    if not data_requests:

        print(
            "No individual data requests were detected."
        )

    else:

        for index, request in enumerate(
            data_requests,
            start=1,
        ):

            print(
                f"\n{index}. "
                f"{request.get('data_name', 'Unknown')}"
            )

            print(
                "   Classification:",
                request.get(
                    "classification",
                    "Unknown",
                ),
            )

            print(
                "   Sensitive:",
                request.get(
                    "sensitive",
                    False,
                ),
            )

            print(
                "   Necessity:",
                request.get(
                    "necessity",
                    "Unknown",
                ),
            )

            print(
                "   Risk Level:",
                request.get(
                    "risk_level",
                    "Unknown",
                ),
            )

            print(
                "   Minimization Concern:",
                request.get(
                    "minimization_concern",
                    False,
                ),
            )

            print(
                "   Reasoning:",
                request.get(
                    "reasoning",
                    "No reasoning provided.",
                ),
            )

            print(
                "   Recommended Action:",
                request.get(
                    "recommended_action",
                    "No recommendation provided.",
                ),
            )

    # ---------------------------------------------------------------
    # Risk Categories
    # ---------------------------------------------------------------

    risk_categories = analysis.get(
        "risk_categories",
        {},
    )

    print("\n📈 RISK CATEGORIES")
    print("-" * 60)

    for category, details in risk_categories.items():

        print(
            f"\n{category}:"
        )

        print(
            "   Level:",
            details.get(
                "level",
                "Unknown",
            ),
        )

        print(
            "   Score:",
            details.get(
                "score",
                0,
            ),
        )

        print(
            "   Reason:",
            details.get(
                "reason",
                "No reason provided.",
            ),
        )

    # ---------------------------------------------------------------
    # Key Findings
    # ---------------------------------------------------------------

    print("\n⚠️ KEY FINDINGS")
    print("-" * 60)

    key_findings = analysis.get(
        "key_findings",
        [],
    )

    if not key_findings:

        print(
            "No key findings were returned."
        )

    else:

        for finding in key_findings:

            print(
                f"• {finding}"
            )

    # ---------------------------------------------------------------
    # Recommended Actions
    # ---------------------------------------------------------------

    print("\n💡 RECOMMENDED ACTIONS")
    print("-" * 60)

    recommended_actions = analysis.get(
        "recommended_actions",
        [],
    )

    if not recommended_actions:

        print(
            "No recommended actions were returned."
        )

    else:

        for action in recommended_actions:

            print(
                f"• {action}"
            )

    # ---------------------------------------------------------------
    # Full JSON Output
    # ---------------------------------------------------------------

    print("\n📦 RAW JSON RESULT")
    print("=" * 60)

    print(
        json.dumps(
            analysis,
            indent=4,
        )
    )

    print("\n")
    print("=" * 60)
    print("FAIRLENS TEST COMPLETE")
    print("=" * 60)


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
