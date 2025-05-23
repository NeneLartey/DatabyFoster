# AWS Deployment Guide for Income Spending Survey Tool

This guide provides step-by-step instructions for deploying your Flask survey application to AWS using different methods.

## Prerequisites

1. **AWS CLI installed and configured**
   ```bash
   aws configure
   ```

2. **Docker installed locally**

3. **AWS Account with appropriate permissions**
   - ECR (Elastic Container Registry)
   - ECS (Elastic Container Service)
   - VPC, Security Groups
   - IAM roles
   - Application Load Balancer (ALB)

## Deployment Options

### Option 1: AWS ECS with Fargate (Recommended) 🚀

This is the most scalable and managed approach.

#### Step 1: Set Up Database

**Option A: MongoDB Atlas (Recommended)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Get your connection string
4. Whitelist your AWS region's IP ranges

**Option B: Amazon DocumentDB**
1. Create DocumentDB cluster in AWS
2. Note the connection string

#### Step 2: Prepare Application

```bash
# Make the deployment script executable
chmod +x aws-deploy.sh

# Run the deployment preparation
./aws-deploy.sh
```

#### Step 3: Create IAM Roles

Create these IAM roles in AWS Console:

**ecsTaskExecutionRole:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

Attach policy: `AmazonECSTaskExecutionRolePolicy`

**ecsTaskRole:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

#### Step 4: Update Task Definition

1. Edit `task-definition.json`
2. Replace `YOUR_ACCOUNT_ID` with your AWS account ID
3. Replace `YOUR_MONGODB_CONNECTION_STRING` with your database connection string

#### Step 5: Create CloudWatch Log Group

```bash
aws logs create-log-group --log-group-name /ecs/survey-task --region us-east-1
```

#### Step 6: Register Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json --region us-east-1
```

#### Step 7: Create Application Load Balancer

1. Go to AWS Console → EC2 → Load Balancers
2. Create Application Load Balancer
3. Configure:
   - Name: `survey-alb`
   - Internet-facing
   - Select your VPC and at least 2 subnets
4. Create target group:
   - Name: `survey-targets`
   - Protocol: HTTP
   - Port: 5000
   - Target type: IP

#### Step 8: Create ECS Service

```bash
aws ecs create-service \
  --cluster survey-cluster \
  --service-name survey-service \
  --task-definition survey-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345,subnet-67890],securityGroups=[sg-12345],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/survey-targets/1234567890123456,containerName=survey-app,containerPort=5000 \
  --region us-east-1
```

Replace the subnet IDs, security group ID, and target group ARN with your actual values.

### Option 2: AWS App Runner (Simplest) 🏃‍♂️

AWS App Runner is the simplest option for containerized web applications.

#### Step 1: Push to GitHub

Ensure your code is in a GitHub repository.

#### Step 2: Create App Runner Service

1. Go to AWS Console → App Runner
2. Create service
3. Choose "Source code repository"
4. Connect to GitHub and select your repository
5. Configure build settings:
   ```yaml
   version: 1.0
   runtime: docker
   build:
     commands:
       build:
         - echo Build started on `date`
         - docker build -t survey-app .
   run:
     runtime-version: latest
     command: gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
     network:
       port: 5000
       env: PORT
   ```

#### Step 3: Configure Environment Variables

Add environment variables in App Runner:
- `MONGO_URI`: Your MongoDB connection string
- `FLASK_ENV`: production

### Option 3: AWS Elastic Beanstalk 🌱

Good for quick deployments with minimal configuration.

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize Elastic Beanstalk

```bash
eb init
# Choose region
# Choose platform: Docker
# Choose application name: survey-app
```

#### Step 3: Create Environment

```bash
eb create survey-production
```

#### Step 4: Set Environment Variables

```bash
eb setenv MONGO_URI=your_mongodb_connection_string
eb setenv FLASK_ENV=production
```

#### Step 5: Deploy

```bash
eb deploy
```

### Option 4: AWS Lambda + API Gateway (Serverless) ⚡

For low-traffic applications with cost optimization.

#### Step 1: Install Zappa

```bash
pip install zappa
```

#### Step 2: Initialize Zappa

```bash
zappa init
```

#### Step 3: Update zappa_settings.json

```json
{
    "production": {
        "app_function": "app.app",
        "aws_region": "us-east-1",
        "runtime": "python3.9",
        "s3_bucket": "your-zappa-deployments-bucket",
        "environment_variables": {
            "MONGO_URI": "your_mongodb_connection_string",
            "FLASK_ENV": "production"
        }
    }
}
```

#### Step 4: Deploy

```bash
zappa deploy production
```

## Post-Deployment Steps

### 1. Configure Domain (Optional)

**For ECS/ALB:**
1. Route 53 → Create hosted zone
2. Create A record pointing to ALB

**For App Runner:**
1. App Runner console → Custom domains
2. Add your domain

### 2. Set Up SSL Certificate

1. AWS Certificate Manager
2. Request public certificate
3. Add to load balancer/App Runner

### 3. Configure Monitoring

**CloudWatch Alarms:**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "High-CPU-Survey-App" \
  --alarm-description "Alarm when CPU exceeds 70%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 70 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### 4. Backup Strategy

**For MongoDB Atlas:**
- Automatic backups included

**For DocumentDB:**
- Enable automated backups
- Set retention period

## Cost Optimization Tips

1. **Use Spot Instances** (for ECS if applicable)
2. **Right-size your resources** (start small, scale up)
3. **Use CloudWatch** to monitor usage
4. **Set up billing alerts**

## Security Best Practices

1. **Use VPC** with private subnets
2. **Configure security groups** to allow only necessary traffic
3. **Use IAM roles** with least privilege
4. **Enable CloudTrail** for auditing
5. **Use AWS Secrets Manager** for sensitive data

## Troubleshooting

### Common Issues:

1. **Container fails to start:**
   - Check CloudWatch logs
   - Verify environment variables
   - Test locally first

2. **Database connection issues:**
   - Check security groups
   - Verify connection string
   - Test from EC2 instance in same VPC

3. **Load balancer health checks fail:**
   - Verify target group configuration
   - Check application port
   - Review health check path

### Useful Commands:

```bash
# View ECS service events
aws ecs describe-services --cluster survey-cluster --services survey-service

# View CloudWatch logs
aws logs describe-log-streams --log-group-name /ecs/survey-task

# Check task status
aws ecs list-tasks --cluster survey-cluster --service-name survey-service
```

## Recommended Deployment Path

For most use cases, I recommend:
1. **Start with App Runner** for simplicity
2. **Move to ECS + Fargate** when you need more control
3. **Consider Lambda** only for very low traffic

Choose ECS + Fargate if you need:
- Custom networking
- Advanced load balancing
- Integration with other AWS services
- Fine-grained control over scaling

Choose App Runner if you want:
- Simplest deployment
- Automatic scaling
- Built-in CI/CD
- Minimal AWS knowledge required 