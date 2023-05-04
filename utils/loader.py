import subprocess
import json
from pymongo import MongoClient
from discord_webhook import DiscordWebhook, DiscordEmbed


#MONGO DB CONNECTION----------------------------#
cluster = MongoClient("mongodb url")
db = cluster[""]
collection = db[""]
def discord(title, description):

    webhook = DiscordWebhook(
        url="discord webhook url",
        rate_limit_retry=True)
    embed = DiscordEmbed(
        title=title,
        description=description,
        color='65535')
    webhook.add_embed(embed)
    response = webhook.execute()


def bugcrowd_assets(program,index):
    platform_file = open('platforms/bugcrowd.json')
    js = json.load(platform_file)
    data = js[index]['target_groups']
    if js[index]['name'] == program:
         assets = []
         for i in data:
            for j in i['targets']:
                assets.append(j['name'])
         return assets
    else:
        print('Δ Index number is incorrect, Fixing...')
        process = subprocess.check_output(["./utils/find_index.sh",program],text=True)
        temp = process.split(',')
        index = int(temp[0])
        platform = str(temp[1])
        if platform == 'bugcrowd':
            collection.update_one({ "program":program },{ "$set": { "index": index}})
            print('[+]Reloading the function ...')
            return bugcrowd_assets(program,index)  
        else:
            h1_assets(program,index)


def h1_assets(program,index):
    platform_file = open('platforms/hackerone.json')
    js = json.load(platform_file)
    data = js[index]['relationships']['structured_scopes']['data']
    if js[index]['attributes']['name'] == program:
         assets = []
         for i in data:
            if i['attributes']['eligible_for_submission'] == True:
                assets.append(i['attributes']['asset_identifier'])
         return assets         
    else:
         print('[Δ] Index number is not correct, Fixing...')
         process = subprocess.check_output(["./utils/find_index.sh",program],text=True)
         temp = process.split(',')
         index = int(temp[0])
         platform = str(temp[1])
         if platform == 'hackerone':            
            collection.update_one({ "index":index })
            print('[+]Reloading the function ...')
            return h1_assets(program,index)
         else:
             bugcrowd_assets(program,index)


def FindDif(program):
    

    # print(Name)        
    #-------------------------------# 
    platform = collection.distinct("platform", {"program": f"{program}"})[0]
    index = collection.distinct("index", {"program": f"{program}"})[0]
    assets = collection.distinct("assets", {"program": f"{program}"})

    #----V Updating resource file V--------$
    print ("[+] Updating the source file...")
    subprocess.call(["./utils/update.sh",platform])

    #--------V updates the database V---------------#
    def update(assets):
        collection.update_one({ "program": program },{ "$push": { "assets": assets} })

    #---------V Finds the the diffrences in assets V----------------#
    def Diffrentiate(new_assets,assets):
        for i in new_assets:
            count =0
            for j in assets:
                count+=1
                if str(i) == str(j):   
                    break
                elif count==len(assets) :
                    # YOU CAN ADD YOUR DISCORD WEBHOOL HERE:
                    update(str(i))
                    print("Ψ Found a new target Ψ :"+ str(i))
                    ChangeTitle = f"[+] New Target"
                    description = f'**Program: **{program}\n**Platform: **{platform}\n**Target: **{str(i)}'
                    discord(title=ChangeTitle ,description=description)
    #-----------------------------------------------------#

    print(f"[Ξ]Looking for a new target in {program}...")
    match platform:
        case 'hackerone':
            new_assets = h1_assets(program,index)
            Diffrentiate(new_assets,assets)
        case 'bugcrowd':
            new_assets = bugcrowd_assets(program,index)
            Diffrentiate(new_assets,assets) 


        # case 'intigriti':
        #     continue
        # 
        #     continue
        # case 'yeswehack':
        #     continue



def insert_Program(program):
    print(f"[+] Adding {program} to your WatchScope...")
    #----------------------------#
    process = subprocess.check_output(["./utils/find_index.sh",program], text=True)
    temp = process
    temp = temp.split(',')
    index = int(temp[0])
    print(index)
    platform = str(temp[1])
    if platform == 'hackerone':
        assets = h1_assets(program,index)
        collection.insert_one({"program":f"{program}","index":index,"platform":f"{platform}","assets":assets})
        print('Done.')
    elif platform == 'bugcrowd':
        with open('platforms/bugcrowd.json') as file:
            file1 = file.read()
        js = json.loads(file1)    
        data = js[index]['target_groups']
        assets = [] 
        for i in data:
            for j in i['targets']:
                assets.append(j['name'])
        collection.insert_one({"program":f"{program}","index":index,"platform":f"{platform}","assets":assets})
        print('Done.')
    elif platform == 'yeswehack':
        with open('platforms/yeswehack.json') as file:
            file1 = file.read()
        js = json.loads(file1)    
        data = js[index]['scopes']
        assets = [] 
        for i in data:
            assets.append(i['scope'])
        collection.insert_one({"program":f"{program}","index":index,"platform":f"{platform}","assets":assets})
        print('Done.')
    elif platform == 'intigriti':
        with open('platforms/intigriti.json') as file:
            file1 = file.read()
        js = json.loads(file1)
        data = js[index]['domains']
        assets = []
        for i in data:
            assets.append(i['endpoint'])
        collection.insert_one({"program":f"{program}","index":index,"platform":f"{platform}","assets":assets})
        print('Done.')        
