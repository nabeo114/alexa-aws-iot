variable "aws_region" {
  description = "AWS region where resources are deployed"
  type        = string
}

variable "project_name" {
  description = "Project tag value"
  type        = string
  default     = "alexa-aws-iot"
}

variable "environment" {
  description = "Environment tag value"
  type        = string
  default     = "prod"
}

variable "default_tags" {
  description = "Additional AWS tags to merge with the always-applied Project/Environment tags."
  type        = map(string)
  default     = {}
}

variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
}

variable "lambda_role_name" {
  description = "IAM role name used by Lambda"
  type        = string
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.12"
}

variable "lambda_handler" {
  description = "Lambda handler entrypoint"
  type        = string
  default     = "src.lambda_handler.lambda_handler"
}

variable "lambda_timeout" {
  description = "Lambda timeout seconds"
  type        = number
  default     = 10
}

variable "lambda_memory_size" {
  description = "Lambda memory size MB"
  type        = number
  default     = 128
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name used by the Lambda"
  type        = string
}

variable "dynamodb_partition_key" {
  description = "Partition key attribute name for the DynamoDB lookup"
  type        = string
}

variable "dynamodb_partition_name" {
  description = "Partition key value used for the DynamoDB lookup"
  type        = string
}

variable "lambda_zip_path" {
  description = "Path to Lambda deployment zip"
  type        = string
  default     = "../../dist/alexa-aws-iot-lambda.zip"
}

variable "alexa_skill_id" {
  description = "Alexa skill ID (amzn1.ask.skill.xxxx) allowed to invoke this Lambda. Leave empty to skip managing the trigger permission."
  type        = string
  default     = ""
}
