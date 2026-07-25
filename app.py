"""
FAIRLENS - Privacy & Data Collection Risk Scanner

User-facing Gradio application.

Users can:
1. Describe what a website or service does.
2. Paste text describing the information it collects.
3. Run FAIRLENS analysis.
4. View privacy risks, sensitive data, and recommendations.
5. View a visual risk breakdown chart.
"""

import gradio as gr
import plotly.graph_objects as go

from risk_analyzer import run_risk_analysis


# -------------------------------------------------------------------
# Application Configuration
# -------------------------------------------------------------------

APP_TITLE = "FAIRLENS"

APP_DESCRIPTION = """
**FAIRLENS** is an AI-powered privacy and data collection risk scanner.

Paste text from a signup form, privacy notice, consent request,
or data collection statement, and FAIRLENS will analyze:

- What personal data is being requested
- Which data may be sensitive
- Whether the data appears necessary
- Potential data minimization concerns
- Privacy risk categories
- Recommended actions
"""


# -------------------------------------------------------------------
# Risk Category Configuration
# -------------------------------------------------------------------

CATEGORY_NAMES = {
    "data_necessity": "Data Necessity",
    "data_sensitivity": "Data Sensitivity",
    "data_minimization": "Data Minimization",
    "transparency": "Transparency",
    "consent": "Consent & User Choice",
    "data_sharing": "Third-Party Data Sharing",
}


# -------------------------------------------------------------------
# Formatting Helpers
# -------------------------------------------------------------------

def format_data_requests(data_requests):
    """
    Format individual data requests into Markdown.
    """

    if not data_requests:
        return "No individual data requests were identified."

    output = []

    for index, request in enumerate(
        data_requests,
        start=1,
    ):

        data_name = request.get(
            "data_name",
            "Unknown data",
        )

        classification = request.get(
            "classification",
            "Unknown",
        )

        sensitive = request.get(
            "sensitive",
            False,
        )

        necessity = request.get(
            "necessity",
            "Unclear",
        )

        risk_level = request.get(
            "risk_level",
            "Unknown",
        )

        minimization_concern = request.get(
            "minimization_concern",
            False,
        )

        reasoning = request.get(
            "reasoning",
            "No reasoning provided.",
        )

        recommended_action = request.get(
            "recommended_action",
            "No recommendation provided.",
        )

        sensitive_text = (
            "Yes"
            if sensitive
            else "No"
        )

        minimization_text = (
            "Yes"
            if minimization_concern
            else "No"
        )

        section = f"""
### {index}. {data_name}

| Attribute | Assessment |
|---|---|
| Classification | {classification} |
| Sensitive Data | {sensitive_text} |
| Necessity | {necessity} |
| Risk Level | {risk_level} |
| Minimization Concern | {minimization_text} |

**Why this matters**

{reasoning}

**Recommended action**

{recommended_action}

---
"""

        output.append(
            section
        )

    return "\n".join(
        output
    )


def format_risk_categories(risk_categories):
    """
    Format risk category analysis into a Markdown table.
    """

    if not risk_categories:
        return "No risk category analysis was returned."

    rows = []

    for category, details in risk_categories.items():

        display_name = CATEGORY_NAMES.get(
            category,
            category.replace(
                "_",
                " ",
            ).title(),
        )

        level = details.get(
            "level",
            "Unknown",
        )

        score = details.get(
            "score",
            0,
        )

        reason = details.get(
            "reason",
            "No explanation provided.",
        )

        rows.append(
            f"| **{display_name}** | {level} | {score}/4 | {reason} |"
        )

    table = """
| Risk Category | Level | Score | Explanation |
|---|---|---|---|
"""

    table += "\n".join(
        rows
    )

    return table


def format_list(
    items,
    empty_message,
):
    """
    Format a list into Markdown bullet points.
    """

    if not items:
        return empty_message

    return "\n".join(
        f"- {item}"
        for item in items
    )


# -------------------------------------------------------------------
# Risk Chart
# -------------------------------------------------------------------

