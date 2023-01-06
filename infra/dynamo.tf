
resource "aws_dynamodb_table" "market_schedule" {
  name           = "price_history_quotes"
  hash_key       = "symbol"
  range_key      = "timestamp"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "symbol"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Name = "Market Scheduler"
  }
}
