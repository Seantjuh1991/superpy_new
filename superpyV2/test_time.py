timestatus = "timestatus.txt"

class DateHandler():                                                                         
    def __init__(self):                                                                      
        pass      

    def today():                                     
        with open(timestatus, "r") as File:
            today = File.read()
            print(type(today))
            print(f"Vandaag is het {today}")
            return today

print(DateHandler.today())        