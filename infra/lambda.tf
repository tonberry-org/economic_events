resource "aws_lambda_function" "economic_events" {
  function_name    = "economic_events"
  role             = aws_iam_role.economic_events_lambda.arn
  filename         = "../dist/economic_events.zip"
  source_code_hash = filebase64sha256("../dist/economic_events.zip")
  handler          = "newrelic_lambda_wrapper.handler"
  runtime          = "python3.9"
  publish          = true
  timeout          = 60

  environment {
    variables = {
      API_EOD : data.aws_ssm_parameter.eod_api_key.value
      DDB_ECONOMIC_EVENTS : aws_dynamodb_table.economic_events.name
      # For the instrumentation handler to invoke your real handler, we need this value
      NEW_RELIC_LAMBDA_HANDLER = "economic_events.lambda_function.lambda_handler"
      NEW_RELIC_ACCOUNT_ID     = data.aws_ssm_parameter.newrelic_account_id.value
      # Enable NR Lambda extension if the telemetry data are ingested via lambda extension
      NEW_RELIC_LAMBDA_EXTENSION_ENABLED = true
      # Enable Distributed tracing for in-depth monitoring of transactions in lambda (Optional)
      NEW_RELIC_DISTRIBUTED_TRACING_ENABLED = true
    }
  }
  layers = ["arn:aws:lambda:us-west-2:451483290750:layer:NewRelicPython39:36"]
}


data "aws_lambda_function" "new_relic" {
  function_name = "newrelic-log-ingestion"
}
resource "aws_cloudwatch_log_subscription_filter" "economic_events" {
  name            = "logdna-logfilter"
  log_group_name  = aws_cloudwatch_log_group.economic_events.name
  filter_pattern  = ""
  destination_arn = data.aws_lambda_function.new_relic.arn
}
