import pyad
from pyad import aduser
import os

ldapuri = 'ldap:///dc%3Dunicph%2Cdc%3Ddomain'


def list_users():
    # Connect to AD using the default credentials
    pyad.set_defaults(ldap_server="dc3.unicph.domain")
    
    try:
        # List all users in the default Users container
        users = aduser.ADUser().get_all()
        
        # Display user information
        for user in users:
            print(f"Username: {user.get_username()}")
            print(f"Full Name: {user.get_attribute('displayName')}")
            print(f"Email: {user.get_attribute('mail')}")
            print("-----")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_users()

