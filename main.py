import requests
import json
import sys

banner = """
    
      ▄████  ██▓▄▄▄█████▓ ███▄ ▄███▓ ▄▄▄       ██▓ ██▓    
     ██▒ ▀█▒▓██▒▓  ██▒ ▓▒▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    
    ▒██░▄▄▄░▒██▒▒ ▓██░ ▒░▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    
    ░▓█  ██▓░██░░ ▓██▓ ░ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    
    ░▒▓███▀▒░██░  ▒██▒ ░ ▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒
     ░▒   ▒ ░▓    ▒ ░░   ░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░
      ░   ░  ▒ ░    ░    ░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░
    ░ ░   ░  ▒ ░  ░      ░      ░     ░   ▒    ▒ ░  ░ ░   
          ░  ░                  ░         ░  ░ ░      ░  ░
   
                                                    @daley
"""

print(banner)

def main():
    if len(sys.argv) == 1:
        print(" Usage: {} [username]".format(sys.argv[0]))
        print(" Usage: {} 0days\n".format(sys.argv[0]))
        sys.exit(0)

    username = sys.argv[1]

    initial = requests.get('https://api.github.com/users/' + username)
    json_initial = json.loads(initial.content)

    userid = json_initial['id']
    name = json_initial['name']
    location = json_initial['location']

    print(" Username: " + username)
    print(" User ID: " + str(userid))
    print(" Name: " + name)
    print(" Location: " + location)

    if json_initial['email'] is None:
        print(" Email: Hidden")
        print("\n Checking commits for email since it's hidden... \n")

        request2 = requests.get('https://api.github.com/users/' + username + '/events')
        json_two = json.loads(request2.content)

        VALID_EMAILS = []

        for event in json_two:
            event_id = event['id']
            if "payload" in event:
                if "commits" in event['payload']:
                    commits = event['payload']['commits']
                    for commit in commits:
                        email = commit['author']['email']
                        if email not in VALID_EMAILS:
                            VALID_EMAILS.append(email)
                
        print(' [+] Email found: ' + VALID_EMAILS + '\n')
    else:
        print(" Email: " + json_initial['email'])

if __name__ == "__main__":
    main()
