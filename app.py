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

def select_bin():
    global b
    l_names=b["Bin Names"] # Get Bin Names from data files
    l_totals=b["Bin Totals"] # Get Bin Totals from data files
    while (True): # loop until user selects a valid bin
        print()
        for x in range(len(l_names)): # print all bin names
            print(f"{l_names[x]}: ${l_totals[x]}")
        i = input(f"Select Bin (1-{len(l_names)} or name): ").lower() # prompt user to input number from 1 to len(bin) or bin name
        if i == "quit": # pass cancel ticket request up
            return -2
        bin = -1 # default to bin -1 (doesnt exist)
        for x in range(len(l_names)): # check each bin against input
            if (i == l_names[x].lower()): # check if input matches bin name
                bin = x
                break
            else: 
                try: # try to check if input matches bin index
                    if (int(i) == x+1):
                        bin = x
                        break
                except ValueError:
                    continue
            
        if bin == -1: # if bin was not detected try again
            print(f"Could not find bin '{i}'")
            continue
        break # if bin selected break
    print(f"{l_names[bin]} Bin Selected") # show user selected bin
    return bin


def deposit(args, modifiers): # Create a deposit Ticket and append it
    print(args)
    print(modifiers)
    global b
    global h
    global v
    l_totals = []
    if (len(args) > 0): # if 1 argument was passed assume value for total
        total = float(args[0])
    else: # otherwise get input for total
        i = input("total: ").lower() # Get Total from User
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return
        total=float(i)
    if (len(args) > 1): # if more arguments were passed assume value for mults
        if (len(modifiers) > 0): # if any -'char' modifiers were passed
            if (modifiers[0] == "-d"): # if -d was passed switch from percents to dollars
                for x in range(1,len(args)): # update l_totals
                    l_totals.append(float(args[x]))
            else: # if no -d modifier assume percentages
                for x in range(1,len(args)):
                    l_totals.append(total*float(args[x])/100) # update l_totals
        else:  # if no modifier assume percentages
            for x in range(1,len(args)):
                l_totals.append(total*float(args[x])/100) # update l_totals

    while (True): # Loop until ticket looks good and break
        l_names=b["Bin Names"] # Get Bin Names from data files
        if (len(l_totals) == 0) :
            mults = v["Deposit"]["Multipliers"] # Get multipliers from data files
            for x in range(len(mults)): # Apply multipliers
                l_totals.append(total*mults[x])
        t=Ticket("Deposit",total,l_names,l_totals) # Create Ticket
        preview = t.output()
        print("\nPreview:\n"+preview) # Preview
        i = input("If preview is good 'enter', else 'any key'").lower() # Ask user if Ticket looks good
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return

        elif i == "": # Append Ticket
            b,h,v=t.append(b,h,v)
            print("Ticket Appended")
            save.write([b,h,v])
            return

        else: # Change Ticket
            i = input("Change total (1) or percentages (2): ").lower()
            print()
            if i == "quit": # cancel ticket
                print("Ticket Canceled")
                return

            elif (i == "1") or (i == "total"): # User wishes to change total
                i = input("total: ").lower() # Get New Total from User
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
                            i = input(f"\n{l_names[x]} (%) ({100-mults_total*100}%) : ").lower()
                        else:
                            i = input(f"\n{l_names[x]} (%) : ").lower() # Ask user to change percentage x
                        if i == "quit": # cancel ticket
                            print("Ticket Canceled")
                            return
                        percent=float(i)
                        l_percents.append(percent/100) # add multiplier to list
                        mults_total+=l_percents[x] # check to see if mults add up to 1
                        print(f"{l_names[x]}: {percent}% = ${total*l_percents[x]}") # Display Total for bin x

                    if (mults_total != 1): # check to see if mults add up to 1
                        print("Percentages do not add up to 100%, please try again\n")       
                        continue # ask user for new percentages

                    i = input("Do you wish to save these new percentages (y/n)? ").lower()
                    if i == "quit": # cancel ticket
                        print("Ticket Canceled")
                        return
                    elif (i == "y") or (i == "yes"): # save percentages to file
                        v["Deposit"]["Multipliers"] = l_percents
                    mults=l_percents # save percentages to variable
                    break # succeessfully got through so break loop


def purchase(): # Create a purchase ticket and append it
    global b
    global h
    global v
    i = input("total: ").lower() # Get Total from User
    if i == "quit": # cancel ticket
        print("Ticket Canceled")
        return
    total=float(i)
    l_names=b["Bin Names"] # Get Bin Names from data files
    bin = select_bin() # run function to get bin from user
    if (bin == -2): # user chose to quit
        print("Ticket Canceled")
        return

    while (True): # Loop until ticket looks good and break
        l_totals=[0]*len(l_names) # create list with len(total bins) size
        l_totals[bin]=-total # assign total to correct bin
        t=Ticket("Purchase",-total,l_names,l_totals) # Create Ticket
        preview = t.output()
        print("\nPreview:\n"+preview) # Preview
        i = input("If preview is good 'enter', else 'any key'").lower() # Ask user if Ticket looks good
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return

        elif i == "": # Append Ticket
            b,h,v=t.append(b,h,v)
            print("Ticket Appended")
            save.write([b,h,v])
            return

        else: # Change Ticket
            i = input("Change total (1) or bin (2): ").lower()
            print()
            if i == "quit": # cancel ticket
                print("Ticket Canceled")
                return

            elif (i == "1") or (i == "total"): # User wishes to change total
                i = input("total: ").lower() # Get New Total from User
                if i == "quit": # cancel ticket
                    print("Ticket Canceled")
                    return
                total=float(i)

            elif (i == "2") or (i == "bin"): # User wishes to change bin
                bin = select_bin() # run function to get bin from user
                if (bin == -2): # user chose to quit
                    print("Ticket Canceled")
                    return
                

def loop():
    global b
    global h
    global v
    condition = True
    while (condition):
        i = input(">").lower()
        i = i.split(" ") # change i to list of arguments
        if i[0] == "quit":
            condition = False
            break
        if i[0] == "deposit": # wish to deposit
            if len(i) == 1: # if input is simply "deposit"
                deposit([],[])
            else: # if input is "deposit x y z"
                args=[]
                modifiers=[]
                for x in range(1,len(i)): # get args and -'char' modifiers
                    if i[x][0] == "-":
                        modifiers.append(i[x])
                    else:
                        args.append(i[x])
                deposit(args,modifiers) 
        if i[0] == "purchase":
            purchase()


if __name__ == "__main__":
    init()
    print(b)
    print(h)
    print(v)
    loop()
    