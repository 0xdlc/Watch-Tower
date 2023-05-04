import argparse
from utils.loader import FindDif
from utils.loader import insert_Program
import os
import os.path
import pymongo
from pymongo import MongoClient
import json
def main():
    # CONNECT TO MONGO CLUSTER
    cluster = MongoClient("mongodb+srv://mohamadkhzd:a4LlRT5zdAW8th1u@subs0.zegtlek.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["datas"]
    collection = db["programs"]
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', required=True, default=False, metavar='url', type=str)
    args = parser.parse_args()
    programs = args.p.split(',')
    print("[+] selected programs are:" + str(programs))
    for i in programs:
       query = {"program": f"{i}"}
       if collection.find_one(query) != None:
             #print(collection.distinct("platform", {"program": f"{i}"})[0])
             print(f'[+] program {i} found in the database')
             FindDif(i)
       else:
             insert_Program(i)
if __name__ == '__main__':
    main()