import csv
from logging import FileHandler
from math import prod
from rich import print
from datetime import datetime, timedelta
import sys
import collections
from tabulate import TableFormat, tabulate
import pandas

#---------------------#
#   GLOBAL VARIABLES  #
#---------------------#

#Files
bought     = "CSV\\bought.csv"
sold       = "CSV\\sold.csv"
pricelist  = "CSV\\pricelist.csv"
timestatus = "timestatus.txt"


# Used data for generating chart.
months = {"jan"  : "2022-01" , 
          "feb"  : "2022-02" , 
          "mar"  : "2022-03" , 
          "apr"  : "2022-04" ,
          "may"  : "2022-05" ,
          "jun"  : "2022-06" ,
          "jul"  : "2022-07" ,
          "aug"  : "2022-08" ,
          "sep"  : "2022-09" ,
          "oct"  : "2022-10" ,
          "nov"  : "2022-11" ,
          "dec"  : "2022-12" } 


#---------------------#
#       CLASSES       #
#---------------------#
class FileScanner():
    
    def __init__(self):
        self.date      = ""                              
        self.key       = ""                       
        self.data      = ""

    # Get specific data from any file  
    def get_data(self, file, colum, search_value="xyz"):
        highest_id  = 0
        revenue     = 0.0
        revenue_product = 0.0
        purchased   = 0.0
        products    = []
        data     = [["ID", "PRODUCT", "STOCK", "EXPIRED"]]

        with open(file, "r") as File:                                                       
            for row in csv.DictReader(File):                                                
                match colum:
                    case "full_inventory": 
                        data.append([row["id"], row["product_name"], row["stock"], row["expired"]])
                    case "highest_id":                          
                        highest_id = row["id"]                                           
                    case "revenue":                                               
                        if self.date in row["sell_date"]:                                   
                            revenue += float(row["sell_price"]) * float(row["quantity"])      
                    case "purchased":                                                  
                        if self.date in row["buy_date"]:                                    
                            purchased += float(row["buy_price"]) * float(row["quantity"])     
                    case "stock":                                               
                        if search_value in row.values():                                     
                            return int(row["stock"])
                    case "product_check":                                               
                        if search_value in row.values():                                     
                            return True                                                
                    case "buy_price":
                        if search_value in row.values():                                     
                            return float(row["buy_price"])
                    case "sell_price":        
                        if search_value in row.values():                                     
                            return float(row["sell_price"])
                    case "id":
                        if search_value in row.values():
                            return int(row["id"])  
                    case "product":
                        products.append(row["product_name"])
                    case "product_sold":
                        if self.date in row["sell_date"]: 
                            if search_value in row["product_name"]:                                    
                                revenue_product += float(row["sell_price"]) * float(row["quantity"])  
                    case "row":
                        if search_value in row["product_name"]:
                            products.append(row)            
                    
       

        match colum:   
            case "highest_id"    : return highest_id                                                                 
            case "revenue"       : return revenue                                              
            case "purchased"     : return purchased   
            case "product"       : return products    
            case "product_sold"  : return revenue_product
            case "row"           : return products
            case "full_inventory": print(tabulate(data, headers='firstrow', tablefmt='grid'))                                                                               

    def get_line(self, product_name):
        return FileScanner.get_data(self,pricelist,"row",product_name)

    def get_expired_products(self, product_name):
        expired_dict = collections.defaultdict(int)

        with open(bought, "r") as File:
            for row in csv.DictReader(File):
                if DateHandler.today() > row["exp_date"]:                  
                    expired_dict[row["product_name"]] += int(row["quantity"])
        return expired_dict[product_name]   


    def get_product_sold(self,product_name, date):
        self.date = date
        return FileScanner.get_data(self, sold, "product_sold", product_name)

    def get_product_list(self):
        return FileScanner.get_data(self, pricelist,"product")

    
    def get_full_inventory(self):                                                           
        FileScanner.get_data(self, pricelist, "full_inventory")                             

    def get_highest_id(self, file):                                                         
        return FileScanner.get_data(self, file, "highest_id")                                       

    def get_revenue(self, date):                                                            
        self.date = DateHandler.date_validation(date)                                       
        return FileScanner.get_data(self, sold, "revenue")                         

    def get_purchased(self, date):                                                          
        self.date = DateHandler.date_validation(date)                                       
        return FileScanner.get_data(self, bought, "purchased")                              

    def get_profit(self, date):                                                             
        self.date = DateHandler.date_validation(date)                                       
        revenue   = FileScanner.get_revenue(self, self.date)                                
        purchased = FileScanner.get_purchased(self, self.date)                              
        profit    = (revenue - purchased)                                                   
        return profit                                                                       

    def get_stock(self, product_name):                                                      
        return FileScanner.get_data(self, pricelist, "stock", product_name)      

    def get_product(self, product_name):               
        return FileScanner.get_data(self,pricelist,"product_check", product_name)

    def get_product_id(self, product_name):
        return FileScanner.get_data(self, pricelist, "id", product_name)    

    def get_price(self, buy_sell, product_name):
        return FileScanner.get_data(self, pricelist, buy_sell, product_name)




