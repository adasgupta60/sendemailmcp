# Gmail MCP Server (Remote Callable)

This MCP server exposes one tool:

- `send_gmail(recipient_email, body, subject?)`

It sends email using your Gmail account through Gmail SMTP.

## 1) Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Then edit `.env` and set:

- `GMAIL_ADDRESS`: your Gmail address
- `GMAIL_APP_PASSWORD`: Gmail app password (recommended), not your normal Gmail password

Load env vars:

```bash
set -a
source .env
set +a
```

## 2) Run for remote MCP clients

Use HTTP transport so remote clients can call the server:

```bash
fastmcp run server.py:mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

Remote MCP clients can connect to:

- `http://<your-server-ip>:8000/mcp`

If your client expects a different endpoint, check that client's MCP transport docs.

## 3) Minimal MCP client test

Use two terminals.

Terminal 1 (start server):

```bash
source .venv/bin/activate
set -a && source .env && set +a
fastmcp run server.py:mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

Terminal 2 (run minimal client):

```bash
source .venv/bin/activate
python3 test_client.py \
  --url http://127.0.0.1:8000/mcp \
  --to your-recipient@gmail.com \
  --body "Hello from MCP test client" \
  --subject "MCP Test"
```

Expected output:

- tool list includes `send_gmail`
- tool response shows success with timestamp

## 4) Tool contract

- Tool name: `send_gmail`
- Inputs:
  - `recipient_email` (string, required)
  - `body` (string, required)
  - `subject` (string, optional, default: `Message from MCP server`)
- Output:
  - Success message with UTC timestamp.

## Gmail security notes

- Gmail commonly blocks plain account passwords for SMTP automation.
- Use a Google App Password (requires 2-Step Verification on the Google account).
- Keep credentials in `.env` and never commit them.
