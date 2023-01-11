
resource "aws_dynamodb_table" "economic_events" {
  name         = "economic_events"
  hash_key     = "id"
  range_key    = "date"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Name = "Economic Events"
  }
}
