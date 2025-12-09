# Deploying Simple Agent to Google Cloud Run

This guide explains how to deploy your exported Langflow application to Google Cloud Run.

## Prerequisites

1. **Google Cloud SDK**: Install from https://cloud.google.com/sdk/docs/install
2. **Docker**: Install from https://docs.docker.com/get-docker/
3. **GCP Project**: Create a project at https://console.cloud.google.com

## Quick Deploy

### Option 1: Using the Deploy Script (Recommended)

```bash
# Make the script executable
chmod +x deploy.sh

# Set your project ID
export PROJECT_ID="your-gcp-project-id"

# Optional: Customize service name and region
export SERVICE_NAME="simple_agent"
export REGION="us-central1"

# Deploy!
./deploy.sh
```

### Option 2: Using Cloud Build

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Submit build
gcloud builds submit --config cloudbuild.yaml \
    --substitutions=_REGION=us-central1
```

### Option 3: Manual Deployment

```bash
# Set variables
PROJECT_ID="your-project-id"
SERVICE_NAME="simple_agent"
REGION="us-central1"

# Build the image
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated
```

## Environment Variables

Before deploying, ensure your `.env` file contains all required API keys:

```bash
# Required
OPENAI_API_KEY=your-key-here
# Add other keys as needed
```

The deploy script will automatically load variables from `.env`.

To set environment variables on an existing deployment:

```bash
gcloud run services update simple_agent \
    --region us-central1 \
    --set-env-vars "OPENAI_API_KEY=your-key"
```

## Testing Your Deployment

Once deployed, test your API:

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe simple_agent --region us-central1 --format 'value(status.url)')

# Test the API
curl -X POST "$SERVICE_URL/run" \
    -H "Content-Type: application/json" \
    -d '{"inputs": {"input_value": "Hello, how are you?"}, "session_id": ""}'

# Health check
curl "$SERVICE_URL/health"
```

## Monitoring

View logs:
```bash
gcloud run services logs read simple_agent --region us-central1
```

View in Console: https://console.cloud.google.com/run

## Troubleshooting

### Build Fails
- Ensure Docker is running
- Check requirements.txt for missing dependencies

### Deployment Fails  
- Verify you have Cloud Run Admin role
- Check that billing is enabled

### Runtime Errors
- Check Cloud Run logs for details
- Verify environment variables are set correctly
