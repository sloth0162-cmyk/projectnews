from services.llm_utils import generate_summary


def summarize_text(content: str):
    """Summarize a single article using the LLM."""

    print("🧠 SUMMARIZER: Starting...")
    print(f"📝 Input content length: {len(content)} characters")

    try:
        summary = generate_summary(content)

        if not summary:
            print("⚠️ SUMMARIZER: Returned empty summary")
            return ""

        print("✅ SUMMARIZER: Success")
        print(f"📝 Summary length: {len(summary)} characters")

        return summary

    except Exception as e:
        print("❌ SUMMARIZER: FAILED")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error: {e}")

        return ""