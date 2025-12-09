# Simple Agent

This is an exported Langflow application.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create a `.env` file based on the example below or export them directly.
   - Required variables:
OPENAI_API_KEY=

## Running

Run the application:
```bash
python main.py
```

## API Usage

The application exposes a REST API to run the flow.

### Run Flow
**POST** `/run`

Execute the flow with inputs.

#### Request Body
```json
{
  "inputs": {
    "input_value": "Hello, how are you?"
  },
  "session_id": "optional-session-id-for-memory"
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/run \
     -H "Content-Type: application/json" \
     -d '{"inputs": {"input_value": "User Message"}, "session_id": "my-session"}'
```

## Docker

Build and run with Docker:
```bash
docker build -t simple_agent .
docker run -p 8000:8000 --env-file .env simple_agent
```
