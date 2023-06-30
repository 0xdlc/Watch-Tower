import subprocess
import json
from pymongo import MongoClient
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import os

#MONGO DB CONNECTION----------------------------#
cluster = MongoClient("mongodb+srv://mohamadkhzd:a4LlRT5zdAW8th1u@subs0.zegtlek.mongodb.net/?retryWrites=true&w=majority")
db = cluster["datas"]
collection = db["programs"]
def discord(title, description):

    webhook = DiscordWebhook(
        url="https://discord.com/api/webhooks/1103661510162653305/Z5GQvXU4VqcCilQTFyBGEbZzp52gxL-XSme1cQF-ACrrlz-3v_z17tMJlF55aWfZSz0X",
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

def sub_only(program):
    assets = collection.distinct("assets", {"program": f"{program}"})
    scopedir = os.path.expanduser('~/scopes')
    print("[+] Finding The Imposter..")
    for i in assets:
        reg = r"\*.+\.[^\s]+"
        if re.search(reg,i) != None:
            s = i.split('*.')[1]
            filedir = f"{scopedir}/{program}/{s}.subfinder.new"
            print(s)
            subprocess.call(["subfinder","-silent","-d",s,"-o",filedir])
            subprocess.call(["sort","-o",filedir,filedir])
            new = subprocess.check_output(["comm","-23",filedir,f"{scopedir}/{program}/{s}.subfinder"],text=True)
            if len(new) > 1:
                ChangeTitle = f"[+] New Asset"
                description = f'**Program: **{program}\n**Assets: **{str(new)}'
                discord(title=ChangeTitle ,description=description)
                f = open(f"{scopedir}/{program}/{s}.subfinder", "a")
                f.write(new)
                f.close()
                #first see if you get the same amount of subs , then do the dif for httpx resualts
                subprocess.run(["sort","-o",f"{scopedir}/{program}/{s}.subfinder",f"{scopedir}/{program}/{s}.subfinder"])
            subprocess.run(["rm",filedir])
            
def FindDif(program,sub):  

    if sub:
        sub_only(program)
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


def insert_Program(program,opt):
    print(f"[+] Adding {program} to your WatchScope...")
    #----------------------------#
    process = subprocess.check_output(["./utils/find_index.sh",program], text=True)
    temp = process
    temp = temp.split(',')
    index = int(temp[0])
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
    if opt == True:
        scopedir = os.path.expanduser('~/scopes')
        print("[+] Adding subdomins to the database..")
        subprocess.run(["mkdir",f"{scopedir}/{program}"])
        assets = collection.distinct("assets", {"program": f"{program}"})
        for i in assets:
            reg = r"\*.+\.[^\s]+"
            if re.search(reg,i) != None:
                s = i.split('*.')[1]
                print(s)
                subprocess.run(["subfinder","-silent","-d",s,"-o",f"{scopedir}/{program}/{s}.subfinder"])
                subprocess.run(["nice_httpx",f"{scopedir}/{program}/{s}.subfinder",f"{scopedir}/{program}/{s}.httpx"])



