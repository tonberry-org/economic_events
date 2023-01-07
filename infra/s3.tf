resource "aws_s3_bucket" "economic_events" {
  bucket = "tonberry-economic-events"
}

resource "aws_s3_bucket_acl" "economic_events" {
  bucket = aws_s3_bucket.economic_events.id
  acl    = "private"
}
