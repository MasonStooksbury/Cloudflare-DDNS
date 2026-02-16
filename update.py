#!/usr/bin/python3

from pprint import pprint
import datetime
import requests
import json


def isTokenValid(env):
    headers = {
        'Authorization': f'Bearer {env['CF_TOKEN']}'
    }
    url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
    r = requests.get(url, headers=headers)
    r = r.json()['result']
    return r['status'] == 'active'



def getEnvironmentVariables():
    data = ''
    env = {}

    with open('.env', 'r') as f:
        data = f.read().splitlines()

    # Split the key/value up, but make sure to preserve any values that may have '=' in them
    for variable in data:
        variable = variable.replace('"', '')
        pieces = variable.split('=')
        key = pieces[0]
        value = '='.join(pieces[1:])

        env[key] = value
    
    return env



def getLastKnownIpAddress():
    data = ''
    with open('last_known_ip_address.txt', 'r') as f:
        data = f.read().splitlines()
    
    return data[0]



def getZoneId(env, headers):
    print('Getting Zone ID...')
    r = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    r = r.json()['result']

    for zone in r:
        if zone['name'] == env['CF_TARGET_DOMAIN']:
            print('Successfully got Zone ID!')
            return zone['id']
    sendMessage(env, '[FAILURE] - Could not get Zone ID for some reason')



def getDnsRecordId(env, headers):
    print('Getting DNS Record ID...')
    r = requests.get(f'https://api.cloudflare.com/client/v4/zones/{env["CF_ZONE_ID"]}/dns_records', headers=headers)
    r = r.json()['result']

    for record in r:
        if env['CF_TARGET_DOMAIN'] in record['name']:
            print('Successfully got DNS Record ID!')
            return record['id']
    sendMessage(env, '[FAILURE] - Could not get DNS Record ID for some reason')



def updateCloudflare(env, current_ip_address):
    print('Updating Cloudflare...')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {env['CF_TOKEN']}'
    }

    zone_id = getZoneId(env, headers)
    dns_record_id = getDnsRecordId(env, headers)
    
    body = {"name": f"*.{env['CF_TARGET_DOMAIN']}",
          "ttl": 1,
          "type": "A",
          "comment": "Domain verification record",
          "content": current_ip_address,
          "proxied": False}

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}'
    
    r = requests.put(url, json=body, headers=headers)

    if r.status_code == 200:
        setCurrentIpAddress(current_ip_address)
        sendMessage('[SUCCESS] - Public IP successfully pushed to Cloudflare DNS record')
    else:
        sendMessage('[FAILURE] - Was not able to update Cloudflare DNS record')



def getCurrentIpAddress(env):
    print('Getting current IP address...')
    r = requests.get('https://icanhazip.com')
    if r.status_code == 200:
        print('Successfully got current IP address!')
        return r.text.strip()
    sendMessage(env, '[FAILURE] - Could not get public IP address')



def setCurrentIpAddress(new_ip_address):
    with open('last_known_ip_address.txt', 'w') as f:
        f.write(new_ip_address)



def sendMessage(env, message):
    if 'WEBHOOK_URL' in env and env['WEBHOOK_URL'] != '':
        data = {
            "content": message
        }

        headers = {
            "Content-Type": "application/json"
        }

        requests.post(env['WEBHOOK_URL'], data=json.dumps(data), headers=headers)
    else:
        with open('logs.log', 'a') as f:
            f.write(f'{datetime.datetime.now()} ~~~ {message}\n')










env = getEnvironmentVariables()

if not isTokenValid(env):
    sendMessage(env, '[FAILURE] - Token is invalid')
else:
    last_known_ip_address = getLastKnownIpAddress()
    current_ip_address = getCurrentIpAddress()

    if last_known_ip_address != current_ip_address:
        updateCloudflare(env, current_ip_address)