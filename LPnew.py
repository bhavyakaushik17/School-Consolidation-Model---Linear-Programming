# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:48:23 2017

@author: Bhavya
"""
#first import pulp and other excel read and write libraries
import pulp
import xlrd
import xlwt

#adding excel worksheet to read from
book = xlrd.open_workbook("LPprob.xls")
book1 = xlwt.Workbook("LPsol.xls")
variables = book.sheet_by_index(0)
objfunc = book.sheet_by_index(1)
constraints = book.sheet_by_index(2)
solution = book1.add_sheet("solution")

#number of variables is n-1
n=variables.nrows
#number of constraint equations is e-2
e=constraints.ncols

#creating lists, for simplicity in calling values from
#particular excel rows and columns later on
var=[]
for i in range(1,n):
    var.append(variables.cell_value(i,1))
lowb=[]
for i in range(1,n):
    lowb.append(variables.cell_value(i,2))
upb=[]
for i in range(1,n):
    upb.append(variables.cell_value(i,3))
cat=[]
for i in range(1,n):
    cat.append(variables.cell_value(i,4))
objcoeff=[]
for i in range(1,n):
    objcoeff.append(objfunc.cell_value(i,2))


#specifying the problem, maximise or minimise, and the variables and their domain etc.
my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)
x=[]
for i in range(1,n):
    x.append('x'+str(i))
for i in range(0,n-1):
    if upb[i]=='None' and lowb[i] =='None':
            x[i]= pulp.LpVariable(x[i], cat=cat[i])
    elif upb[i]=='None':
            x[i]= pulp.LpVariable(x[i], lowBound=float(lowb[i]), cat=cat[i])
    else:
            x[i]= pulp.LpVariable(x[i], lowBound=float(lowb[i]),upBound=float(upb[i]), cat=cat[i])

#So the problem variables are denoted by x[t], t can be 1,2,..n-1

# Objective function "Z"
o=0
for i in range(0,n-1):
    o=x[i]*objcoeff[i] + o
my_lp_problem += o , "Z"


# Constraints
c=dict()
for j in range(0,e-2):
    c[j]=[]
    for i in range(1,n):
        c[j].append(constraints.cell_value(i,j+2))
const=[]
for j in range(2,e):
    const.append(constraints.cell_value(n,j))
expn=[]
for j in range(0,e-2):
    expn.append(0)
for j in range(0,e-2):
    for i in range(0,n-1):
       expn[j]=c[j][i]* x[i] + expn[j]

for j in range(0,e-2):
    my_lp_problem += expn[j] <= const[j]


#to print out the problem statement:
my_lp_problem


#solving
my_lp_problem.solve()
pulp.LpStatus[my_lp_problem.status]
Z= pulp.value(my_lp_problem.objective)


#print out the solution in console
for variable in my_lp_problem.variables():
    print ("{} = {}".format(variable.name, variable.varValue))
print ("Z(objective function value) = ", pulp.value(my_lp_problem.objective))


#writing solution to seperate excel worksheet
solution.write(0,0, "Variable")
solution.write(0,1, "Value")
for i in range(1,n):
    solution.write(i,0,var[i-1])
solution.write(n,0, "Z(objective function)")
for i in range(1,n):
    solution.write(i,1, x[i-1].varValue)
solution.write(n,1,pulp.value(my_lp_problem.objective))


#saving the solution workbook
book1.save("LPsol.xls")




