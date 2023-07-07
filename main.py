import os, requests, time
Token = "Your token"

header = {"authorization": Token,"Content-Type": "application/json"}
payload = {"max_age": 0, "max_uses": 0, "temporary": False, "flags": 0}

print("""
██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗
██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝
██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝ 
██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║     
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     


""")

def front_logs(link):
    if link == 1:
        print(f"Invitation denided")
    else:
        print(f"Invitation link  : discord.gg/{link}")

def writing_server(link,name,auth):
    if auth:
        with open("Backup_server.txt", "a") as file:
            file.write(f"discord.gg/{link} :\t {name} \n")
            file.close()
    else:
        with open("Backup_server.txt", "a") as file:
            file.write(f"Permission denided :\t {name} \n")
            file.close()

def get_invitation_link(server_id,server_name):
    guild_channel = requests.get(f"https://ptb.discord.com/api/v9/guilds/{server_id}/channels", headers=header).json()
    for channel in guild_channel:
        # print(channel)
        if channel['type'] == 0:
            try:
                requests_temp = requests.post(f"https://ptb.discord.com/api/v9/channels/{channel['id']}/invites", headers=header, json=payload).json()
                invitation_link = requests_temp['code']
                # print("code inv : ",invitation_link)
                if invitation_link == 50013:
                    pass
                elif invitation_link == 50183:
                    time.sleep(10)
                else:
                    time.sleep(5)
                    return invitation_link, server_name, True
                
            except:
                # print("error")
                time.sleep(2)
                pass
    return 1, server_name, False

                                                  
def Backup_guilds():
    print("\t SERVER\n")
    r = requests.get("https://canary.discord.com/api/v10/users/@me/guilds", headers=header).json()
    for json_data in r:
        print(f"Server name      : {json_data['name']}")
        print(f"Server ID        : {json_data['id']}")
        if "VANITY_URL" in json_data["features"]:
            r_vanity = requests.get(f"https://canary.discord.com/api/v10/guilds/{json_data['id']}", headers=header).json()
            if not r_vanity['vanity_url_code'] == None:
                print(f"Server Vanity    : {r_vanity['vanity_url_code']}")
                writing_server(r_vanity['vanity_url_code'],json_data['name'],True)
            else: 
                link,name,auth = get_invitation_link(json_data['id'],json_data['name'])
                front_logs(link)
                writing_server(link,name,auth)
        else:
            link,name,auth = get_invitation_link(json_data['id'],json_data['name'])
            front_logs(link)
            writing_server(link,name,auth)
        print("\n")
    
def Backup_relationship():
    print("\t RELATIONSHIPS")
    file = open("Backup_friend.txt","a") 
    file.write("FRIEND :\n\n")
    print("\n")
    blocked_user = []
    requested_user = []
    r = requests.get("https://canary.discord.com/api/v10/users/@me/relationships", headers=header).json()
    for user in r:
        if user['type'] == 2:
            blocked_user.append(user)
        elif user['type'] == 4:
            requested_user.append(user)
        else:
            print(f"""
User ID  : {user['id']} 
Nickname : {user['nickname']} 
Username : {user['user']['username']}#{user['user']['discriminator']}\n
                  """)
            
            file.write(f"User ID  : {user['id']} \t Nickname : {user['nickname']} \t Username : {user['user']['username']}#{user['user']['discriminator']} \n")

    file.write("\nREQUESTED USERS :\n\n")
    for user in requested_user:
        print(f"""
User ID  : {user['id']} 
Nickname : {user['nickname']} 
Username : {user['user']['username']}#{user['user']['discriminator']}\n
        """)
        file.write(f"User ID  : {user['id']} \t Nickname : {user['nickname']} \t Username : {user['user']['username']}#{user['user']['discriminator']} \n")


    file.write("\nBLOCKED USERS :\n\n")
    for user in blocked_user:
        print(f"""
User ID  : {user['id']} 
Nickname : {user['nickname']} 
Username : {user['user']['username']}#{user['user']['discriminator']}\n
        """)
        file.write(f"User ID  : {user['id']} \t Nickname : {user['nickname']} \t Username : {user['user']['username']}#{user['user']['discriminator']} \n")

Backup_guilds()
Backup_relationship()


