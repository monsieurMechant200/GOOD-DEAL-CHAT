# GOOD-DEAL-CHAT

A knowledge-grounded conversational interface that empowers GOOD-DEAL training alumni to access core concepts and domain expertise on demand. Built with Flask, Mistral AI, and an integrated knowledge management system.

## Overview

GOOD-DEAL-CHAT is a specialized AI chat assistant designed for learners who have completed the GOOD-DEAL training program. It serves as a quick-reference companion for daily professional use—answering questions about Excel workflows, financial calculations, inventory management, Pareto analysis, and prompt engineering with responses grounded in a curated knowledge base.

The system combines a clean, cosmic-themed web interface with a Python backend that orchestrates requests to the Mistral AI API, enriched by a domain-specific knowledge base that ensures accurate, contextually relevant responses.

## Architecture

```
GOOD-DEAL-CHAT/
├── server.py                    Flask application & API layer
├── static/
│   ├── index.html               Responsive HTML interface with animated starfield
│   ├── app.js                   Client-side messaging logic & Markdown rendering
│   └── style.css                Cosmic theme styling
├── convert_csv_to_txt.py        Knowledge base transformation utility
├── knowledge_base.csv           Structured Q&A dataset
├── knowledge.txt                Compiled system context (generated)
├── requirements.txt             Python dependencies
├── Procfile                     Heroku deployment configuration
└── LICENSE                      MIT License
```

### How It Works

1. **Backend (server.py)** — Flask application that:
   - Loads the knowledge base into memory on startup
   - Exposes a `/chat` endpoint that accepts user messages
   - Enriches requests with system context from `knowledge.txt`
   - Proxies to the Mistral AI API with fixed parameters (temperature: 0.3, max_tokens: 1024)
   - Returns formatted responses to the client

2. **Frontend (static/)** — Responsive web interface with:
   - Real-time chat bubbles with Markdown rendering (via marked.js)
   - Animated starfield canvas background
   - Auto-expanding textarea for messages
   - Loading states and error recovery
   - Accessibility features (ARIA labels, semantic HTML)

3. **Knowledge Base System** — Two-stage pipeline:
   - `knowledge_base.csv` — Structured questions, expert answers, and concrete examples
   - `convert_csv_to_txt.py` — Transforms CSV into system prompt context
   - `knowledge.txt` — Injected into every request as the LLM's reference material

## Getting Started

### Prerequisites

- Python 3.8+
- A Mistral AI API key (sign up at https://console.mistral.ai)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/monsieurMechant200/GOOD-DEAL-CHAT.git
   cd GOOD-DEAL-CHAT
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   echo "MISTRAL_API_KEY=<your_mistral_api_key>" > .env
   ```

### Running Locally

```bash
python server.py
```

The app will start at `http://localhost:5000`. Visit the URL in your browser and begin chatting.

### Deploying to Heroku

1. Ensure the Procfile is in place (already included).

2. Set the environment variable:
   ```bash
   heroku config:set MISTRAL_API_KEY=<your_mistral_api_key> -a <app-name>
   ```

3. Push to Heroku:
   ```bash
   git push heroku main
   ```

## Knowledge Base Management

To update the knowledge base:

1. **Edit** `knowledge_base.csv` with new or revised Q&A entries (delimiter: `;`).

2. **Regenerate** the system context:
   ```bash
   python convert_csv_to_txt.py
   ```
   This produces `knowledge.txt`, which will be reloaded on the next server restart.

3. **Commit** both files to version control:
   ```bash
   git add knowledge_base.csv knowledge.txt
   git commit -m "Update knowledge base"
   ```

## Configuration

Key parameters in `server.py`:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Model** | `mistral-small` | Can be changed to `mistral-medium` for higher precision |
| **Temperature** | `0.3` | Lower = more deterministic; higher = more creative |
| **Max Tokens** | `1024` | Maximum response length |
| **API URL** | `https://api.mistral.ai/v1/chat/completions` | Mistral endpoint |

## Security Considerations

- **API Key**: Never commit `.env` files to version control. Use environment variables in production.
- **HTML Content**: User messages are plaintext-escaped; assistant responses are rendered via marked.js (which sanitizes by default).
- **Timeout**: API requests enforce a 30-second timeout to prevent hanging connections.

## Development

### Running Tests

Currently, no automated test suite is included. For manual testing:

```bash
# Terminal 1: Start the server
python server.py

# Terminal 2: Send test requests
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Comment utiliser VLOOKUP en Excel?"}]}'
```

### Extending the System

- **Custom styling**: Modify `static/style.css`.
- **UI behavior**: Edit `static/app.js`.
- **Backend logic**: Extend `server.py` with new endpoints or middleware.
- **Knowledge content**: Update `knowledge_base.csv` and regenerate.

## Dependencies

- **Flask** — Web framework for Python
- **requests** — HTTP library for Mistral API calls
- **python-dotenv** — Environment variable management
- **gunicorn** — WSGI server for production (Heroku)
- **marked.js** — Client-side Markdown parser (CDN-loaded)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support & Feedback

For issues, feature requests, or questions:
1. Check existing issues on GitHub.
2. Open a new issue with a clear title and description.
3. Include any relevant error logs or screenshots.

---

**Built with ✦ for GOOD-DEAL alumni**
