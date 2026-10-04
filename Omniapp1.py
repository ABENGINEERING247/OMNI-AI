# ============================================================
# GROK API
# ============================================================

class GrokAPIError(RuntimeError):
    """Grok API error that preserves the HTTP status code."""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(
            f"Grok API Error {status_code}: {message}"
        )


def call_grok(request, agent, api_key):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-3-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are OMNI AI, a multi-agent intelligent "
                    "assistant. The selected specialist agent is "
                    f"{agent}. "
                    "Respond as part of a multi-agent system. "
                    "Explain which agent should handle the request "
                    "and provide a practical structured response."
                ),
            },
            {
                "role": "user",
                "content": request,
            },
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=90,
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Unable to connect to Grok API: {exc}"
        ) from exc

    if response.status_code != 200:
        raise GrokAPIError(
            response.status_code,
            response.text,
        )

    try:
        data = response.json()

    except ValueError as exc:
        raise RuntimeError(
            "Grok API returned an invalid JSON response."
        ) from exc

    try:
        return data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "Unexpected response received from Grok API."
        )


# ============================================================
# AUTOMATIC DEMO FALLBACK
# ============================================================

def is_credit_or_quota_error(exc):
    """
    Detect Grok API errors caused by credits,
    quota, billing, balance or usage limits.
    """

    text = str(exc).lower()

    credit_keywords = [
        "insufficient",
        "insufficient credits",
        "credit",
        "credits",
        "quota",
        "rate limit",
        "rate_limit",
        "too many requests",
        "billing",
        "payment required",
        "payment",
        "balance",
        "usage limit",
        "usage_limit",
        "limit reached",
        "exceeded",
        "exhausted",
        "spending limit",
    ]

    if any(
        keyword in text
        for keyword in credit_keywords
    ):
        return True

    status_code = getattr(
        exc,
        "status_code",
        None
    )

    # Common API statuses related to
    # quota / billing / access limits.
    if status_code in {
        402,
        403,
        429,
    }:
        return True

    return False


def activate_demo_mode(reason=""):
    """
    Automatically switch OMNI AI to Demo Mode.
    """

    st.session_state[
        "operating_mode"
    ] = "🎮 Demo Mode"

    st.session_state[
        "grok_fallback_reason"
    ] = reason


def process_ai_request(
    request,
    agent,
    api_key
):
    """
    Try Grok first.

    If Grok credits, quota or billing limits
    are exhausted, automatically use Demo Mode.
    """

    # --------------------------------------------------------
    # NO API KEY
    # --------------------------------------------------------

    if not api_key:

        reason = (
            "XAI_API_KEY is not configured. "
            "OMNI AI automatically switched "
            "to Demo Mode."
        )

        activate_demo_mode(reason)

        return (
            demo_response(
                request,
                agent
            ),
            "🎮 Demo Mode — Automatic Fallback",
            reason,
        )

    # --------------------------------------------------------
    # TRY GROK
    # --------------------------------------------------------

    try:

        result = call_grok(
            request,
            agent,
            api_key
        )

        return (
            result,
            "🔑 Grok API Mode",
            "",
        )

    # --------------------------------------------------------
    # AUTOMATIC FALLBACK
    # --------------------------------------------------------

    except Exception as exc:

        if is_credit_or_quota_error(exc):

            reason = (
                "Grok API credits/quota/billing "
                "limit was reached. "
                "OMNI AI automatically switched "
                "to Demo Mode."
            )

            activate_demo_mode(
                reason
            )

            return (
                demo_response(
                    request,
                    agent
                ),
                "🎮 Demo Mode — Automatic Fallback",
                reason,
            )

        # Unexpected errors should remain visible.
        raise
