import datetime

class Ticket:
    t_type = ""
    total = 0
    l_names=[]
    l_totals=[]
    date = None
    def __init__(self,t_type,total,l_names,l_totals):
        self.t_type = t_type
        self.total = total
        self.l_names = l_names
        self.l_totals = l_totals
        self.date = datetime.datetime.now()

    def output(self):
        #time = f"{self.date.month}/{self.date.day}/{self.date.year} {self.date.hour}:{self.date.minute}"
        time = self.date.strftime("%m/%d/%Y %H:%M:%S")
        bins = ""
        for x in range(len(self.l_names)):
            bins+=f" {self.l_names[x]}: ${self.l_totals[x]}"
        return(f"{time} | {self.t_type}: ${self.total} {bins}")

    def append(self,b,h,v):
        b["Total"]+=self.total # Update Total
        for x in range(len(v["Deposit"]["Multipliers"])): # Update Bins
            b["Bin Totals"][x]+=self.l_totals[x]
        ticket_number = h["Total"] # Get Ticket Number
        h["Total"] = ticket_number+1 # Update Total Tickets
        h[str(ticket_number)] = [self.t_type,self.date.strftime("%d/%m/%Y %H:%M:%S"),self.total,self.l_totals] # Add Ticket to History file
        return b,h,v

    #def 