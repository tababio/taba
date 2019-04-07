#! /usr/bin/python
# Program to generate a scatter plot, and find the best fit polynommial equation.
# Data for arrays x and y are read from a CSV file  

import numpy as np
import matplotlib.pyplot as plt

################
# Open csv file
import csv
print("Reading resultadoTreino.csv...")
fo1 = open("./outputFiles/resultadoTreino.csv","r")
csv1 = csv.reader(fo1)

# Set empty list for input data
input_data = []

# Looping through first line to get "Predicted" "Experimental" indeces
for line0 in csv1:
    count_line = 0
    aux_line0 = str(line0).replace("\'","")
    aux_line1 = aux_line0.replace("[","")
    aux_line2 = aux_line1.replace("]","")
    aux_line3 = aux_line2.replace(" ","")
    first_line = str(aux_line3)
    break

# Get data
for line in csv1:
    aux_line0 = str(line).replace("[","")
    aux_line1 = aux_line0.replace("]","")
    aux_line2 = aux_line1.replace(" ","")
    aux_line3 = aux_line2.replace("\'","")
    input_data.append(str(aux_line3))

fo1.close()
print("Done")

##############################

# Reads CSV file to get predicted and experimental data
my_csv = np.genfromtxt ('./outputFiles/resultadoTreino.csv', delimiter=",", skip_header = 1)

# Gets each column from CSV file
y = my_csv[:,6]
x = my_csv[:,5]
 
# Generates plot
plt.scatter(x,y) 

#Least-squares polynomial fitting 
z = np.polyfit(x,y, 1)
p = np.poly1d(z)

# Equation y = ax + b
# z array has the coefficients a = z[0] and b = z[1] 
print("a = ",z[0])
print("b = ",z[1])
print("Best fit polynomial equation: ",p)


####################################
# Open new file
fo2 = open("./outputFiles/opt_results.csv","w")
fo2.write(first_line+",ax+b\n")

for i in range(len(y)):
    #fo2.write(str(input_data[i])+","+str(p(x[i]))+","+str(float(z[0])*float(x[i])+float(z[1]))+"\n") # Only to test the equation
    fo2.write(str(input_data[i])+","+str(p(x[i]))+"\n")

# Close new file
fo2.close()


#################################
# Read equation
fo3 = open("./outputFiles/melhorEquacao.csv","r")
for line0 in fo3:
    break

# Get b
b0 = ""
my_flag = False
for line0 in fo3:
    for line2 in line0[17:]:
        b0 += str(line2)
    break
b1 = ""

# Some editing
for line in b0[1:]:
    if str(line[0]) == "+" or str(line[0]) == "-":
        break
    else:
        b1 += str(line[0])
aux_b = str(b0[0])+str(b1)
my_b = float(aux_b)

# Set up empty list for coefficients for old equation
my_coef = []

# my_b is the c0
my_coef.append(my_b)

# More editing
aux_string = str(b0[len(str(my_b)):])

my_c = []
c_aux = ""
my_index = 0
while len(aux_string[my_index:]) > 1:
    i = 0
    for line in aux_string[my_index:]:
        c_aux += str(line[0])
        i += 1
        if str(line[0]) == "*":
            c_out = c_aux.replace("*","")
            my_c.append(c_out)
            c_aux = ""
            my_index += i

for line in my_c:
    if ")" in str(line):
        index_par = str(line).index(")")
        my_coef.append(float(line[index_par+1:]))
    else:
        my_coef.append(float(line))

# Close file
fo3.close()
#################################
# For 3 explanatory variables
# Reads CSV file to get predicted and experimental data
my_csv = np.genfromtxt ('./outputFiles/resultadoTreino.csv', delimiter=",", skip_header = 1)

# Gets each column from CSV file
x1 = my_csv[:,2]
x2 = my_csv[:,3]
x3 = my_csv[:,4]

print("Coefficients:",my_coef[0],my_coef[1],my_coef[2],my_coef[3])

# Taken from Taba
d_x1 = 4.953239146161247
d_x2 = 4.9474703703392455
d_x3 = 5.241119061541568

# Calculates predicted (to check if everything is fine)
c0 = float(my_coef[0])
c1 = float(my_coef[1])
c2 = float(my_coef[2])
c3 = float(my_coef[3])
a = z[0]
b = z[1]

print("Applying a =",a," and b = ", b, "to old equation...")

# Apply ax + b to y_old (pred)
# Looping data to check equation
#for i in range(len(x1)):
#    pred_old = c0+c1*(x1[i]-d_x1)**2+c2*(x2[i]-d_x2)**2+c3*(x3[i]-d_x3)**2
#    pred_new = a*c0+b+a*c1*(x1[i]-d_x1)**2+a*c2*(x2[i]-d_x2)**2+a*c3*(x3[i]-d_x3)**2
#    print(x1[i],x2[i],x3[i],pred_old,pred_new,my_csv[i][6])

# Calculates new coefficients 
d0 = float(my_coef[0])*a + b
d1 = float(my_coef[1])*a
d2 = float(my_coef[2])*a
d3 = float(my_coef[3])*a

# Looping data to check equation
for i in range(len(x1)):
    pred_old = c0+c1*(x1[i]-d_x1)**2+c2*(x2[i]-d_x2)**2+c3*(x3[i]-d_x3)**2
    #pred_new = a*c0+b+a*c1*(x1[i]-d_x1)**2+a*c2*(x2[i]-d_x2)**2+a*c3*(x3[i]-d_x3)**2
    pred_new = d0+d1*(x1[i]-d_x1)**2+d2*(x2[i]-d_x2)**2+d3*(x3[i]-d_x3)**2
    print(x1[i],x2[i],x3[i],pred_old,pred_new,my_csv[i][6])

# Open new file
fo4 = open("./outputFiles/new_results.csv","w")
fo4.write(first_line+",a(y_old)+b\n")

# Looping through data to write new file
for i in range(len(y)):
    #fo4.write(str(input_data[i])+","+str(p(x[i]))+","+str(float(z[0])*float(x[i])+float(z[1]))+"\n") # Only to test the equation
    pred_new = d0+d1*(x1[i]-d_x1)**2+d2*(x2[i]-d_x2)**2+d3*(x3[i]-d_x3)**2
    fo4.write(str(input_data[i])+","+str(pred_new)+"\n")

# Close new file
fo4.close()

#################################
# Generates plot
plt.plot(x, p(x), '-')

# Shows plot
plt.show()

# Saves plot on png file
#plt.savefig('scatter_plot3.png')
