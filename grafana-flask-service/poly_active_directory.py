from helpers import Helpers
import requests


class PolyActiveDirectory():
    def __init__(self):
        self._helpers = Helpers()
        self.env = self._helpers.get_env_path()
        self.access_token = self.get_token()

    def get_token(self):
        payload = 'grant_type='+self.env["AZURE_GRANT_TYPE"]\
            + '&client_id='+self.env["AZURE_CLIENT_ID"] \
            + '&client_secret='+self.env["AZURE_CLIENT_SECRET"]\
            + '&scope='+self.env["AZURE_AUTH_SCOPE"]
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request(
            "POST", self.env["AZURE_AUTH_TOKEN_API"],
            headers=headers, data=payload
        ).json()

        return response.get("access_token")

    def get_users(self):
        try:
            ad_users = []
            headers = {
                "Authorization": "Bearer {}".format(self.access_token)
            }
            response = requests.get(
                self.env["AZURE_USERS_API"]+"?$select=mail,companyName",
                headers=headers
            ).json()
            for user in response.get("value"):
                email = user.get("mail")
                userCompanyRole = user.get("companyName")
                if (
                    email is not None
                    and email != "null"
                    and len(email) > 0
                    and userCompanyRole != None
                    and str(userCompanyRole).lower() == 'user'
                ):
                    ad_users.append(email)

            return ad_users
        except Exception as e:
            print(e)

    def get_valid_user_organization(self, email, organization):
        try:
            url = self.env["AZURE_USERS_API"]\
                + "?$filter=userPrincipalName eq '" \
                + email \
                + "'  or mail eq '" \
                + email \
                + "' &$select=companyName"
            headers = {
                "Authorization": "Bearer {}".format(self.access_token)
            }
            response = requests.get(url, headers=headers).json()
            for user in response.get("value"):
                if str(user.get("companyName")) in organization \
                        or str(user.get("companyName")).casefold() == 'admin':
                    return user.get("companyName")
            return None

        except Exception as e:
            print("Error while validating the user\n", e)

    def validate_poly_user(self, email):
        try:
            url = self.env["AZURE_USERS_API"]\
                + "?$filter=userPrincipalName eq '" \
                + email \
                + "'  or mail eq '" \
                + email \
                + "' &$select=companyName"

            headers = {
                "Authorization": "Bearer {}".format(self.access_token)
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                poly_user_azure_data = response.json().get("value")
                if poly_user_azure_data is not None and len(poly_user_azure_data) > 0:
                    for user in response.json().get("value"):
                        return str(user.get("companyName")).casefold()

            return None
        except Exception as e:
            print("Error while validating the user\n", e)
