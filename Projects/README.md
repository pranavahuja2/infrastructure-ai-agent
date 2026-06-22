# 🏗️ Infrastructure AI Agent

An AI-powered Solutions Engineer that conducts technical discovery sessions, identifies infrastructure requirements, generates architecture recommendations, and produces executive summaries.

Powered by **AWS Bedrock + Claude**.

## Features

- **Guided Discovery** — Conversational flow that asks the right questions
- **Technical Deep-Dive** — Covers scale, security, compliance, budget, and more
- **Architecture Recommendations** — Tailored cloud infrastructure designs with reasoning
- **Executive Summary** — Downloadable markdown report with full recommendations
- **Phase Tracking** — Visual progress through the discovery process

## Quick Start

### Prerequisites

- Python 3.10+
- AWS credentials with Bedrock access configured (`~/.aws/credentials` or environment variables)

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/infrastructure-ai-agent.git
cd infrastructure-ai-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## AWS Credentials

The app uses your local AWS credentials. Make sure you have Bedrock access:

```bash
# Verify your credentials
aws sts get-caller-identity

# Your IAM user/role needs the AmazonBedrockFullAccess policy
```

## Project Structure

```
infrastructure-ai-agent/
├── app.py                 # Streamlit UI and chat interface
├── agent/
│   ├── __init__.py
│   ├── engine.py          # AWS Bedrock integration and conversation logic
│   └── prompts.py         # System prompts and templates
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## How It Works

The agent follows a structured workflow:

1. **Discovery** — Understands the business context and high-level needs
2. **Technical Deep-Dive** — Asks targeted questions about scale, security, compliance
3. **Requirements Summary** — Structures findings into functional/non-functional requirements
4. **Architecture Recommendation** — Proposes cloud services with justifications
5. **Executive Summary** — Generates a downloadable professional report

## Customization

- **Change the model**: Edit `modelId` in `agent/engine.py` (e.g., `anthropic.claude-3-haiku-20240307-v1:0` for lower cost)
- **Modify the agent's behavior**: Edit prompts in `agent/prompts.py`
- **Add new phases**: Extend the `SYSTEM_PROMPT` with additional workflow steps

## Deploy to Streamlit Community Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. In "Advanced settings", add your AWS credentials as secrets:
   ```toml
   AWS_ACCESS_KEY_ID = "your-key"
   AWS_SECRET_ACCESS_KEY = "your-secret"
   AWS_DEFAULT_REGION = "us-east-1"
   ```
4. Deploy

## License

MIT
# infrastructure-ai-agent
