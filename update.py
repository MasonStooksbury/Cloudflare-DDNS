#!/usr/bin/python3

from pprint import pprint
import requests


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


def getDnsRecordId(env, headers):
    print('Getting DNS Record ID...')
    r = requests.get(f'https://api.cloudflare.com/client/v4/zones/{env["CF_ZONE_ID"]}/dns_records', headers=headers)
    r = r.json()['result']

    for record in r:
        if env['CF_TARGET_DOMAIN'] in record['name']:
            print('Successfully got DNS Record ID!')
            return record['id']




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
    return r.status_code


def getCurrentIpAddress():
    return requests.get('https://icanhazip.com').text.strip()

def setCurrentIpAddress(new_ip_address):
    with open('last_known_ip_address.txt', 'w') as f:
        f.write(new_ip_address)


def sendMessage():
    pass









env = getEnvironmentVariables()
if not isTokenValid(env):
    print('Token is invalid, not progressing further')
    exit()


last_known_ip_address = getLastKnownIpAddress()
current_ip_address = getCurrentIpAddress()

if last_known_ip_address != current_ip_address:
    pass_or_nah = updateCloudflare(env, current_ip_address)

    if pass_or_nah == 200:
        setCurrentIpAddress(current_ip_address)
        sendMessage('succeed')
    else:
        sendMessage('failed')