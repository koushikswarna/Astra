"""Allow running as `python -m astra`."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="astra",
        description="Astra — local AI assistant with memory and personality",
    )
    parser.add_argument(
        "--voice", action="store_true",
        help="Enable voice input/output (requires pyttsx3 + SpeechRecognition)",
    )
    parser.add_argument(
        "--ui", choices=["cli", "streamlit"], default="cli",
        help="Which interface to launch (default: cli)",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--personality",
        choices=["default", "professional", "casual", "edgy", "nerd", "zen"],
        default=None,
        help="Use a personality preset instead of random",
    )

    args, _ = parser.parse_known_args()

    if args.ui == "streamlit":
        from astra.ui.web import run as run_web
        run_web()
    else:
        from astra.ui.cli import run as run_cli
        run_cli(voice=args.voice)


if __name__ == "__main__":
    main()
