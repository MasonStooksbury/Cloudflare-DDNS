# Cloudflare-DDNS
Simple Python script to update my public IP when it changes. Automatically figures out the Zone and DNS Record IDs, and optionally messages a Discord webhook if you provide one (if you don't, it will write to `logs.log`)

<br>

## Installation
Download the script and put it wherever you want

## Usage
- Create a [Cloudflare API Token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
    - Make sure to select `Edit Zone DNS` and choose your specific domain
- Rename `.env.sample` to `.env`
- Update variables with your info
- Optionally, you can add a Discord webhook to send success and failure messages
- Finally, set this up via CRON or your favorite scheduling tool (setting it to run every 3 hours is a good, but every 12-24 should be enough)

## .env Variable Descriptions:
- `CF_TOKEN` - This is your Cloudflare API Token. It is used to discover your Zone ID, DNS Record ID, update the DNS record, and validate itself
- `CF_TARGET_DOMAIN` - This is the domain that you want to update. The script assumes you have a single, wildcard A record aimed at your home server (though you can modify this if you want). This is used to get your Zone ID, DNS Record ID, and update the DNS record
- `WEBHOOK_URL` - This is the Discord webhook URL. If you don't want to use this, simply remove the line entirely or set to "". If this is not set, it will log to `logs.log` in whatever directory the script is ran from

## Notes
Don't worry, the IP in `last_known_ip_address.txt` is not my IP address. I could make the script a bit more robust and create this if it doesn't exist, but I figured it was just easier to add a file in here now and not have/need that logic in the first place