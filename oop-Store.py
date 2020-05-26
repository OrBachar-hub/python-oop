##Or Bachar 205972805
import csv
from datetime import date
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

class Customer:
    def __init__(self,lst):
        if lst[5]!="F" and lst[5]!="M" and lst[5]!="male":
            lst[5]="F"
        self.ID=lst[0]
        self.FirstName=lst[1]
        self.LastName=lst[2]
        self.Address=lst[3]
        self.PhoneNumber=lst[4]
        self.Gender=(lst[5])
        self.couponSet=set()
    def print(self):
        print(self.ID,self.FirstName,self.LastName,self.Address,self.PhoneNumber,self.Gender)
    def __str__(self):
        return self.FirstName+', '+self.LastName+', '+self.Address+', '+self.PhoneNumber+', '+self.Gender+'.'
    def add_coupon(self,coupon):
        self.couponSet.add(coupon)

class CustomerList:
    def __init__(self,file):
        if file=="empty":
            lst=[]
        else:
            with open(file,newline='') as csvfile:
                read=csv.reader(csvfile)
                lst=[]
                next(read)
                for i in read:
                    c=Customer(i)
                    lst.append(c)
        self.ListOfCustomers=lst
    def __str__(self):
        back=""
        for i in self.ListOfCustomers:
            back +=i.FirstName+" "+i.LastName
        return back
    def AddCustomer(self,other):
        if self.find_cus(other.ID)==False:
            self.ListOfCustomers.append(other)
        return False
    def deleteCustomer(self,ID):
        for i in self.ListOfCustomers:
            if i.ID==ID:
                self.ListOfCustomers.remove(i)
    def printByLastName(self,lastName):
        for i in self.ListOfCustomers:
            if i.LastName==lastName:
                print(i)
    def find_cus(self,id):
        for i in self.ListOfCustomers:
            if int(i.ID)==id:
                return i
        return False

class Product:
    def __init__(self,ID,Name,inventory,Price,Manufacturer):
        self.ID=ID
        self.Name=Name
        self.inventory=inventory
        self.Price=Price
        self.Manufacturer=Manufacturer
    def __str__(self):
        return self.Name + ",inventory=" + str(self.inventory) + ",price=" + str(self.Price) + ",id=" + str(self.ID)
    def updateAfterSell(self):
        self.inventory=int(self.inventory) - 1
    def load_list(self,line):
        self.ID=line[0]
        self.Name=line[1]
        self.inventory=line[2]
        self.Price=line[3]
        self.Manufacturer=line[4]

class Sales:
    def __init__(self,customer_id,prod_id,price,date):
        self.customer_id=customer_id
        self.prod_id=prod_id
        self.price=price
        self.date=date
    def __str__(self):
        return self.customer_id+" "+self.prod_id+" "+str(self.price)+" "+str(self.date)

class Coupon:
    SIMPLE_DIS=0
    PERCENTAGE=1
    def __init__(self,type,discount,pr_id,name,date="1/1/2020"):
        self.type=type
        self.discount=discount
        self.pr_id=pr_id
        self.name=name
        self.date=date
    def __eq__(self, other):
        return isinstance(other, Coupon) and self.name == other.name
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return str(self.type)+" "+str(self.discount)+" "+str(self.pr_id)+" "+str(self.name)+" "+str(self.date)

class Product_list:
    def __init__(self):
        self.productList=[]
    def findProduct(self,productName):
        for i in self.productList:
            if i.Name==productName:
                return i
        return False
    def add_prod(self,product):
        if int(product.inventory)<=0 or self.findProduct(product.Name)!=False:
                return False
        else:
            self.productList.append(product)
            return True
    def load_from_file(self,file,object):
        with open(file,newline="") as csvfile:
            read=csv.reader(csvfile)
            next(read)
            for i in read:
                p=object()
                p.load_list(i)
                self.add_prod(p)
    def make_sale_p(self,name):
        p=self.findProduct(name)
        if p!=False:
            p.updateAfterSell()
            if p.inventory==0:
                self.RemoveFromList(p)
            return True
    def __str__(self):
        back=""
        for i in self.productList:
                back +=i.__str__()+"\n"
        return back
    def RemoveFromList(self,p):
        self.productList.remove(p)