def create_risk_chart(risk_categories):
    """
    Create an interactive Plotly bar chart showing FAIRLENS
    risk scores across the six privacy risk categories.

    Risk scores range from 0 to 4.

    0 = Lowest risk
    4 = Highest risk
    """

    if not risk_categories:
        return None

    categories = []
    scores = []
    levels = []

    # Keep the chart in a consistent order.
    for category_key, display_name in CATEGORY_NAMES.items():

        details = risk_categories.get(
            category_key,
            {},
        )

        if not isinstance(
            details,
            dict,
        ):
            details = {}

        score = details.get(
            "score",
            0,
        )

        level = details.get(
            "level",
            "Unknown",
        )

        # Safely convert the score to an integer.
        try:
            score = int(score)
        except (
            TypeError,
            ValueError,
        ):
            score = 0

        # Keep scores within the expected 0-4 range.
        score = max(
            0,
            min(
                score,
                4,
            ),
        )

        categories.append(
            display_name
        )

        scores.append(
            score
        )

        levels.append(
            level
        )

    # Create horizontal bar chart.
    figure = go.Figure(
        data=[
            go.Bar(
                x=scores,
                y=categories,
                orientation="h",
                text=[
                    f"{score}/4 — {level}"
                    for score, level in zip(
                        scores,
                        levels,
                    )
                ],
                textposition="auto",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Risk Score: %{x}/4<br>"
                    "Risk Level: %{customdata}"
                    "<extra></extra>"
                ),
                customdata=levels,
            )
        ]
    )

    figure.update_layout(
        title="FAIRLENS Privacy Risk Profile",
        xaxis={
            "title": "Risk Score",
            "range": [
                0,
                4.5,
            ],
            "dtick": 1,
        },
        yaxis={
            "title": "",
        },
        height=450,
        margin={
            "l": 180,
            "r": 40,
            "t": 80,
            "b": 60,
        },
        template="plotly_white",
    )

    return figure


# -------------------------------------------------------------------
# Main Analysis Function
# -------------------------------------------------------------------

def analyze_privacy_risk(
    service_description,
    user_text,
):
    """
    Run FAIRLENS analysis and return formatted results
    together with a visual risk chart.
    """

    # ---------------------------------------------------------------
    # Validate user input
    # ---------------------------------------------------------------

    if not service_description or not service_description.strip():

        return (
            "## ⚠️ Missing Service Description\n\n"
            "Please describe what the website or service does.",
            "",
            None,
            "",
            "",
        )

    if not user_text or not user_text.strip():

        return (
            "## ⚠️ Missing Text to Analyze\n\n"
            "Please paste the privacy notice, signup form, "
            "permission request, or data collection text.",
            "",
            None,
            "",
            "",
        )

    # ---------------------------------------------------------------
    # Run FAIRLENS backend
    # ---------------------------------------------------------------

    response = run_risk_analysis(
        service_description=service_description,
        user_text=user_text,
    )

    # ---------------------------------------------------------------
    # Handle analysis errors
    # ---------------------------------------------------------------

    if not response.get(
        "success",
        False,
    ):

        error_message = response.get(
            "error",
            "An unknown error occurred.",
        )

        return (
            f"""
## ❌ Analysis Failed

**Error:**

{error_message}

Please check your configuration and try again.
""",
            "",
            None,
            "",
            "",
        )

    # ---------------------------------------------------------------
    # Extract analysis
    # ---------------------------------------------------------------

    analysis = response.get(
        "result",
        {},
    )

    overall_risk = analysis.get(
        "overall_risk",
        {},
    )

    risk_level = overall_risk.get(
        "level",
        "Unknown",
    )

    risk_score = overall_risk.get(
        "score",
        0,
    )

    risk_summary = overall_risk.get(
        "summary",
        "No summary available.",
    )

    risk_categories = analysis.get(
        "risk_categories",
        {},
    )

    # ---------------------------------------------------------------
    # Overall Risk Result
    # ---------------------------------------------------------------

    overall_output = f"""
# 🔍 FAIRLENS Privacy Risk Assessment

## Overall Risk: **{risk_level}**

### Risk Score

**{risk_score}/4**

### Summary

{risk_summary}

---

> **Note:** FAIRLENS provides an AI-assisted privacy risk assessment.
> It does not determine legal compliance and does not provide legal advice.
"""

    # ---------------------------------------------------------------
    # Data Requests
    # ---------------------------------------------------------------

    data_requests_output = format_data_requests(
        analysis.get(
            "data_requests",
            [],
        )
    )

    # ---------------------------------------------------------------
    # Risk Categories
    # ---------------------------------------------------------------

    risk_categories_output = format_risk_categories(
        risk_categories
    )

    # ---------------------------------------------------------------
    # Create Visual Risk Chart
    # ---------------------------------------------------------------

    risk_chart = create_risk_chart(
        risk_categories
    )

    # ---------------------------------------------------------------
    # Findings and Recommendations
    # ---------------------------------------------------------------

    key_findings = format_list(
        analysis.get(
            "key_findings",
            [],
        ),
        "No major findings were identified.",
    )

    recommended_actions = format_list(
        analysis.get(
            "recommended_actions",
            [],
        ),
        "No specific actions were recommended.",
    )

    actions_output = f"""
## ⚠️ Key Findings

{key_findings}

---

## 💡 Recommended Actions

{recommended_actions}
"""

    # ---------------------------------------------------------------
    # Return five outputs
    # ---------------------------------------------------------------

    return (
        overall_output,
        data_requests_output,
        risk_chart,
        risk_categories_output,
        actions_output,
    )


