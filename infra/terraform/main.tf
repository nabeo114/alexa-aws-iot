locals {
  lambda_role_name = var.lambda_role_name
  lambda_environment = {
    Region        = var.aws_region
    TableName     = var.dynamodb_table_name
    PartitionKey  = var.dynamodb_partition_key
    PartitionName = var.dynamodb_partition_name
  }
  lambda_dynamodb_table_arn = format(
    "arn:%s:dynamodb:%s:%s:table/%s",
    data.aws_partition.current.partition,
    var.aws_region,
    data.aws_caller_identity.current.account_id,
    var.dynamodb_table_name
  )
}

data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

resource "aws_iam_role" "lambda_exec" {
  name        = local.lambda_role_name
  path        = "/"
  description = "Allows Lambda functions to call AWS services on your behalf."
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  max_session_duration = 3600

  lifecycle {
    ignore_changes = [
      tags,
      tags_all,
    ]
  }
}

resource "aws_lambda_function" "alexa_skill" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn
  runtime       = var.lambda_runtime
  handler       = var.lambda_handler
  filename      = var.lambda_zip_path

  source_code_hash = filebase64sha256(var.lambda_zip_path)
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory_size
  publish          = false

  environment {
    variables = local.lambda_environment
  }

  lifecycle {
    ignore_changes = [
      publish,
      tags,
      tags_all,
    ]
  }
}

resource "aws_lambda_permission" "alexa_invoke" {
  count = var.alexa_skill_id != "" ? 1 : 0

  statement_id  = "AllowInvokeFromAlexaSkillsKit"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.alexa_skill.function_name
  principal     = "alexa-appkit.amazon.com"

  event_source_token = var.alexa_skill_id
}

resource "aws_iam_policy" "lambda_dynamodb_read" {
  name = "${var.project_name}-lambda-device-access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:GetItem"]
        Resource = local.lambda_dynamodb_table_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_read" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_dynamodb_read.arn
}
