resource "aws_lambda_function" "pricehistory" {
  function_name    = "pricehistory"
  role             = aws_iam_role.pricehistory_lambda.arn
  filename         = "../dist/pricehistory.zip"
  source_code_hash = filebase64sha256("../dist/pricehistory.zip")
  handler          = "pricehistory.lambda_function.lambda_handler"
  runtime          = "python3.9"
  publish          = true
  timeout          = 60

  environment {
    variables = {
      CODE : data.aws_ssm_parameter.code.value
      CLIENT_ID : data.aws_ssm_parameter.client_id.value
    }
  }
}
