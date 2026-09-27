#!/usr/bin/env bash
set -euo pipefail
: "${ACR_NAME:?Set ACR_NAME after terraform apply output/portal lookup}"
IMAGE_TAG="${IMAGE_TAG:-1.0.0}"
az acr login --name "$ACR_NAME"
docker build -t "$ACR_NAME.azurecr.io/multicloud-agentic-ai:$IMAGE_TAG" .
docker push "$ACR_NAME.azurecr.io/multicloud-agentic-ai:$IMAGE_TAG"
echo "Set deployment/azure container_image to $ACR_NAME.azurecr.io/multicloud-agentic-ai:$IMAGE_TAG and terraform apply again."
