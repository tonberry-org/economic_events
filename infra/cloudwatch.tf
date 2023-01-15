resource "aws_cloudwatch_event_rule" "economic_events" {
  name                = "economic_events"
  schedule_expression = "cron(0 10 * * ? *)"
}


resource "aws_cloudwatch_event_target" "invoke_economic_events_lambda" {
  rule      = aws_cloudwatch_event_rule.economic_events.name
  target_id = "economic_events_lambda"

  input = <<DOC
{
}
DOC
  arn   = aws_lambda_function.economic_events.arn
}


resource "aws_lambda_permission" "event_economic_events" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.economic_events.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.economic_events.arn
}

resource "aws_cloudwatch_log_group" "economic_events" {
  name              = "/aws/lambda/${aws_lambda_function.economic_events.function_name}"
  retention_in_days = 7
}
