provider "aws" {
  region = "us-east-1"
}

# DynamoDB table
resource "aws_dynamodb_table" "job_scheduler" {
  name           = "JobScheduler"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "jobId"

  attribute {
    name = "jobId"
    type = "S"
  }
}

# IAM Role for Lambdas
resource "aws_iam_role" "lambda_exec_role" {
  name = "job_scheduler_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

# Attach policies
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "eventbridge_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess"
}

# Lambda: executeJob
resource "aws_lambda_function" "execute_job" {
  filename         = "../lambdas/executeJob/executeJob.zip"
  function_name    = "executeJob"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = filebase64sha256("../lambdas/executeJob/executeJob.zip")
}

# Lambda: createJob
resource "aws_lambda_function" "create_job" {
  filename         = "../lambdas/createJob/createJob.zip"
  function_name    = "createJob"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "index.lambda_handler"
  runtime          = "python3.10"
  source_code_hash = filebase64sha256("../lambdas/createJob/createJob.zip")

  environment {
    variables = {
      TABLE_NAME           = aws_dynamodb_table.job_scheduler.name
      TARGET_LAMBDA_ARN    = aws_lambda_function.execute_job.arn
    }
  }
}
