#!/bin/bash
source .env

# Verify token is legit:
echo $CF_TOKEN
echo $WEBHOOK_URL

# response=$(curl -H "Authorization: Bearer $CF_TOKEN" "https://api.cloudflare.com/client/v4/user/tokens/verify")

SUCCESS_BODY='{"username": "test_username", "content": "hello"}'

curl -H "Content-Type: application/json" -d $SUCCESS_BODY --url $WEBHOOK_URL
