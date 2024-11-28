# bluesky_autofollow.py

from atproto import Client
import os
import sys
from dotenv import load_dotenv
from colorama import Fore, Style

def get_all_followers(client, actor):
    followers = []
    cursor = None
    print(f"{Fore.YELLOW}Fetching followers...{Style.RESET_ALL}")
    while True:
        response = client.get_followers(actor=actor, cursor=cursor)
        followers.extend(response['followers'])
        cursor = response['cursor'] if 'cursor' in response else None
        if not cursor:
            break
    return followers

def get_all_following(client, actor):
    following = []
    cursor = None
    print(f"{Fore.YELLOW}Fetching following...{Style.RESET_ALL}")
    while True:
        response = client.get_follows(actor=actor, cursor=cursor)
        following.extend(response['follows'])
        cursor = response['cursor'] if 'cursor' in response else None
        if not cursor:
            break
    return following

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read username and password from environment variables
    username = os.getenv('BLUESKY_USERNAME')
    password = os.getenv('BLUESKY_PASSWORD')

    if not username or not password:
        print(f"{Fore.RED}Please set your BLUESKY_USERNAME and BLUESKY_PASSWORD in your .env file.{Style.RESET_ALL}")
        sys.exit(1)

    client = Client()

    try:
        print(f"{Fore.YELLOW}Logging in to BlueSky...{Style.RESET_ALL}")
        client.login(username, password)
        print(f"{Fore.GREEN}Successfully logged in to BlueSky.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to log in: {e}{Style.RESET_ALL}")
        sys.exit(1)

    try:
        # Get the user's handle and DID
        user_handle = client.me['handle']
        user_did = client.me['did']

        # Get the list of followers
        followers = get_all_followers(client, user_did)
        follower_dids = set(follower['did'] for follower in followers)

        # Get the list of following
        following = get_all_following(client, user_did)
        following_dids = set(follow['did'] for follow in following)

        # Identify users to follow back
        to_follow_back = follower_dids - following_dids
        followed_back_count = len(to_follow_back)

        print(f"{Fore.GREEN}Found {followed_back_count} new followers to follow back.{Style.RESET_ALL}")

        # Follow back the users
        for did in to_follow_back:
            print(f"{Fore.YELLOW}Following {did}...{Style.RESET_ALL}")
            client.follow(did)
            print(f"{Fore.GREEN}Followed {did}{Style.RESET_ALL}")

        print(f"{Fore.GREEN}All new followers have been followed back. 🎉 Followed back {followed_back_count} users! 👏{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
