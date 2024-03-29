import re
import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt

vars = input("Enter 3 vars (ex: xyz): ")
ax = plt.figure().gca(projection='3d')

def read_expresion(string):
	string2 = re.sub("\s","",string)
	# Add coefficient 1 to single variables (replace "x" with "1x")
	for i in [i[-1] for i in re.findall("\D{1}[a-z]+"," " + string)]:
		string2 = re.sub(f"[{i}]","1"+i,string2)
	# List coefficients (including negatives, decimals and fractions)
	coefficients = re.findall("[-]?[0-9]+[,.]?[0-9]*[/]?[0-9]*[,.]?[0-9]*",string2)
	coefficients,constant = list(map(float,map(Fraction,coefficients[:-1]))),float(Fraction(coefficients[-1])) # Get the constant
	# List variables
	variables = re.findall(f"[{vars}]+",string2)
	# Add remaining variables with coefficient 0
	for i,var in enumerate(list(vars)):
		if var not in variables:
			variables.insert(min(len(variables)-1,i),var)
			coefficients.insert(min(len(variables)-1,i),0)
	return coefficients,constant

def det(m):
	# Determinant of a matrix
	return round(np.linalg.det(m.astype(float)),2)

def adj(m):
	# Adjugate of a matrix (transpose of cofactor matrix)
	return np.array([
		[+det(np.array([[m[1,1],m[1,2]],[m[2,1],m[2,2]]])), -det(np.array([[m[0,1],m[0,2]],[m[2,1],m[2,2]]])), +det(np.array([[m[0,1],m[0,2]],[m[1,1],m[1,2]]]))],
		[-det(np.array([[m[1,0],m[1,2]],[m[2,0],m[2,2]]])), +det(np.array([[m[0,0],m[0,2]],[m[2,0],m[2,2]]])), -det(np.array([[m[0,0],m[0,2]],[m[1,0],m[1,2]]]))],
		[+det(np.array([[m[1,0],m[1,1]],[m[2,0],m[2,1]]])), -det(np.array([[m[0,0],m[0,1]],[m[2,0],m[2,1]]])), +det(np.array([[m[0,0],m[0,1]],[m[1,0],m[1,1]]]))]
	])

def inv(m):
	return adj(m)/det(m) # also np.linalg.inv(m)

def rank(m):
	return np.linalg.matrix_rank(m.astype(float))

def solve(eq1,eq2,eq3):
	variables = list(vars)
	M_c = np.empty((0,3)) # coefficient matrix
	constants = np.empty((0,1))
	for eq in (eq1,eq2,eq3):
		coefs,const = read_expresion(eq)
		M_c = np.vstack((M_c,coefs))
		constants = np.vstack((constants,const))
	M_a = np.concatenate((M_c,constants),axis=1) # augmented matrix

	# Solve the system
	if det(M_c) != 0:
		system_type = "Independent System"
		# Cramer's rule
		Mx = np.copy(M_c)
		Mx[:,0] = constants[:,0]
		My = np.copy(M_c)
		My[:,1] = constants[:,0]
		Mz = np.copy(M_c)
		Mz[:,2] = constants[:,0]
		x = det(Mx)/det(M_c)
		y = det(My)/det(M_c)
		z = det(Mz)/det(M_c)
		ax.scatter(x,y,z,"o")
	else:
		# Rouché-Frobenius/Capelli theorem
		if rank(M_c) != rank(M_a): system_type = "Inconsistent System"
		elif rank(M_c) == rank(M_a) != 3: system_type = "Dependent System"

	# Plot planes
	for row,eq in zip(M_a,(eq1,eq2,eq3)):
		X = np.linspace(-10,10,2)
		Y = np.linspace(-10,10,2)
		X,Y = np.meshgrid(X,Y)
		Z = (row[3] - row[0]*X - row[1]*Y) / row[2]
		surf = ax.plot_surface(X,Y,Z,alpha=0.5,label=eq)
		surf._facecolors2d=surf._facecolors3d
		surf._edgecolors2d=surf._edgecolors3d

	# Print solution
	print(f"\nSystem type: {system_type}")
	if system_type == "Independent System":
		print(f"""
The planes intersect in a point:
{variables[0]} = {x}
{variables[1]} = {y}
{variables[2]} = {z}
""")
	elif system_type == "Dependent System":
		print("\nThis system has infinite possible solutions. The planes intersect in a line or a plane\n")
	else:
		print("\nThis system has no solution.\n")

	# Plot settings
	ax.set_xlabel(f"${variables[0]}$")
	ax.set_ylabel(f"${variables[1]}$")
	ax.set_zlabel(f"${variables[2]}$")
	ax.legend()
	plt.show()

solve(	input("Equation 1: "),
		input("Equation 2: "),
		input("Equation 3: "))
