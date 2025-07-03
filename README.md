# Commit messages generator

A CLI app generating concise Git commit messages from staged diffs using Google's Gemini LLM.

## Features

- Fetches staged Git diff.
- Generates commit messages using `gemini-2.0-flash`.
- Provides a suggested `git commit` command.

## Setup & Installation

A free Gemini API key is required. Obtain one from Google AI Studio after logging in.
Set it as GEMINI_API_KEY environment variable:
`export GEMINI_API_KEY=<YOUR_KEY>`

## Usage

1. Navigate to a Git repository with staged changes.
2. Run the application: `python /path/to/ai_commit.py` (adjust path as needed).

## Example Output

```
$ python /path/to/ai_commit.py
feat: Add initial dependencies
```

For ease of use, you can also set an alias: `alias generate-commit-msg="python /path/to/ai_commit.py"`, to use like:
```
$ generate-commit-msg
feat: Add initial dependencies
```
