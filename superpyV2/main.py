import argparse
from argparse import RawTextHelpFormatter
import csv
from datetime import datetime
from rich import print
import Classes
import Chart
from tabulate import tabulate, TableFormat
#---------------------#
#   GLOBAL VARIABLES  #
#---------------------#

#Files
bought     = "CSV\\bought.csv"
sold       = "CSV\\sold.csv"
pricelist  = "CSV\\pricelist.csv"
timestatus = "timestatus.txt"

# ARGPARSER
parser = argparse.ArgumentParser(description="     _      _       ____    _____   ____    _____      ____   _____   ___   _   _ \n    / \    | |     | __ )  | ____| |  _ \  |_   _|    / ___| | ____| |_ _| | \ | |\n   / _ \   | |     |  _ \  |  _|   | |_) |   | |     | |  _  |  _|    | |  |  \| |\n  / ___ \  | |___  | |_) | | |___  |  _ <    | |     | |_| | | |___   | |  | |\  |\n /_/   \_\ |_____| |____/  |_____| |_| \_\   |_|      \____| |_____| |___| |_| \_|\nSuperPy Software\nVersion 1.0\nJean-Michel Veerman", formatter_class=RawTextHelpFormatter)

# Optional Arguments:
parser.add_argument("-a" , "--add"         , help="Adds a product to the product list, or changes its price, requires [-p product name] [-b buy price] [-s sell price]", action="store_true")      
parser.add_argument("-b" , "--buy_price"   , help="Buy price of a product."                                                   , metavar="", default=0)                                                         
parser.add_argument("-c" , "--command"     , help="Use when you [buy] or [sell] an item"                                      , metavar="", choices=["buy", "sell"])                                            
parser.add_argument("-d" , "--date"        , help="Specify a date for reports"                                                , metavar="", default="today")
parser.add_argument("-e" , "--expiry"      , help="expiry date of product [YYYY-MM-DD]"                                       , metavar="")                                                                     
parser.add_argument("-l" , "--product_list", help="Prints all available products"                                             , action="store_true")                                                            
parser.add_argument("-p" , "--product_name", help="Name of the product"                                                       , metavar="", default="")                                                         
parser.add_argument("-q" , "--quantity"    , help="The amount of products bought/sold"                                        , metavar="", default= 0)                                                         
parser.add_argument("-r" , "--report"      , help="Report [revenue], [profit], [inventory], [chart_total] or [chart_products]", metavar="", choices=["revenue", "profit", "inventory", "chart_total", "chart_products"])                         
parser.add_argument("-s" , "--sell_price"  , help="Sell price of product."                                                    , metavar="", default=0)                                                          
parser.add_argument("-t" , "--advance_time", help="Insert date: [YYYY-MM-DD] to change the softwares date, type [current] to show current time or [update] to update to today.\n'I wish we could travel to the date of next easter'", metavar="", default="")    
args = parser.parse_args()


            
# ARGPARSER HANDLING
# Adds a product to the product list
if args.add == True:
    if args.product_name == "" or args.buy_price == 0 or args.sell_price == 0:
        print("Please Specify full command:  Example: [blue]--add[/blue] [magenta]-p apple[/magenta] [red]-b 2[/red] [green]-s 3[/green]")
    else: 
        try:       
            Classes.ProductManager().update_inventory(pricelist,args.product_name,False,args.buy_price, args.sell_price, 0)
        except KeyError:
            print("Please add [magenta]-p <product_name>[/magenta] and [red]-bp <cost_price>[/red] and -sp [green]<sell_price>[/green]")

# Buys or sells an item, adds item to bought or sold CSV and updates inventory
if args.command == "buy":
    try:
        Classes.ProductManager().bought_sold(bought,args.product_name, args.quantity, args.expiry)
    except:
        print("Please add: [magenta]-p <product name>[/magenta] and [blue]-q <quantity>[/blue] and [purple]-e <expiry>[/purple], Example: -c buy [magenta]-p apple[/magenta] [blue]-q 5[/blue] [purple]-e 2022-10-21[/purple]")        
if args.command == "sell":
    try:
        Classes.ProductManager().bought_sold(sold, args.product_name, args.quantity,"")
    except:
        print("Please add: [magenta]-p <product name>[/magenta] and [blue]-q <quantity>[/blue], Example: -c sell [magenta]-p apple[/magenta] [blue]-q 5[/blue]")  

# Returns list of all available products in product list
if args.product_list:
    with open(pricelist, "r", newline="") as File:
        reader = csv.DictReader(File)
        table = [["Product", "Buy Price", "Sell Price", "stock"]]
        for row in reader:
            table.append([row["product_name"], row["buy_price"], row["sell_price"], row["stock"]])       
    print(tabulate(table, tablefmt='grid')) 

# Check if inserted expiry date is the correct format
if args.expiry:
    Classes.DateHandler.date_validation(args.expiry)
    
# Reports back revenues, profits and inventory or produces charts
match args.report:
    case "revenue" : 
        print(f"The revenue of {args.date} is: [bold green]€ {round(Classes.FileScanner().get_revenue(args.date),2)}[/bold green]")
    case "profit":
        print(f"The profit of {args.date} is: [bold green]€ {round(Classes.FileScanner().get_profit(args.date),2)}[/bold green]")
    case "inventory":    
        if args.product_name == "":
            Classes.FileScanner().get_full_inventory()
        else:
            print(f"You have [bold blue]{Classes.FileScanner().get_stock(args.product_name)}[/bold blue] [magenta]{args.product_name}(s)[/magenta] in stock!") 
    case "chart_total":
        Chart.Chart().create_chart_total()
    case "chart_products":
        Chart.Chart().create_chart_product()        

# Time manipulation
if args.advance_time != "":
    if args.advance_time == "current":
        print(Classes.DateHandler.today())
    elif args.advance_time == "update":
        today = datetime.today()
        date = today.strftime("%Y-%m-%d")
        Classes.DateHandler().manipulate_time(date)    
        Classes.update_stock() 
    else:
        Classes.DateHandler().manipulate_time(args.advance_time)
        Classes.update_stock()
if args.advance_time == "2023-04-09":
    Chart.whatisthis()
        