from datetime import datetime
from dateutil import relativedelta


class Employee:
   def __init__(self,emp_id,name,designation,department,base_salary,DOJ):
       self.emp_id=emp_id
       self.name=name
       self.designation=designation
       self.department=department
       self.base_salary=int (base_salary)
       self.DOJ=datetime.strptime(DOJ,"%d/%m/%Y")
       
   def tax(self,total):
      # to follow the given slabs for tax deduction 
      if (total<=700000):
         return ((0.1)*(total))
      elif(total<=1500000):
         return (((0.1)*(700000)) + ((0.2)*(total-700000)))
      else:
         return((((0.1)*700000) + ((0.2)*(800000))) + ((0.3)*(total-1500000)))
      
   
# Salaried employee 

class Salaried (Employee):
   def __init__(self,emp_id , name, designation , department, base_salary, DOJ,DOP,insurance,other_benefits, taken_leaves_in_this_month):
      super().__init__( emp_id,name, designation, department ,base_salary,DOJ)
      self.DOP=datetime.strptime(DOP, "%d/%m/%Y")
      self.insurance = insurance
      self.other_benefits = other_benefits
      self.taken_leaves_in_this_month= taken_leaves_in_this_month
      pass
   

   #leave management 
   def leave_management(self):
       leave_deduction=0
       paid_leaves= int(input("enter the remainig paid leaves for this month: "))
       # calculating the tenure of employye :
       delta=relativedelta.relativedelta(self.DOP,self.DOJ)

       if(delta.years >=5 ):
          Extra_months=((delta.months + (delta.years * 12) ) - (5*12))
          paid_leaves+= Extra_months//2  # providing 6 extra leaves per year as a bonus to the employee having tenure more than 5 years  

       # updating the leaves if paid > taken ones
       if paid_leaves <self.taken_leaves_in_this_month:
          leave_deduction = (self.taken_leaves_in_this_month - paid_leaves) * (self.base_salary/30)
       return leave_deduction 
         
   # calculating total salary         
   def t_s(self):
      salary= self.base_salary -(self.insurance + self.other_benefits + self.leave_management())
      return (salary-self.tax(salary))



# contractual emplyee 
class Contractual (Employee):
   def __init__(self,emp_id,name,designation,department, base_salary, DOJ,taken_leaves_in_this_month):
      super().__init__(emp_id,name,designation,department,base_salary, DOJ)
      self.taken_leaves_in_this_month= taken_leaves_in_this_month
   
   # overtime as bonus
   def overtime(self):
      worked_hours = int(input("enter the hours worked this month : "))
      if worked_hours > 160:
         return (worked_hours-160)*(self.base_salary /160)*(1.5)
      return 0
   
   #leave management 
   def leave_management(self):
      leave_deduction=0
      total_paid_leaves = int(input("enter the total paid leaves provided to employee during his tenure : "))
      if self.taken_leaves_in_this_month > total_paid_leaves :
         leave_deduction=(self.taken_leaves_in_this_month - total_paid_leaves) * (6*(self.base_salary/160))  # assumed that a standard hours per day of work are 6hrs 
      return leave_deduction

   # toatal salary 
   def t_s(self):
      salary= self.base_salary + self.overtime() - self.leave_management()
      total_salary=salary-self.tax(salary)
      return total_salary
# commission based employee
class Commisioned (Employee):
   def __init__(self,emp_id,name,designation,department,base_salary,DOJ,sale_percentage):
      super().__init__(emp_id,name,designation,department,base_salary,DOJ)
      self.sale_percentage= sale_percentage

   # commission  as bonus   
   def bonus(self):
      return (self.sale_percentage * self.base_salary) / 100 
   
   #total salary 
   def t_s(self ):
      salary= self.base_salary + self.bonus()
      total_salary=salary- self.tax(salary)
      return total_salary

if __name__=="__main__":
   emp_id=input("employee id : ")
   name=input("employee name: ")
   designation = input("Designation: ")
   department= input("department: ")
   base_salary = input("Base Salary : ")
   DOJ = input("Date Of Joining (DD/MM/YYYY) :  ")
   type = int(input("enter choice  : \n 1 . Salaried employee \n 2. contractual employee \n 3. commision based employee \n >>your type : "))

   
   if type == 1 :
      DOP=input("Date of pay slip generation (DD/MM/YYYY) :")
      insurance = int(input("insurance amount: "))
      other_benefits=int(input("other benefits Amount : "))
      taken_leaves_in_this_month = int(input("taken leaves in this month :"))
      employe=Salaried(emp_id,name,designation,department,base_salary,DOJ,DOP,insurance,other_benefits,taken_leaves_in_this_month)

   elif type == 2 :
      taken_leaves_in_this_month = int(input("taken leaves in this month :"))
      employe=Contractual(emp_id, name,designation,department,base_salary,DOJ, taken_leaves_in_this_month)

   elif type == 3 :
      sale_percentage = int(input("enter the commission percentage on sales: "))
      employe=Commisioned(emp_id,name,designation,department,base_salary,DOJ,sale_percentage)
   else : print("choice out of range ")
      

   print(f"total salary for {name} : {employe.t_s()}")

     
   
