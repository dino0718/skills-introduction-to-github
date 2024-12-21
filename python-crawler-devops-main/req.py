import requests


class APITestManager:
    """負責 API 測試"""
    def run_api_test(self, url):
        headers = {'Accept': 'application/json'}
        response = None

        if "signup" in url:
            payload = {"email": "ntc-test-123@gmail.com", "username": "1111111111", "password": "1111111111"}
            response = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signup', data=payload, headers=headers)
        elif "signin" in url:
            payload = {"email": "ntc-test-123@gmail.com", "password": "1111111111"}
            response = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signin', data=payload, headers=headers)

        return response.text if response else "API 測試失敗"
