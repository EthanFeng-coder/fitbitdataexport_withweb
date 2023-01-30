from django.shortcuts import render, redirect
import json.decoder

import pandas as pd
import urllib3
import requests
import urllib.parse
import csv
from django.contrib import messages

import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def home(request):
    if request.method == 'POST':
        userName = request.POST.get('account')
        password = request.POST.get('password')
        headers = {
            'Host': 'api.fitbit.com',
            # 'Content-Length': '397',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://accounts.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://accounts.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        en_userName = urllib.parse.quote(userName)
        en_password = urllib.parse.quote(password)

        data = 'grant_type=password&username=' + en_userName + '&password=' + en_password + '&session-data=%7B%22browser-name%22%3A%22Chrome%22%2C%22browser-version%22%3A%22106.0.5249.62%22%2C%22os-name%22%3A%22Windows%22%2C%22os-version%22%3A%2210%22%2C%22device-model%22%3A%22%22%2C%22device-manufacturer%22%3A%22%22%2C%22device-name%22%3A%22Windows%22%7D&client_id=228TQF&access_token=on&enableRefreshToken=true'
        response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data, verify=False)
        access_token1 = response.json().get('access_token')

        headers = {
            'Host': 'api.fitbit.com',
            # 'Content-Length': '42',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer %s' % (access_token1),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://accounts.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://accounts.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        data = 'grant_type=delegate_token&client_id=228TQD'
        try:
            response = requests.post('https://api.fitbit.com/oauth2/delegate', headers=headers, data=data, verify=False)
            delegate_token = response.json()['result']['delegate_token']
        except KeyError:
            messages.error(request, 'Wrong Account or Passwrod, please try again.')
            return render(request, 'home.html')

        headers = {
            'Host': 'api.fitbit.com',
            # 'Content-Length': '451',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://accounts.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://accounts.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        data = 'token=%s&client_id=228TQF' % (delegate_token)

        response = requests.post('https://api.fitbit.com/oauth2/delegate/token', headers=headers, data=data,
                                 verify=False)
        access_token2 = response.json()['result']['access_token']

        headers = {
            'Host': 'web-api.fitbit.com',
            # 'Content-Length': '110',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer %s' % (access_token2),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://www.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        data = 'periodType=CURRENT_WEEK&dataTypes=ACTIVITIES&dataExportFileFormat=CSV&startDate=2022-10-11&endDate=2022-10-17'

        response = requests.post('https://web-api.fitbit.com/1/user/-/legacy/export/request-export.json',
                                 headers=headers,
                                 data=data, verify=False)
        print(response.json())
        fileIdentifier = response.json()['fileIdentifier']

        headers = {
            'Host': 'web-api.fitbit.com',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer %s' % (access_token2),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://www.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = {
            'fileIdentifier': '%s' % (fileIdentifier),
        }

        response = requests.get('https://web-api.fitbit.com/1/user/-/legacy/export/export-status.json', params=params,
                                headers=headers, verify=False)
        print(response.json())

        headers = {
            'Host': 'web-api.fitbit.com',
            'Sec-Ch-Ua': '"Not;A=Brand";v="99", "Chromium";v="106"',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Ch-Ua-Mobile': '?0',
            'Authorization': 'Bearer %s' % (access_token2),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Origin': 'https://www.fitbit.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.fitbit.com/',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = {
            'fileIdentifier': '%s' % (fileIdentifier),
        }
        try:
            response = requests.get('https://web-api.fitbit.com/1/user/-/legacy/export/get-completed-export.json',
                                    params=params, headers=headers, verify=False, )
            print(response.json())
            exportUrl = response.json()['exportUrl']
            r = requests.get(exportUrl, allow_redirects=True)
            open(userName, 'wb').write(r.content)

        except KeyError:
            print('Retry')
        with open(userName, "r") as f:
            data = f.read().split("\n")
        if data[0] == 'Activities':
            del data[0]
            with open(userName, "w") as f:
                f.write("\n".join(data))
        else:
            pass
        df = pd.read_csv(userName)
        try:
            df.drop('Floors', inplace=True, axis=1)
            df.drop('Minutes Sedentary', inplace=True, axis=1)
            df.drop('Minutes Lightly Active', inplace=True, axis=1)
            df['Zone point'] = df['Minutes Fairly Active'] + df['Minutes Very Active'] * 2
        except KeyError:
            pass
        df.to_csv(userName)
        print(df)
        try:
            with open(userName, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            return render(request, 'display_csv.html', {'data': data})
        except FileNotFoundError:
            messages.error(request, 'Failed to load the csv file, please try again.')
            return render(request, 'home.html')
    return render(request, 'home.html')
