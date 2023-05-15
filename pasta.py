import json
import random

json_file = open('data\\pastas.json')
pastas = json.load(json_file)
json_file.close()

json_file = open('data\\facts.json')
facts = json.load(json_file)
json_file.close()

def num_pastas():
    return len(pastas['pastas'])

def get_fact():
    return facts['facts'][random.randint(0, len(facts['facts'])-1)]['fact']
    
def get_pasta():
    return pastas['pastas'][random.randint(0, len(pastas['pastas'])-1)]