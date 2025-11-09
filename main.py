#!/usr/bin/env python3
"""
Literature Assistant - Main Entry Point

This script provides a command-line interface to:
1. Start the backend server
2. Verify API configuration
3. Run basic tests

For web interface, use the Flask backend in backend/api/app.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_api_keys():
    """Verify that OpenAI API key is configured."""
    openai_key = os.getenv("OPENAI_API_KEY")

    print("=" * 50)
    print("API Configuration Check")
    print("=" * 50)

    if openai_key:
        print("✓ OPENAI_API_KEY: Configured")
    else:
        print("✗ OPENAI_API_KEY: Not found")
        print("  Please add your OpenAI API key to .env file")

    print("=" * 50)

    if not openai_key:
        print("\nError: OpenAI API key not configured!")
        print("Please copy .env.example to .env and add your API key.")
        return False

    return True


def start_backend_server():
    """Start the Flask backend server."""
    print("\nStarting Flask backend server...")
    print("Server will run on http://localhost:5001")
    print("(Using port 5001 because macOS uses port 5000 for AirPlay)")
    print("\nPress Ctrl+C to stop the server.\n")

    # Add backend/api to path and import Flask app
    backend_path = os.path.join(os.path.dirname(__file__), 'backend', 'api')
    sys.path.insert(0, backend_path)

    try:
        import app as backend_app # type: ignore
        backend_app.app.run(debug=True, port=5001, host='127.0.0.1')
    except ImportError as error:
        print(f"Error: Could not import Flask app: {error}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("\n" + "=" * 50)
    print("Literature Assistant")
    print("=" * 50)
    print("\nUsage:")
    print("  python main.py check      - Verify API configuration")
    print("  python main.py server     - Start the backend server")
    print("  python main.py help       - Show this help message")
    print("\nFor setup instructions, see SETUP.md")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "check":
        check_api_keys()
    elif command == "server":
        if check_api_keys():
            start_backend_server()
        else:
            sys.exit(1)
    elif command == "help":
        print_usage()
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)

