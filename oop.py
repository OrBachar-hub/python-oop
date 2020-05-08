##Or Bachar 205972805
import csv
from datetime import date
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
        if self.findByID(other.ID)==False:
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
    def findByID(self,id):
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

class Sales:
    def __init__(self,customer_id,prod_id,price,date):
        self.customer_id=customer_id
        self.prod_id=prod_id
        self.price=price
        self.date=date
    def __str__(self):
        return self.customer_id+" "+self.prod_id+" "+str(self.price)+" "+str(self.date)

class coupon:
    SIMPLE_DIS=0
    PERCENTAGE=1
    def __init__(self,type,discount,pr_id,name,date="1/1/2020"):
        self.type=type
        self.discount=discount
        self.pr_id=pr_id
        self.name=name
        self.date=date
    def __eq__(self, other):
        return isinstance(other,coupon) and self.name==other.name
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
            if object==Phone:
                for i in read:
                    p=Phone(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
                    self.add_prod(p)
            if object==Refrigerator:
                for i in read:
                    p=Refrigerator(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
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
    def __init__(self, cus_file_name, phone_file, ref_file):
        self.cus_lst=CustomerList(cus_file_name)
        self.ProductsList=Product_list()
        if phone_file!="empty":
            self.ProductsList.load_from_file(phone_file,Phone)
        if ref_file!="empty":
            self.ProductsList.load_from_file(ref_file,Refrigerator)
        self.sales=[]
    def make_sale(self,cus_id,prod_name):
        if self.cus_lst.findByID(cus_id)==False or self.ProductsList.findProduct(prod_name)==False:
            return False
        p = self.ProductsList.findProduct(prod_name)
        c=self.cus_lst.findByID(cus_id)
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
        # back=""
        list=[]
        for i in self.sales:
            # back +=str(i)+"\n"
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
    def __init__(self,id=1,name="",inventory=10,price=100,manufacturer="",number_of_doors=2,size=500):
        super().__init__(id,name,inventory,price,manufacturer)
        self.number_of_doors=int(number_of_doors)
        self.size=int(size)
    def __str__(self):
        return "Refrigerator: of size "+str(self.size)+"   "+",inventory= "+str(self.inventory)+",price= "+str(self.Price)+",id= "+str(self.ID)
    def __eq__(self, other):
        return isinstance(other,Refrigerator)
    def __hash__(self):
        return hash(self.Name)

class Phone(Product):
    def __init__(self,id=1,name="",inventory=10,price=100,manufacturer="Apple",screen_size=5,os=""):
        super().__init__(id,name,inventory,price,manufacturer)
        self.screen_size=float(screen_size)
        self.os=os
    def __str__(self):
        return "Phone: with screen size "+str(self.screen_size)+","+"os="+self.os+"   "+",inventory= "+str(self.inventory)+",price= "+str(self.Price)+",id= "+str(self.ID)
    def __eq__(self, other):
        return isinstance(other,Phone)
    def __hash__(self):
        return hash(self.Name)
# p=Product("42","koalaFinder",1,100000,"bestAnimal")
# c=Customer(["14","or","bachar","daniel","054213","M"])
# c1=Customer(["15","or","bachar","daniel","054213","M"])
# l1=CustomerList("custmer.csv")
# l1.AddCustomer(c)
# l1.AddCustomer(c1)
# c=coupon(coupon.PERCENTAGE,4,4,"new year")
# cc=coupon(coupon.SIMPLE_DIS,2000,2,"new ear")
# ccc=coupon(coupon.PERCENTAGE,3,4,"new yer")
# cccc=coupon(coupon.SIMPLE_DIS,1000,4,"ne year")
# ross=s.cus_lst.findByID(12)
# ross.add_coupon(c)
# ross.add_coupon(cc)
# ross.add_coupon(ccc)
# ross.add_coupon(cccc)
# sl=s.make_sale(12,"Ipad3")
# print(sl)
# print(pl)
# print(s.prod_lst)
# print(s.prod_lst.productList[1])

s=Store("custmer.csv","phone.csv","refrigerator.csv")
ph=Phone(5,"ap")
re=Refrigerator()
print(ph)
print(re)
pl=s.find_phone_by_size(4.2,6)
print(pl)
print("good to here")
c=coupon(coupon.PERCENTAGE,4,1,"new year")
ross=s.cus_lst.findByID(12)
ross.add_coupon(c)
s.make_sale(12,"Iphone8")
s.make_sale(14,"Iphone8")
s.make_sale(12,"Iphone2")
s.make_sale(12,"big blue")
sales_list=s.get_all_sales()
for i in s.ProductsList.productList:
    print(i)
for x in sales_list:
    print(x)
print(s.profit())
print(s.count_product(Phone))
print(s.count_product(Refrigerator))