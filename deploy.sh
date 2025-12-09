#!/bin/bash
set -e

# =============================================================================
# Cloud Run Deployment Script for Simple Agent
# =============================================================================

# Configuration - Update these values or set as environment variables
PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
SERVICE_NAME="${SERVICE_NAME:-simple_agent}"
REGION="${REGION:-us-central1}"
REPO_NAME="${REPO_NAME:-langflow-exports}"

echo "=============================================="
echo "  Deploying Simple Agent to Cloud Run"
echo "=============================================="
echo ""
echo "Configuration:"
echo "  Project ID:   $PROJECT_ID"
echo "  Service Name: $SERVICE_NAME"
echo "  Region:       $REGION"
echo "  Repository:   $REPO_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth print-identity-token &> /dev/null; then
    echo "Error: Not authenticated with gcloud."
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

# Create Artifact Registry repository if it doesn't exist
echo ""
echo "Ensuring Artifact Registry repository exists..."
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Langflow exported applications" \
    2>/dev/null || echo "Repository already exists."

# Configure Docker for Artifact Registry
echo ""
echo "Configuring Docker authentication..."
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

# Build and push the image
echo ""
echo "Building and pushing Docker image..."
IMAGE_URL="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME"
docker build -t $IMAGE_URL .
docker push $IMAGE_URL

# Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_URL \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "$(grep -v '^#' .env 2>/dev/null | grep '=' | xargs | tr ' ' ',')" \
    || gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_URL \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated

# Get the service URL
echo ""
echo "=============================================="
echo "  Deployment Complete!"
echo "=============================================="
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo ""
echo "Service URL: $SERVICE_URL"
echo ""
echo "Test your deployment:"
echo "  curl -X POST $SERVICE_URL/run \\"
echo "       -H \"Content-Type: application/json\" \\"
echo "       -d '{"inputs": {"input_value": "Hello!"}, "session_id": ""}'"
