import simplejson as json

def load():
    l=[0,0,0]
    with open("data/balances.json","r") as f:
        l[0] = json.load(f)
    with open("data/history.json","r") as f:
        l[1] = json.load(f)
    with open("data/variables.json","r") as f:
        l[2] = json.load(f)
    return l

def write(l): # L = [balances,history]
    with open("data/balances.json","w") as f:
        json.dump(l[0],f, indent=4)
    with open("data/history.json","w") as f:
        json.dump(l[1],f, indent=4)
    with open("data/variables.json","w") as f:
        json.dump(l[2],f, indent=4)

if __name__ == "__main__":
    d=load()