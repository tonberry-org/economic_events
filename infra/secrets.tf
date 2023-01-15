data "aws_ssm_parameter" "eod_api_key" {
  name = "/eod/api_key"
}

data "aws_ssm_parameter" "newrelic_account_id" {
  name = "/newrelic/account_id"
}
