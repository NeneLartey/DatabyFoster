#!/bin/bash

# Quick AWS App Runner deployment script
set -e

SERVICE_NAME="foster-survey-app"
GITHUB_REPO="https://github.com/NeneLartey/DatabyFoster"

echo "🚀 Deploying to AWS App Runner..."

# Create App Runner service
aws apprunner create-service \
  --service-name $SERVICE_NAME \
  --source-configuration '{
    "CodeRepository": {
      "RepositoryUrl": "'$GITHUB_REPO'",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY"
      }
    },
    "AutoDeploymentsEnabled": true
  }' \
  --instance-configuration '{
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  }'

echo "✅ App Runner service created! Check AWS Console for deployment status."
echo "🌐 Your app will be available at the App Runner service URL in a few minutes." 