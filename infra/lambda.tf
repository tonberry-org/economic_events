resource "aws_lambda_function" "economic_events" {
  function_name    = "economic_events"
  role             = aws_iam_role.economic_events_lambda.arn
  filename         = "../dist/economic_events.zip"
  source_code_hash = filebase64sha256("../dist/economic_events.zip")
  handler          = "economic_events.lambda_function.lambda_handler"
  runtime          = "python3.9"
  publish          = true
  timeout          = 60

  environment {
    variables = {
      API_EOD : data.aws_ssm_parameter.eod_api_key.value
      DDB_ECONOMIC_EVENTS : aws_dynamodb_table.economic_events.name
    }
  }
}