class Store:
    def __init__(self, cus_file_name="custmer.csv",phone_file="phone.csv",ref_file="refrigerator.csv"):
        self.cus_list=CustomerList(cus_file_name)
        self.ProductsList=Product_list()
        if phone_file!="empty":
            self.ProductsList.load_from_file(phone_file,Phone)
        if ref_file!="empty":
            self.ProductsList.load_from_file(ref_file,Refrigerator)
        self.sales=[]
    def make_sale(self,cus_id,prod_name):
        if self.cus_list.find_cus(cus_id)==False or self.ProductsList.findProduct(prod_name)==False:
            return False
        p = self.ProductsList.findProduct(prod_name)
        c=self.cus_list.find_cus(cus_id)
        lst=[float(p.Price)]
        for coupon in c.couponSet:
            if int(coupon.pr_id)==int(p.ID):
                if coupon.type==0:
                    price=float(p.Price) - float(coupon.discount)
                    lst.append(float(price))
                else:
                    price=float(p.Price)*((100-float(coupon.discount))/100)
                    lst.append(float(price))
        price=min(lst)
        if price<0:
            price=0
        s=Sales(c.ID,p.ID,price,date.today())
        p.updateAfterSell()
        if p.inventory==0:
            if self.ProductsList.findProduct(prod_name)!=False:
                self.ProductsList.RemoveFromList(p)
        self.sales.append(s)
        return s
    def get_all_sales(self):
        list=[]
        for i in self.sales:
            list.append(i)
        return list
    def find_phone_by_size(self,min,max):
        list=Product_list()
        for phone in self.ProductsList.productList:
            if isinstance(phone,Phone):
                if phone.screen_size<=max and phone.screen_size>=min:
                    list.add_prod(phone)
        return list
    def profit(self):
        num=0
        for sale in self.sales:
            num +=float(sale.price)
        return num
    def count_product(self,object):
        num=0
        for product in self.ProductsList.productList:
            if isinstance(product,object):
                num +=int(product.inventory)
        return num


class Refrigerator(Product):
    def __init__(self,number_of_doors=2,size=500,id=1,name="",inventory=10,price=100,manufacturer=""):
        super().__init__(id,name,inventory,price,manufacturer)
        self.number_of_doors=int(number_of_doors)
        self.size=int(size)
    def __str__(self):
        return "Refrigerator: of size "+str(self.size)+"   "+",inventory= "+str(self.inventory)+",price= "+str(self.Price)+",id= "+str(self.ID)
    def __eq__(self, other):
        return isinstance(other,Refrigerator) and self.Name==other.Name
    def __hash__(self):
        return hash(self.Name)
    def load_list(self,line):
        self.ID=line[0]
        self.Name=line[1]
        self.inventory=line[2]
        self.Price=line[3]
        self.Manufacturer=line[4]
        self.number_of_doors=line[5]
        self.size=line[6]
class Phone(Product):
    def __init__(self,screen_size=5,os="",id=1,name="",inventory=10,price=100,manufacturer="Apple"):
        super().__init__(id,name,inventory,price,manufacturer)
        self.screen_size=float(screen_size)
        self.os=os
    def __str__(self):
        return "Phone: with screen size "+str(self.screen_size)+","+"os="+self.os+"   "+self.Name+",inventory= "+str(self.inventory)+",price= "+str(self.Price)+",id= "+str(self.ID)
    def __eq__(self, other):
        return isinstance(other,Phone) and self.Name==other.Name
    def __hash__(self):
        return hash(self.Name)
    def load_list(self,line):
        self.ID=line[0]
        self.Name=line[1]
        self.inventory=line[2]
        self.Price=line[3]
        self.Manufacturer=line[4]
        self.screen_size=float(line[5])
        self.os=line[6]
