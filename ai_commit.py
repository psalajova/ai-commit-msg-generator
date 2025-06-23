import subprocess


def get_git_diff():
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


# Example of how to use it (for testing purposes, this part won't be in the final CLI directly)
# python3 ./ai_commit.py
if __name__ == "__main__":
    diff_content = get_git_diff()
    if diff_content.startswith("Error"):
        print(diff_content)
    elif not diff_content.strip():
        print("No staged changes found. Please stage your changes using 'git add .'")
    else:
        print(diff_content)
