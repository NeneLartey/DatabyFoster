#!/bin/bash

# AWS ECS Deployment Script for Income Spending Survey Tool
# Make sure to run: chmod +x aws-deploy.sh

set -e

# Configuration variables
AWS_REGION="us-east-1"
CLUSTER_NAME="survey-cluster"
SERVICE_NAME="survey-service"
TASK_DEFINITION_NAME="survey-task"
ECR_REPOSITORY_NAME="survey-app"
IMAGE_TAG="latest"

echo "🚀 Starting AWS ECS deployment..."

# Step 1: Create ECR repository
echo "📦 Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION || echo "Repository might already exist"

# Get ECR login token
echo "🔐 Getting ECR login token..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com

# Step 2: Build and tag Docker image
echo "🏗️ Building Docker image..."
docker build -t $ECR_REPOSITORY_NAME:$IMAGE_TAG .

# Tag image for ECR
ECR_URI=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:$IMAGE_TAG
docker tag $ECR_REPOSITORY_NAME:$IMAGE_TAG $ECR_URI

# Step 3: Push image to ECR
echo "⬆️ Pushing image to ECR..."
docker push $ECR_URI

# Step 4: Create ECS cluster
echo "🏗️ Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION || echo "Cluster might already exist"

echo "✅ Deployment preparation complete!"
echo "📋 Next steps:"
echo "1. Create MongoDB Atlas cluster or use DocumentDB"
echo "2. Update MONGO_URI in task definition"
echo "3. Run the task definition and service creation commands"

echo ""
echo "🔗 Your ECR image URI: $ECR_URI" 