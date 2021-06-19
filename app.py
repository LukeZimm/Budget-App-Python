import save
from objects import *

b={}
h={}
v={}

def init():
    print("Loading data...")
    global b
    global h
    global v
    b,h,v=save.load()
    print("Loaded")

def deposit(): # Create a deposit Ticket and append it
    global b
    global h
    global v
    i = input("total: ") # Get Total from User
    if i == "quit": # cancel ticket
        print("Ticket Canceled")
        return
    total=float(i)
    l_names=b["Bin Names"] # Get Bin Names from data files
    mults = v["Deposit"]["Multipliers"] # Get multipliers from data files
    while (True): # Loop until ticket looks good and break
        l_totals=[]
        for x in range(len(mults)): # Apply multipliers
            l_totals.append(total*mults[x])
        t=Ticket("Deposit",total,l_names,l_totals) # Create Ticket
        preview = t.output()
        print("\nPreview:\n"+preview) # Preview
        i = input("If preview is good 'enter', else 'any key'") # Ask user if Ticket looks good
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return
        elif i == "": # Append Ticket
            b,h,v=t.append(b,h,v)
            print("Ticket Appended")
            save.write([b,h,v])
            return
        else: # Change Ticket
            i = input("Change total (1) or percentages (2): ")
            print()
            if i == "quit": # cancel ticket
                print("Ticket Canceled")
                return
            elif (i == "1") or (i == "total"): # User wishes to change total
                i = input("total: ") # Get New Total from User
                if i == "quit": # cancel ticket
                    print("Ticket Canceled")
                    return
                total=float(i)
            elif (i == "2") or (i == "percentages"): # User wishes to change percentages
                while (True): # Loop until user gets percentages totaling up to 100%
                    for x in range(len(l_names)): # Print current percentages
                        print(f"{l_names[x]}: {mults[x]*100}%")
                    l_percents = [] # create new percentage list
                    mults_total = 0 
                    for x in range(len(l_names)): # User Inputs new percentages
                        if (x == len(l_names)-1): # if last bin, tell user required percent to total 100%
                            i = input(f"\n{l_names[x]} (%) ({100-mults_total*100}%) : ")
                        else:
                            i = input(f"\n{l_names[x]} (%) : ") # Ask user to change percentage x
                        if i == "quit": # cancel ticket
                            print("Ticket Canceled")
                            return
                        percent=float(i)
                        l_percents.append(percent/100) # add multiplier to list
                        mults_total+=l_percents[x] # check to see if mults add up to 1
                        print(f"{l_names[x]}: {percent}% = ${total*l_percents[x]}") # Display Total for bin x
                    if (mults_total != 1):
                        print("Percentages do not add up to 100%, please try again\n")       
                        continue         
                    i = input("Do you wish to save these new percentages (y/n)? ")
                    if i == "quit": # cancel ticket
                        print("Ticket Canceled")
                        return
                    elif (i == "y") or (i == "yes"):
                        v["Deposit"]["Multipliers"] = l_percents
                    mults=l_percents
                    break

            

def purchase(): # Create a purchase ticket and append it
    global b
    global h
    global v
    i = input("total: ") # Get Total from User
    total=float(i)
    l_names=b["Bin Names"] # Get Bin Names from data files
    for x in range(len(l_names)):
        pass

def loop():
    global d
    global h
    condition = True
    while (condition):
        i = input(">")
        if i == "quit":
            condition = False
            break
        if i == "deposit":
            deposit()
        if i == "purchase":
            purchase()


if __name__ == "__main__":
    init()
    print(b)
    print(h)
    print(v)
    loop()
    