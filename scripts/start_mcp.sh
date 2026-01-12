#!/bin/bash
# Start MCP Server for Skill Prompt Generator

cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Run MCP server
python -m mcp_server.server
