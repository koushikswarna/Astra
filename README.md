# Astra

A local AI assistant that runs entirely on your machine. Supports conversational chat with personality, short-term and long-term semantic memory, sentiment analysis, voice I/O, and a web interface.

## Setup

```bash
pip install -r requirements.txt
python scripts/download_models.py  # pre-download models for offline use
```

## Usage

```bash
# CLI chat
python main.py

# CLI with voice input/output
python main.py --voice

# Web UI (Streamlit)
streamlit run main.py -- --ui streamlit

# Run as module
python -m astra
```

## Commands (CLI)

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `remember <text>` | Save to long-term memory |
| `recall <query>` | Search long-term memory |
| `history` | Show conversation history |
| `clear` | Clear conversation history |
| `personality` | Show current personality |
| `status` | Show session stats |
| `quit` / `exit` | Exit |

## Configuration

Astra looks for `~/.astra/config.yaml` for settings. You can also use environment variables:

```bash
ASTRA_CHAT_MODEL=distilgpt2
ASTRA_TEMPERATURE=0.8
ASTRA_MAX_NEW_TOKENS=120
ASTRA_ENABLE_SENTIMENT=true
ASTRA_ENABLE_LTM=true
ASTRA_DEBUG=false
```

## Development

```bash
make dev        # install dev dependencies
make test       # run tests
make lint       # run linter
make test-cov   # test with coverage report
```

## Project Structure

```
astra/
├── config/     # configuration system (YAML, env vars, defaults)
├── core/       # engine, session management, events, hooks
├── models/     # transformer model loading and text generation
├── memory/     # short-term (sliding window) and long-term (vector) memory
├── nlp/        # sentiment analysis, pre/post processing, content filters
├── voice/      # speech recognition and text-to-speech
├── pipelines/  # chat processing pipeline and middleware
├── storage/    # JSON and ChromaDB storage backends
├── plugins/    # plugin system for extensibility
├── ui/
│   ├── cli/    # terminal interface
│   └── web/    # Streamlit web interface
└── utils/      # text helpers, logging, timing, decorators
```
