"""Core agent engine — handles conversation with AWS Bedrock (Claude)."""

import json
import boto3
from agent.prompts import SYSTEM_PROMPT, SUMMARY_PROMPT


def get_client(region: str = "us-east-1"):
    """Create a Bedrock Runtime client."""
    return boto3.client("bedrock-runtime", region_name=region)


def get_agent_response(client, messages: list[dict]) -> str:
    """Get a response from Claude via Bedrock given the conversation history."""
    # Convert messages to Bedrock format (separate system from conversation)
    bedrock_messages = []
    for msg in messages:
        bedrock_messages.append({
            "role": msg["role"],
            "content": [{"type": "text", "text": msg["content"]}],
        })

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0.7,
        "system": SYSTEM_PROMPT,
        "messages": bedrock_messages,
    })

    response = client.invoke_model(
        modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def generate_summary(client, messages: list[dict], project_name: str) -> str:
    """Generate the executive summary from the full conversation."""
    summary_instruction = SUMMARY_PROMPT.format(project_name=project_name)

    bedrock_messages = []
    for msg in messages:
        bedrock_messages.append({
            "role": msg["role"],
            "content": [{"type": "text", "text": msg["content"]}],
        })

    # Add the summary request as a user message
    bedrock_messages.append({
        "role": "user",
        "content": [{"type": "text", "text": summary_instruction}],
    })

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
        "temperature": 0.5,
        "system": SYSTEM_PROMPT,
        "messages": bedrock_messages,
    })

    response = client.invoke_model(
        modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def parse_phase(response: str) -> dict:
    """Extract phase information from the agent's response."""
    phase_info = {"phase": "DISCOVERY", "progress": 0}

    for line in response.split("\n"):
        if line.strip().startswith("[PHASE:"):
            try:
                content = line.strip().strip("[]")
                parts = content.split("|")
                phase = parts[0].replace("PHASE:", "").strip()
                progress = int(parts[1].replace("PROGRESS:", "").replace("%", "").strip())
                phase_info = {"phase": phase, "progress": progress}
            except (IndexError, ValueError):
                pass

    return phase_info
