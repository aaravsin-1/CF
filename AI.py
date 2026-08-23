#!/usr/bin/env python3

import sys
import json
import urllib.request
import urllib.error

# ============================================================
# CONFIG
# ============================================================

GEMINI_API_KEY = ""

MODEL = "gemini-3.6-flash"

# ============================================================
# GEMINI
# ============================================================

def ask_gemini(prompt):

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODEL}:generateContent"
    )

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}", file=sys.stderr)
        print(e.read().decode(), file=sys.stderr)
        sys.exit(1)

    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except (KeyError, IndexError, TypeError):
        print("Unexpected Gemini response:", file=sys.stderr)
        print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) < 2:
        print('Usage: python main.py "question" [file]')
        sys.exit(1)

    question = sys.argv[1]

    # --------------------------------------------------------
    # No file supplied
    # --------------------------------------------------------

    if len(sys.argv) == 2:

        prompt = f"""
You are a helpful coding assistant.

Answer the following question clearly:

{question}
"""

        print(ask_gemini(prompt))
        return

    # --------------------------------------------------------
    # File supplied
    # --------------------------------------------------------

    filename = sys.argv[2]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

    except OSError as e:
        print(f"Could not read file: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = f"""
You are a coding assistant.

The user wants:

{question}

Here is the file:

----- BEGIN FILE: {filename} -----

{code}

----- END FILE -----

Return ONLY the complete resulting file.

Do NOT:
- explain the solution
- use Markdown code fences
- add commentary outside the code

Preserve the existing code where appropriate.
"""

    answer = ask_gemini(prompt)

    # Remove accidental markdown fences
    answer = answer.strip()

    if answer.startswith("```"):
        lines = answer.splitlines()

        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines.pop()

        answer = "\n".join(lines)

    print(answer)


if __name__ == "__main__":
    main()
