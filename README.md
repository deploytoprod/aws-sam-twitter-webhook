# Twitter Webhook Serverless API

This SAM template generates the necessary API for both:

1. Replying the CRC challenge made daily by Twitter.
2. Posting your latest tweet into a JSON file in a public S3 bucket.

The only manual step you need to do is to create a secure parameter in AWS SSM Parameter Store, which by default should be called `twitter.api.secret`. The reason why I am not creating the parameter as part of the SAM template is because AWS CloudFormation doesn't support creating a `SecureString` parameter type, which is what we are using for obvious reasons.

This Stack Overflow answer by coderina has the step-by-step instructions on what you should do to work on the Twitter part: https://stackoverflow.com/questions/57953470/what-is-the-procedure-of-registering-the-webhook-for-twitter/71907679#71907679