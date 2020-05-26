from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from Store import *

s=Store()
c=Coupon(Coupon.PERCENTAGE,4,1,"new year")
ross=s.cus_list.find_cus(12)
ross.add_coupon(c)

window=Tk()
window.title("Store Data")
window.geometry("1300x1250")
txt1=Entry(window,width=15)
txt1.grid(column=1,row=0)
txt1.focus()
txt2=Entry(window,width=15)
txt2.grid(column=1,row=1)
txt2.focus()
def clicked1():
    sale=False
    lst=txt1.get()
    lst1=lst.split()
    if len(lst1)==2:
        sale=s.make_sale(int(lst1[0]),lst1[1])
    if sale == False or len(lst1)!=2:
        text="fail to make this sale"
    else:
        text=sale
    messagebox.showinfo("SALE",text)
def clicked2():
    lst=txt2.get()
    lst1=lst.split()
    if len(lst1)==2:
        phones=s.find_phone_by_size(int(lst1[0]),int(lst1[1]))
        if len(phones.productList) == 0:
            text = "Empty"
        else:
            text = phones
    else:
        text="please insert two values with space before you click"
    messagebox.showinfo("here are the relevant phones",text)
def clicked3():
    count=0
    if var.get()==1:
        count +=s.count_product(Phone)
    if var.get()==2:
        count +=s.count_product(Refrigerator)
    if var.get()==3:
        count +=s.count_product(Refrigerator)
        count +=s.count_product(Phone)
    if var.get()!=1 and var.get()!=2 and var.get()!=3:
        count="please selecf a product that you want to count"
    messagebox.showinfo("total of",count)
def clicked4():
    countProfit=s.profit()
    if s.profit()==0:
        countProfit="0"
    messagebox.showinfo("total sale to",countProfit)
makeSale=Button(window,text="make sale",command=clicked1)
makeSale.grid(column=3,row=0)
findPhone=Button(window,text="find phone by size",command=clicked2)
findPhone.grid(column=3,row=1)
count=Button(window,text="count number of products",command=clicked3)
count.grid(column=3,row=2)
totalProfit=Button(window,text="get total",command=clicked4)
totalProfit.grid(column=3,row=3)
# phoneValue=BooleanVar()
# phoneValue.set(False)
var=IntVar()
phonesC=Radiobutton(window,text="phones",value=1,variable=var)
phonesC.grid(column=0,row=2)
# refrigeratorValue=BooleanVar()
# refrigeratorValue.set(False)
refrigeratorC=Radiobutton(window,text="refrigerator",value=2,variable=var)
refrigeratorC.grid(column=1,row=2)
# allValue=BooleanVar()
# allValue.set(False)
all=Radiobutton(window,text="all",value=3,variable=var)
all.grid(column=2,row=2)
window.mainloop()