# -------------------------------------------------------------------
# Clear Function
# -------------------------------------------------------------------

def clear_analysis():
    """
    Clear all inputs and outputs.
    """

    return (
        "",
        "",
        "",
        None,
        "",
        "",
    )


# -------------------------------------------------------------------
# Gradio Application
# -------------------------------------------------------------------

with gr.Blocks(
    title=APP_TITLE,
) as demo:

    # ---------------------------------------------------------------
    # Header
    # ---------------------------------------------------------------

    gr.Markdown(
        f"""
# 🔍 {APP_TITLE}

### Privacy & Data Collection Risk Scanner

{APP_DESCRIPTION}
"""
    )

    gr.Markdown(
        """
---

### How it works

**Step 1:** Describe what the website or service does.

**Step 2:** Paste the text describing what information it asks users to provide.

**Step 3:** Click **Scan for Privacy Risks**.

**Step 4:** FAIRLENS analyzes the data collection practices and generates a risk report.

---
"""
    )

    # ---------------------------------------------------------------
    # Input Section
    # ---------------------------------------------------------------

    gr.Markdown(
        "## 1. Describe the Website or Service"
    )

    service_description = gr.Textbox(
        label="What does this website or service do?",
        placeholder=(
            "Example: An online clothing store where users "
            "can browse products, create accounts, and place orders."
        ),
        lines=4,
    )

    gr.Markdown(
        "## 2. Paste the Data Collection Text"
    )

    user_text = gr.Textbox(
        label="What information is the website asking you to provide?",
        placeholder=(
            "Paste text from a signup form, privacy notice, "
            "consent request, permission request, or data collection statement..."
        ),
        lines=12,
    )

    # ---------------------------------------------------------------
    # Buttons
    # ---------------------------------------------------------------

    with gr.Row():

        analyze_button = gr.Button(
            "🔍 Scan for Privacy Risks",
            variant="primary",
        )

        clear_button = gr.Button(
            "🗑️ Clear",
        )

    # ---------------------------------------------------------------
    # Results
    # ---------------------------------------------------------------

    gr.Markdown(
        "---"
    )

    gr.Markdown(
        "## 📊 FAIRLENS Analysis"
    )

    overall_output = gr.Markdown()

    # ---------------------------------------------------------------
    # Visual Risk Chart
    # ---------------------------------------------------------------

    gr.Markdown(
        "### 📈 Privacy Risk Profile"
    )

    risk_chart_output = gr.Plot(
        label="Privacy Risk Profile",
        show_label=False,
    )

    # ---------------------------------------------------------------
    # Detailed Data Requests
    # ---------------------------------------------------------------

    with gr.Accordion(
        "🔐 Detailed Data Requests",
        open=True,
    ):

        data_requests_output = gr.Markdown()

    # ---------------------------------------------------------------
    # Risk Category Breakdown
    # ---------------------------------------------------------------

    with gr.Accordion(
        "📋 Risk Category Breakdown",
        open=True,
    ):

        risk_categories_output = gr.Markdown()

    # ---------------------------------------------------------------
    # Findings and Recommendations
    # ---------------------------------------------------------------

    actions_output = gr.Markdown()

    # ---------------------------------------------------------------
    # Analyze Button
    # ---------------------------------------------------------------

    analyze_button.click(
        fn=analyze_privacy_risk,

        inputs=[
            service_description,
            user_text,
        ],

        outputs=[
            overall_output,
            data_requests_output,
            risk_chart_output,
            risk_categories_output,
            actions_output,
        ],
    )

    # ---------------------------------------------------------------
    # Clear Button
    # ---------------------------------------------------------------

    clear_button.click(
        fn=clear_analysis,

        inputs=[],

        outputs=[
            service_description,
            user_text,
            overall_output,
            risk_chart_output,
            data_requests_output,
            risk_categories_output,
            actions_output,
        ],
    )


# -------------------------------------------------------------------
# Launch FAIRLENS
# -------------------------------------------------------------------

if __name__ == "__main__":

    demo.launch()
