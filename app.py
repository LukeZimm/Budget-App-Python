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

def select_bin(text="Select Bin"):
    global b
    l_names=b["Bin Names"] # Get Bin Names from data files
    l_totals=b["Bin Totals"] # Get Bin Totals from data files
    while (True): # loop until user selects a valid bin
        print()
        for x in range(len(l_names)): # print all bin names
            print(f"{l_names[x]}: ${l_totals[x]}")
        i = input(f"{text} (1-{len(l_names)} or name): ").lower() # prompt user to input number from 1 to len(bin) or bin name
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
    global b
    global h
    global v
    l_totals = []
    # Get Total
    if (len(args) > 0): # if 1 argument was passed assume value for total
        total = float(args[0])
    else: # otherwise get input for total
        i = input("total: ").lower() # Get Total from User
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return
        total=float(i)

    # Get Mults
    if (len(args) > 1): # if more arguments were passed assume value for mults
        if (len(modifiers) > 0): # if any -'char' modifiers were passed
            if (modifiers[0] == "-d"): # if -d was passed switch from percents to dollars
                sum=0
                for x in range(1,len(args)): # update l_totals
                    l_totals.append(float(args[x]))
                    sum+=float(args[x])
                if (sum > total): # check if args sum to total
                    print("Bin Totals did not sum up to total")
                    return
            else: # if no -d modifier assume percentages
                sum=0
                for x in range(1,len(args)):
                    l_totals.append(total*float(args[x])/100) # update l_totals
                    sum+=float(args[x])
                if (sum > 1): # check if args sum to total
                    print("Bin percentages did not sum up to 100%")
                    return
        else:  # if no modifier assume percentages
            sum=0
            for x in range(1,len(args)):
                l_totals.append(total*float(args[x])/100) # update l_totals
                sum+=float(args[x])/100
            if (sum > 1): # check if args sum to total
                print("Bin percentages did not sum up to 100%")
                return
    l_mults = v["Deposit"]["Multipliers"]
    if (len(args) < 1+len(l_mults)): # if user did not provide all bin prep next function for assuming the rest
        sum=0
        mults_total=0
        for x in range(len(l_totals)): # get current total
            sum+=l_totals[x]
            mults_total+=l_mults[x]
        remaining = total-sum
    mults = v["Deposit"]["Multipliers"] # Get multipliers from data files

    while (True): # Loop until ticket looks good and break
        l_names=b["Bin Names"] # Get Bin Names from data files
        if (len(l_totals) < len(mults)) :
            for x in range(len(l_totals),len(mults)): # Apply multipliers
                l_totals.append((total-sum)*(mults[x]/(1-mults_total)))
        t=Ticket("Deposit",total,l_names,l_totals) # Create Ticket
        preview = t.output()
        print("\nPreview:\n"+preview) # Preview
        i = input("If preview is good 'enter', else 'any key': ").lower() # Ask user if Ticket looks good
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
                l_totals=[]
                mults_total=0
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
                    l_totals=[]
                    mults_total=0
                    break # succeessfully got through so break loop

def purchase(args, modifiers): # Create a purchase ticket and append it
    global b
    global h
    global v
    # get total
    if (len(args) > 0): # if 1 argument was passed assume value for total
        total = float(args[0])
    else: # otherwise get input for total
        i = input("total: ").lower() # Get Total from User
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return
        total=float(i)
    
    # get bin selection
    l_names=b["Bin Names"] # Get Bin Names from data files
    if (len(args) > 1): # if more arguments were passed assume bin selection
        bin=int(args[1])-1
    else:
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
        i = input("If preview is good 'enter', else 'any key': ").lower() # Ask user if Ticket looks good
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
                
def transfer(args):
    global b
    global h
    global v
    # get source and deposit bin
    bin_source = -1
    bin_deposit = -1
    bins=b["Bin Totals"]
    if (len(args) == 0): # input required from user
        bin_source = select_bin(text="Select Source Bin")
        bin_deposit = select_bin(text="Select Deposit Bin")
    elif (len(args) == 1): # interpret args to get source bin and get deposit bin from user
        bin_source = int(args[0])-1
        bin_deposit = select_bin(text="Select Deposit Bin")
    elif (len(args) > 1): # interpret args to get source and deposit bin
        bin_source = int(args[0])-1
        bin_deposit = int(args[1])-1

    # get amount
    if (len(args) < 3): # input required from user
        i = input("Total: ")
        if i == "quit": # cancel ticket
            print("Ticket Canceled")
            return
        else: total = float(i)
    else: # interpret args to get total
        total = float(args[2])

    while (True): # loop until user is satisfied and break
        # Display Transfer
        print("\nSource bin: "+b["Bin Names"][bin_source]+" $"+str(bins[bin_source]))
        print("Deposit bin: "+b["Bin Names"][bin_deposit]+" $"+str(bins[bin_deposit]))
        print(f"Total: ${total}")
        l_totals=[0]*len(bins)
        for x in range(len(bins)): # create l_totals 
            if x == bin_source: l_totals[x]=-total
            elif x == bin_deposit: l_totals[x]=total
        t=Ticket("Transfer",0,b["Bin Names"],l_totals)
        print(t.output())
        i = input("Enter to confirm, any key to change: ")
        if (i == "quit"): # cancel ticket
            print("Ticket Canceled")
            return
        elif (i == ""): # append ticket
            t.append(b, h, v)
            print("Ticket Appended")
            save.write([b,h,v])
            break
        else: # user wishes to change ticket
            i = input("Change total (1) or bins (2): ").lower()
            print()
            if i == "quit": # cancel ticket
                print("Ticket Canceled")
                return

            elif (i == "1") or (i == "total"): # User wishes to change total
                i = input("total: ").lower() # Get New Total from User
                if i == "quit": # cancel ticket
                    print("Ticket Canceled")
                    return
                l_totals=[]
                total=float(i)

            elif (i == "2") or (i == "bins"): # User wishes to change percentages
                bin_source = select_bin(text="Select Source Bin")
                bin_deposit = select_bin(text="Select Deposit Bin")

def view():
    global b
    global h
    global v
    bin_names = b["Bin Names"] # Get bin names
    bin_totals = b["Bin Totals"] # Get bin totals
    total = b["Total"] # Get total
    print(f"Total: ${total}") # print total
    for x in range(len(b["Bin Names"])): # print bin totals
        print(f"{bin_names[x]}: ${bin_totals[x]}")
    print() # line break


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

        elif i[0] == "deposit": # wish to deposit
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

        elif i[0] == "purchase":
            if len(i) == 1: # if input is simply "purchase"
                purchase([],[])
            else: # if input is "purchase x y z"
                args=[]
                modifiers=[]
                for x in range(1,len(i)): # get args and -'char' modifiers
                    if i[x][0] == "-":
                        modifiers.append(i[x])
                    else:
                        args.append(i[x])
                purchase(args,modifiers) 

        elif (i[0] == "view") or (i[0] == "totals") or (i[0] == "bins"):
            view()
        
        elif (i[0] == "transfer"):
            if len(i) == 1: # if input is simply "transfer"
                transfer([])
            else: # if input is "transfer x y z"
                args=[]
                for x in range(1,len(i)):
                    args.append(i[x])
                transfer(args)

if __name__ == "__main__":
    init()
    print(b)
    print(h)
    print(v)
    loop()
    