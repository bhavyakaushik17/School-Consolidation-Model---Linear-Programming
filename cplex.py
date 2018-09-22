# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 11:24:45 2017

@author: Bhavya
"""
import pulp
import xlrd
import xlwt

#constants
p=80
s=322
g=2
D1=1000
D2=1000
#D3=900
M=1000000;
#Nmin=20;
Nmax=30;
c=100
#D1 = Maximum possible travel between new and old schools
#D2 = Consolidate all schools within D2 (D2<D1)
#capacity = [[0 for i in range (1,s+1)] for j in range (1,g+1)]
'''
Decision Variables: xi,g,j (1,if transfer takes place from to I to j of grade g)and yj
(1 if school is open after consolidation) both binary indicating the transfer and
open/close decision of the schools and nj,g (where n is integer multiplier of 30 to
ensure lower deviations from 30:1 PTR).
'''

#adding excel worksheets to read from and write into
book = xlrd.open_workbook("Chittoor_P1.xls")
book1 = xlwt.Workbook("Chittoor_P1sol.xls")
sheet0 = book.sheet_by_index(0)
sheet1 = book.sheet_by_index(1)
solution = book1.add_sheet("solution")
solution1 = book1.add_sheet("solution_xij")

#N[i] is number of students enrolled in school i, for now g=2 only
N=[]
for i in range(1,s+1):
    N.append(sheet0.cell_value(i,9))

#schoolref will tell the [mandal,panchayat,school number]
def schoolref(s):
    str1=str(sheet0.cell_value(s,7))
    str1=str1.split('.')
    for i in range(len(str1)):
        str1[i]=int(str1[i])
    return str1
#for total number of schools in a panchayat
#no panchayat is common in two mandals, hence sum over panchayats=total for particular mandals
def schooltotal(p):
    r=0
    for i in range(1,s+1):
        if(sheet0.cell_value(r,5) == p):
            r+=1
        while r==0:
            flag=i+1
    return [r,flag]
#for 11dig schoolcode
def schcd(s):
    return sheet0.call_value(s,8)
        #variables
#d[i][j]=distance between schools i and j, panchayat p
d = [[99999 for i in range (s)]for j in range (s)]
j=0
for a in (1,p+1):
    d[i][j] =[[sheet1.cell_value(i,j) for i in range(schooltotal(a)[1],schooltotal(a)[0]+schooltotal(a)[1])]for j in range(schooltotal(a)[1],schooltotal(a)[0]+schooltotal(a)[1])]

my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMinimize)

#LP variables
x = [[pulp.LpVariable('x.'+str(i)+'.'+str(j),cat = 'Binary') for i in range (1,s+1)] for j in range (1,s+1)]
y = [pulp.LpVariable('y.'+str(i),cat = 'Binary') for i in range (1,s+1)]
Nf = [pulp.LpVariable('e.'+str(i),cat = 'Integer') for i in range (1,s+1)]

#objective function
#model 1
o=0
for i in range(0,s):
    for j in range(0,s):
        o+=Nf[i]*x[i][j]
my_lp_problem += o ,"Z"

'''
model 2
o=0
for i in range(1,s+1):
    o+=y[i]
#my_lp_problem += o,"Z"

#model 4
o=0
for i in range(1,s+1):
    for j in range(1,s+1):
        o+=Nf[i]*x[i][j]*d[i][j]
#my_lp_problem +=o,"Z"

#model 8
o=0
for i in range(1,s+1):
    for j in range(1,s+1):
        o+=Nf[i]*x[i][j]
for i in range(1,s+1):
    o+=M*y[i]
#my_lp_problem += o, "Z"
'''

# consstraint 1 (access constraint):
for i in range(0,s):
    for j in range(0,s):
        my_lp_problem += x[i][j]*d[i][j]<=D1

# constraint 2 (logical constraints):
for i in range(0,s):
    for j in range(0,s):
        my_lp_problem += x[i][j]<=y[j]
for i in range(0,s):
    sum1=0
    for j in range(0,s):
         sum1+=x[i][j]
    my_lp_problem += sum1<=1-y[i]

    # constraint 4 (large school opening constraint):
for j in range(0,s):
        my_lp_problem += (N[j]-Nmax)*(1-y[j])<=0

# constraint 5 (no school distance constraint), **only for model 1 and 4: apply
'''for i in range(0,s):
    for j in rangerange(0,s):
        my_lp_problem += d[i][j]-D2>=(y[i]+y[j]-2)*M'''

# constraint 6 (flow balance constraint):
for j in range(0,s):
    sum1=0
    for i in range(0,s):
         sum1+=N[i]*x[i][j]
    sum1=sum1+N[j]*y[j]
    my_lp_problem += sum1 == Nf[j]
sum1=0
for i in range(0,s):
    sum1+=N[i]
sum2=0
for i in range(0,s):
    sum2+=Nf[i]
my_lp_problem += sum1 == sum2

# constraint 7 (capacity constraint):
for i in range(0,s):
    my_lp_problem += c*y[i]>=Nf[i]

solution.write(0,0, "Nf")
solution.write(0,1, "y")
for i in range(1,s+1):
    solution.write(i,0,Nf[i-1].varValue)
for i in range(1,s+1):
    solution.write(i,0,y[i-1].varValue)
solution.write(0,3, "Z(objective function)")
solution1.write(1,3,pulp.value(my_lp_problem.objective))
for i in range(0,s):
    for j in range(0,s):
        solution1.write(i,j,x[i][j].varValue)
#saving the solution workbook
book1.save("Chittoor_P1sol.xls")


'''
    {
      forall ( j in 1 .. schoolTotal[m] ) {
        ( sum ( g in grades ) excelEnrolment[j][g] - Nmax ) * ( 1 - y[m][j] )
           <= 0;
      }
    }
  forall ( m in mandal : m >= 2 ) {
    forall ( j in 1 .. schoolTotal[m] ) {
      (( sum ( g in grades ) (excelEnrolment[j + (sum(k in 1..m-1)(schoolTotal[k]))][g])) - Nmax )
         * ( 1 - y[m][j] ) <= 0;
    }
  }
  cons4:
    forall ( m in mandal, i in 1 .. schoolTotal[m], g in grades,
       j in 1 .. schoolTotal[m] : i == j )
      x[m][i][g][j] == 0;


  cons5:
    forall ( m in mandal, i in 1 .. schoolTotal[m], g in grades,
       j in 1 .. schoolTotal[m] : m == 1 && i != j  ) {
      x[m][i][g][j] * excelDistance[i][j] <= D1;
    }
  cons5c:
    forall ( m in mandal, i in 1 .. schoolTotal[m], g in grades,
       j in 1 .. schoolTotal[m] : m >= 2 && i != j  ) {
      x[m][i][g][j] * excelDistance[i + (sum(k in 1..m-1)(schoolTotal[k]))][j + (sum(k in 1..m-1)(schoolTotal[k]))] <= D1;
    }
  cons5b:
    forall ( m in mandal, i in 1 .. schoolTotal[m], g in grades ) {
      sum ( j in 1 .. schoolTotal[m] ) x[m][i][g][j] == 1 - y[m][i];
    }
  cons6:
    forall ( m in mandal, i in 1 .. schoolTotal[m], g in grades,
       j in 1 .. schoolTotal[m] : i != j ) {
      x[m][i][g][j] <= y[m][j];
    }
  cons7:
    forall ( m in mandal, j in 1 .. schoolTotal[m], g in grades : m == 1 ) {
      excelStudents[j][g] == sum ( i in 1 .. schoolTotal[m] : i != j )
        ( excelEnrolment[i][g] * x[m][i][g][j] )
         + excelEnrolment[j][g] * y[m][j];
    }
  cons7a:
    forall ( m in mandal, j in 1 .. schoolTotal[m], g in grades : m >= 2 ) {
      excelStudents[j+ (sum(k in 1..m-1)(schoolTotal[k]))][g] == sum ( i in 1 .. schoolTotal[m] : i != j )
        ( excelEnrolment[i + (sum(k in 1..m-1)(schoolTotal[k]))][g] * x[m][i][g][j] )
         + excelEnrolment[j + (sum(k in 1..m-1)(schoolTotal[k]))][g] * y[m][j];
    }
  //  cons8:
  //    forall ( j in schools, g in grades ) {
  //      totalstudents[j][g] <= capacity[j][g] * y[j];
  //    }
  cons8b:
    forall ( m in mandal, i in 1 .. schoolTotal[m], j in 1 .. schoolTotal[m] :
       m == 1 && i != j ) {
      ( sum ( g in grades ) excelEnrolment[i][g] - Nmax <= 0 ) =>
        ( excelDistance[i][j] - D2 ) >= ( y[m][i] + y[m][j] - 2 ) * M;
    }
  cons8c:
    forall ( m in mandal, i in 1 .. schoolTotal[m], j in 1 .. schoolTotal[m] :
       m >= 2 && i != j ) {
      ( sum ( g in grades ) excelEnrolment[i + (sum(k in 1..m-1)(schoolTotal[k]))][g] - Nmax <= 0 ) => ( excelDistance[i + (sum(k in 1..m-1)(schoolTotal[k]))][j + (sum(k in 1..m-1)(schoolTotal[k]))] - D2 ) >= ( y[m][i] + y[m][j] - 2 ) * M;
    }
  cons9:
    forall ( m in mandal, g in grades : m == 1 ) {
      sum ( j in 1 .. schoolTotal[m] ) excelStudents[j][g] == sum
        ( i in 1 .. schoolTotal[m] ) excelEnrolment[i][g];
    }
  cons9b:
    forall ( m in mandal, g in grades : m >= 2 ) {
      sum ( j in 1 .. schoolTotal[m] ) excelStudents[j+ (sum(k in 1..m-1)(schoolTotal[k]))][g] == sum
        ( i in 1 .. schoolTotal[m] ) excelEnrolment[i + (sum(k in 1..m-1)(schoolTotal[k]))]
        [g];
    }
    cons10:
    forall ( i in schools)
      { sum(g in grades)excelStudents[i][g]>=1=> z[i]==1;
    }


//  obj >= sum (m in mandal,i in schools, g in grades, j in schools:m==1 )
//     excelEnrolment[i][g] * x[m][i][g][j]*excelDistance[i][j];

 obj >= sum (m in mandal,i in schools, g in grades, j in schools:m==1 )
     excelEnrolment[i][g] * x[m][i][g][j]*excelDistance[i][j]+sum (m in mandal,i in 1 .. schoolTotal[m], g in grades, j in 1 .. schoolTotal[m]:m>=2 )
     excelEnrolment[i+(sum(k in 1..m-1)(schoolTotal[k]))][g] * x[m][i][g][j]*excelDistance[i+(sum(k in 1..m-1)(schoolTotal[k]))][j+(sum(k in 1..m-1)(schoolTotal[k]))];

}
execute {


  writeln("totalStud" + excelStudents);
  writeln("schools_open" + y);
  for (var m = 1; m <= 44; m++) {

    for (var i = 1; i <= 588; i++) {
      for (var g = 1; g <= 2; g++)
        for (var j = 1; j <= 588; j++){
          if (x[m][i][g][j] == 1)

          {

            writeln(" ", +m, "  ", +i, "  ", +g, "  " + j, " "
                + x[m][i][g][j]);
}
}}
}

 writeln("My Answer" + obj);

}'''