class DateHandler():                                                                         
    def __init__(self):                                                                      
        pass                                                                                 

    def today():                                     
        with open('timestatus.txt', "r") as File:
            today = File.read()
            File.close()
            return today

    # Checks if today or yesterday is used, ifnot see if it matches
    def date_validation(date):
        full_date = ""
        today = DateHandler.today()
        match date:
            case "today"     : 
                return today
            case "yesterday" : 
                change_date = datetime.strptime(today, '%Y-%m-%d')
                sub_date = change_date - timedelta(days=1)
                return datetime.strftime(sub_date, "%Y-%m-%d")
            case _: 
                full_date = date         
        try:
            datetime.strptime(full_date, "%Y-%m-%d")
            return full_date
        except ValueError: 
            pass
        try:
            datetime.strptime(full_date, "%Y-%m")
            return full_date
        except ValueError:
            pass
        try:
            datetime.strptime(full_date, "%Y")
            return full_date
        except ValueError:
            print("Incorrect time format, use YYYY or YYYY-MM or YYYY-MM-DD")
            sys.exit()

    # Reads or writes in timestatus.txt
    def manipulate_time(self, new_date):
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            with open(timestatus, "w") as File:
                if DateHandler.date_validation(new_date):
                    File.write(new_date)    
                    print(f"Changed the date to: [blue]{new_date}[/blue].")  
        except ValueError:
            print("Incorrect time format, use YYYY-MM-DD")
            sys.exit() 

        



class ProductManager():
    def __init__(self):
        pass

    # Function that can update the pricelist and inventory and tracks stock.    
    def update_inventory(self, file, product_name, buy_sell, new_buy_price, new_sell_price, quantity):
        product_exists     = FileScanner.get_product(self,product_name)
        product_id         = FileScanner.get_product_id(self,product_name) 
        current_stock      = FileScanner.get_stock(self,product_name)
        buy_price          = new_buy_price
        sell_price         = new_sell_price
        expired_products   = FileScanner.get_expired_products(self,product_name)
        if new_buy_price  == ""  or new_sell_price == "":
            buy_price      = FileScanner.get_price(self,"buy_price", product_name)
            sell_price     = FileScanner.get_price(self,"sell_price", product_name)
        new_stock = 0
        #If product is already in catalog start overwriting.   
        if product_exists == True:
            if buy_sell == "buy":
                new_stock = int(current_stock) + int(quantity)
            if buy_sell == "sell":
                new_stock = int(current_stock) - int(quantity) - int(expired_products)
                # Checks if there is enough stock
                if new_stock < 0:
                    print(f"Not enough {product_name} in stock! Please buy them first!")
                    raise ValueError
            product_list = []
            # Finds current line and replaces the stock value
            with open(pricelist, "r") as File:
                product = csv.reader(File)
                product_list.extend(product)
                for row in product_list:
                    if product_name in row:
                        line_to_override = {product_id:[product_id, product_name, buy_price, sell_price, new_stock, expired_products]}     
                        with open(file, "w", newline="") as File:
                            writer = csv.writer(File)
                            for line, row in enumerate(product_list):
                                data = line_to_override.get(line, row)
                                writer.writerow(data)  
                if file == pricelist:
                    print(f"Changed data from [bold magenta]{product_name}[/bold magenta] Buy Price:[bold red]€{buy_price}[/bold red], Sell price: [bold green]€{sell_price}[/bold green], Stock: {new_stock}") 
        # If product does not exist then add it to the list
        else:
            # Append to list if product doesn't exist yet.
            new_id = int(FileScanner.get_highest_id(self,pricelist)) + 1 
            with open(pricelist, "a", newline="") as File:
                writer = csv.writer(File)    
                writer.writerow([new_id, product_name,new_buy_price, new_sell_price, quantity,0])
                print(f"New product added: [bold magenta]{product_name}[/bold magenta] for Buy Price:[bold red]€{new_buy_price}[/bold red], Sell Price: €[bold green]{new_sell_price}[/bold green], Quantity: {quantity}")






    # Function that handles bought or sold items.
    def bought_sold(self, file, product_name, quantity, expiry):
        today      = DateHandler.today()
        sales_id   = int(FileScanner.get_highest_id(self,file)) + 1 
        buy_price  = FileScanner.get_price(self,"buy_price", product_name)
        sell_price = FileScanner.get_price(self,"sell_price", product_name)
        current_stock  = int(FileScanner.get_stock(self,product_name))
        expired_products   = int(FileScanner.get_expired_products(self,product_name))
        total_stock = current_stock - expired_products
        if total_stock >= int(quantity) or file == bought:
            convert_buy_sell = ""
            if buy_price and sell_price != 0:  
                with open(file, "a", newline="") as File:
                    writer = csv.writer(File)
                    if file == bought:
                        convert_buy_sell = "buy"
                        writer.writerow([sales_id, product_name, today, buy_price, quantity,expiry])
                        print(f"[bold green]Bought[/bold green] [bold blue]{quantity}[/bold blue] [bold magenta]{product_name}(s)[/bold magenta]!")
                    if file == sold:
                        convert_buy_sell = "sell"
                        writer.writerow([sales_id, product_name, today, sell_price, quantity])
                        print(f"[bold red]Sold[/bold red] [bold blue]{quantity}[/bold blue] [bold magenta]{product_name}(s)[/bold magenta]!")
                ProductManager.update_inventory(self,pricelist,product_name,convert_buy_sell,"","",quantity)
            else:
                print(f"Product [bold magenta]{product_name}[/bold magenta] not found yet! Can't be bought or sold. Please use the --add command first!")
        else:
           print(f"Not enough {product_name} in stock! Please buy them first!") 





def update_stock():
    products = FileScanner().get_product_list()
    expiry = []
    for i in products:
        expired = FileScanner().get_expired_products(i)
        expiry.append(expired)

    product_list = []
    new_list = []
    with open(pricelist, "r") as File:
        product = csv.reader(File)
        product_list.extend(product)
        x = 0
        
        for row in product_list[1:]:
            row[5] = expiry[x]
            x = x + 1
            new_list.append(row)

        with open(pricelist, "w", newline="") as File:
            writer = csv.writer(File)
            header = ['id','product_name','buy_price','sell_price','stock','expired']
            writer.writerow(header)
            for i in new_list:
                writer.writerow(i)



















