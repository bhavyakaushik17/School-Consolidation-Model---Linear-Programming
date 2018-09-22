# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:48:23 2017

@author: Bhavya
"""
import pulp
import xlrd
import xlwt

book = xlrd.open_workbook("LPprob.xls")
book1 = xlwt.Workbook("LPsol.xls")
variables = book.sheet_by_index(0)
objfunc = book.sheet_by_index(1)
constraints = book.sheet_by_index(2)
solution = book1.add_sheet("solution")

#variables
my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)
x = pulp.LpVariable('x', lowBound=float(variables.cell_value(1,2)), cat='Continuous')
y = pulp.LpVariable('y', lowBound=float(variables.cell_value(2,2)), cat='Continuous')

# Objective function
my_lp_problem += float(objfunc.cell_value(1,2))* x + float(objfunc.cell_value(2,2))* y, "Z"

# Constraints
my_lp_problem += float(constraints.cell_value(1,2))*x + float(constraints.cell_value(2,2))*y <= float(constraints.cell_value(3,2))
my_lp_problem += float(constraints.cell_value(1,3))*x + float(constraints.cell_value(2,3))*y <= float(constraints.cell_value(3,3))
my_lp_problem += float(constraints.cell_value(1,4))*x + float(constraints.cell_value(2,4))*y <= float(constraints.cell_value(3,4))
e =float(constraints.cell_value(1,2))*x + float(constraints.cell_value(2,2))*y <= float(constraints.cell_value(3,2))
#to print out the problem statement:
my_lp_problem

#solving
my_lp_problem.solve()
pulp.LpStatus[my_lp_problem.status]

Z= pulp.value(my_lp_problem.objective)

for variable in my_lp_problem.variables():
    print ("{} = {}".format(variable.name, variable.varValue))

print ("Z(objective function value) = ", pulp.value(my_lp_problem.objective))

#writing solution to excel
solution.write(0,0, "Variable")
solution.write(0,1, "Value")
solution.write(1,0, "x")
solution.write(2,0, "y")
solution.write(3,0, "Z(objective function)")
solution.write(1,1, x.varValue)
solution.write(2,1, y.varValue)
solution.write(3,1,pulp.value(my_lp_problem.objective))
book1.save("LPsol.xls")




