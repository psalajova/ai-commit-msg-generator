import os
import subprocess
import sys

import google.generativeai as genai
from google.generativeai.types import generation_types

MODEL_NAME = "gemini-2.0-flash"

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


def get_git_diff() -> str:
    """
    Fetches the staged Git diff from the current repository.
    The 'staged' diff means changes that have been added to the staging area
    (e.g., using `git add .`) but not yet committed.

    Returns:
        str: The Git diff output, or an error message if Git fails.
    """
    try:
        is_git_repo = subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"],
            text=True,
            stderr=subprocess.PIPE,  # Capture stderr to prevent it from printing to console directly
        ).strip()

        if is_git_repo != "true":
            return "Error: Not inside a Git repository."

        return subprocess.check_output(
            ["git", "diff", "--staged"], text=True, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        return f"Error executing git command: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: Git command not found. Please ensure Git is installed and in your system's PATH."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def generate_commit_message(diff_content: str) -> str:
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")

    if not diff_content.strip():
        return "Error: No diff content provided to generate a commit message."

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        For the following Git diff, generate a single, 
        short commit message (max 10 words and under 50 characters 
        for the subject line) that accurately summarizes the changes.
        Be precise, but don't sacrifice readability.

        Follow conventional commit style, using prefixes like 
        `feat:`, `fix:`... Start the subject line with a strong, imperative verb 
        ('Add', 'Fix', 'Remove', 'Update').

        Git Diff:
        ```diff
        {diff_content}
        ```

        Commit Message:
        """
        response = model.generate_content(prompt, stream=False)
        return validate_response(response)

    except Exception as e:
        return f"Error communicating with LLM: {e}"


def validate_response(response: generation_types.GenerateContentResponse) -> str:
    if (
        response.candidates
        and response.candidates[0].content
        and response.candidates[0].content.parts
        and response.candidates[0].content.parts[0].text
    ):
        return response.candidates[0].content.parts[0].text.strip()
    else:
        # If the LLM generates an empty or malformed response.
        return "Error: LLM did not generate a valid commit message. Response structure unexpected."


def main():
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    diff_content = get_git_diff()
    if diff_content.startswith("Error"):
        print(diff_content, file=sys.stderr)
        sys.exit(1)

    if not diff_content.strip():
        print("No staged changes found.", file=sys.stderr)
        print(
            "Please stage your changes first using 'git add .' or 'git add <files>'.",
            file=sys.stderr,
        )
        sys.exit(0)  # Exit successfully as there's nothing to do

    commit_msg = generate_commit_message(diff_content)

    if commit_msg.startswith("Error"):
        print(commit_msg, file=sys.stderr)
        sys.exit(1)

    print(f"{commit_msg}")


if __name__ == "__main__":
    main()
