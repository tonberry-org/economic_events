data "aws_ssm_parameter" "code" {
  name = "/tda/code"
}

data "aws_ssm_parameter" "client_id" {
  name = "/tda/client_id"
}
