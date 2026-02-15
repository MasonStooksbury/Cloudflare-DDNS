# Cloudflare-DDNS
Simple bash script to update my public IP when it changes

## Installation
Download the script and put it wherever you want

## Usage
- Create a [Cloudflare API Token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
    - Make sure to select `Edit Zone DNS` and choose your specific domain
- Rename `.env.sample` to `.env`
- Update variables with your info
- Optionally, you can add a webhook to 


## Notes
If you decide to use Discord for your webhook messages, you can use [Discohook](https://discohook.app/?data=eyJ2ZXJzaW9uIjoiZDIiLCJtZXNzYWdlcyI6W3siX2lkIjoiWk9sZTE0ZjdrcCIsImRhdGEiOnsiY29udGVudCI6IlRlc3QiLCJlbWJlZHMiOm51bGwsImF0dGFjaG1lbnRzIjpbXX19XX0) to easily format them (the URL is huge because it the webhook just URL-encodes your message)