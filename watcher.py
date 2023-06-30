import argparse
from utils.loader import FindDif
from utils.loader import insert_Program
from utils.loader import sub_only
from pymongo import MongoClient
def main():
    # CONNECT TO MONGO db
    cluster = MongoClient("mongodb+srv://mohamadkhzd:a4LlRT5zdAW8th1u@subs0.zegtlek.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["datas"]
    collection = db["programs"]
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', required=True, default=False, metavar='programs to watch', type=str)
    parser.add_argument('-scope',required=False,nargs='?', const='true', metavar='Watch for new scope', type=bool)
    parser.add_argument('-sub',required=False,nargs='?', const='true', metavar='Watch for new subdomains', type=bool)
    args = parser.parse_args()
    sub = False
    cidr = False
    programs = args.p.split(',')
    print("[+] selected programs are:" + str(programs))
    for i in programs:
       query = {"program": f"{i}"}
       if collection.find_one(query) != None:
             if args.get:
                  print(f"getting assets of {i}")
                  for j in collection.distinct("assets", {"program": f"{i}"}):
                       print(j)
             if args.sub:
                  sub_only(i)          
             if args.scope:
                  print(f'[+] program {i} found in the database')
                  FindDif(i)                       
       else:
             insert_Program(i,args.sub)
if __name__ == '__main__':
    main()