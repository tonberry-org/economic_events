data "aws_iam_policy_document" "lamda_exec_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ssm_secrets" {
  statement {
    actions = ["ssm:GetParameter"]
    resources = [
      "arn:aws:ssm:us-west-2:536213556125:parameter/eod/api_key",
      "arn:aws:ssm:us-west-2:536213556125:parameter/slack/*"
    ]
  }
}

resource "aws_iam_policy" "ssm_secrets" {
  name   = "EconomicEventSecrets"
  policy = data.aws_iam_policy_document.ssm_secrets.json
}
data "aws_iam_policy" "newrelic_license_key_policy" {
  arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/NewRelic-ViewLicenseKey-us-west-2"
}

data "aws_iam_policy" "aws_lambda_basic_execution_role" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy" "ddb" {
  arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

data "aws_iam_policy" "s3" {
  arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}


resource "aws_iam_role" "economic_events_lambda" {
  name               = "economic_events_lambda"
  assume_role_policy = data.aws_iam_policy_document.lamda_exec_assume_role.json

  managed_policy_arns = [
    data.aws_iam_policy.aws_lambda_basic_execution_role.arn,
    data.aws_iam_policy.newrelic_license_key_policy.arn,
    aws_iam_policy.ssm_secrets.arn,
    data.aws_iam_policy.ddb.arn,
    data.aws_iam_policy.s3.arn,
  ]
}
