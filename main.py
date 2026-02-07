"""Entry point for Astra.

Run directly:
    python main.py              # CLI mode
    python main.py --voice      # CLI with voice
    python main.py --ui streamlit   # (after: streamlit run main.py -- --ui streamlit)
"""

from astra.__main__ import main

if __name__ == "__main__":
    main()
