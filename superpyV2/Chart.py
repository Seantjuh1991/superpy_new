import Classes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate, TableFormat

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



class Chart():

    def __init__(self):
        pass
     
    def create_chart_total(self):
        data_rev = []
        data_prof = []
        numbers = Classes.FileScanner()
        for number in months.values():
            data_rev.append(round(numbers.get_revenue(number),2))
            data_prof.append(round(numbers.get_profit(number),2))

        labels = months.keys()

        x = np.arange(len(labels))  
        width = 0.35  
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, data_rev, width, label='revenue', color="orange")
        rects2 = ax.bar(x + width/2, data_prof, width, label='profit', color="green")
        
        # view data terminal
        header = ["","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        line1 = ["Revenue"] + data_rev
        line2 = ["Profit"] + data_prof
        dft = [header, line1, line2]
        print(tabulate(dft, tablefmt='grid')) 

        ax.set_title('Revenue and profit by month')
        ax.set_xticks(x, labels)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        fig.tight_layout()
        plt.show()    






    def create_chart_product(self):
        product_list = Classes.FileScanner().get_product_list()
        num_of_products = len(product_list)

        # First create the Products as columns.
        header = ["month"] 
        products = ["Products"]
        for i in product_list:
                products.append(i)
                header.append(i)

        # Create the groups that will show on the chart and add name Labels.
        jan = ["jan"]
        feb = ["feb"]
        mar = ["mar"]
        apr = ["apr"]
        may = ["may"]
        jun = ["jun"]
        jul = ["jul"]
        aug = ["aug"]
        sep = ["sep"]
        oct = ["oct"]
        nov = ["nov"]
        dec = ["dec"]

        # Adds all the products sales per month to the array, if num of products increase, it will still fill the array!
        for i in range(num_of_products):
                jan.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-01"))
                feb.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-02"))
                mar.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-03"))
                apr.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-04")) 
                may.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-05"))
                jun.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-06"))
                jul.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-07"))
                aug.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-08"))
                sep.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-09"))
                oct.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-10"))
                nov.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-11")) 
                dec.append(Classes.FileScanner().get_product_sold(product_list[i],"2022-12"))        

        # create dataframe from arrays
        df = pd.DataFrame([jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec],
                        columns=products)
        # view data terminal
        dft = [header, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        print(tabulate(dft, headers='firstrow', tablefmt='grid')) 
        
        # plot grouped bar chart
        df.plot(x='Products',
                kind='bar',
                stacked=True,
                title='Overview revenue per product per month')
                
        plt.show()    



def whatisthis():
    img = mpimg.imread('other\\whatisthis.png')
    imgplot = plt.imshow(img)
    plt.show()


