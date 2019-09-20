import numpy as np
import math
import os
import time
def get_rows(n):
	rows = []
	for i in range(1,n*n+1,n):
		row_list = []
		for j in range(n):
			row_list.append(i+j)
		rows.append(row_list)
	return rows

def get_columns(n):
	cols = []
	for i in range(n):
		col_list = []
		for j in range(i+1,n*n+1,n):
			col_list.append(j)
		cols.append(col_list)
	return cols


def get_diagonals(problem):
	n = len(problem)
	matrix = np.array(problem)
	diagonals = []
	diags = [matrix[::-1,:].diagonal(i) for i in range(-(n-2),n-1)]
	diags.extend(matrix.diagonal(i) for i in range(n-2,-n+1,-1))
	for i in diags:
		diagonals.append(i.tolist())
	return diagonals

def CNF_expression(problem,type='at_most_one'):
	constraints = ''
	n = len(problem)
	for i in range(n-1):
		for j in range(i+1,n):
			constraints = constraints + '-' + str(problem[i]) + ' ' + '-' + str(problem[j]) + ' 0' + '\n'
	
	if (type == 'exactly_one'):
		for i in problem:
			constraints = constraints + str(i) +' '
		constraints = constraints + '0' + '\n'

	return constraints

def make_queen_sat(N):
	CNF_constraints = ''
	rows  = get_rows(N)
	for i in rows:
		CNF_constraints = CNF_constraints + CNF_expression(i,type='exactly_one')

	columns  = get_columns(N)
	for j in columns:
		CNF_constraints = CNF_constraints + CNF_expression(j,type='exactly_one')

	diagonals = get_diagonals(get_rows(N))
	for k in diagonals:
		CNF_constraints = CNF_constraints + CNF_expression(k)

	first_line = 'c N=' + str(N) + ' ' + 'queens problem' + '\n'
	num_vbles = N*N
	num_clauses = CNF_constraints.count('\n')
	second_line = 'p cnf ' + str(num_vbles) + ' ' + str(num_clauses) +'\n'
	final_input = first_line + second_line + CNF_constraints
	return final_input

def draw_queen_sat_sol(sol):
	if sol == 'UNSAT':
		print ('No solution')
	else:
		a = sol.split()
		sol_list = []
		for i in a:
			sol_list.append(int(i))
		length = len(sol_list)
		n = int(math.sqrt(length))
		if n > 40:
			print ('Too big: N must be less than 40')
		model = ''
		count = n
		for i in range (n):	
			for j in range (i*n,(i+1)*n):
				if sol_list[j] < 0:
					model = model +  ' . '
				elif sol_list[j] > 0:
					model = model + ' Q '
			count = count - 1 
			if count > 0:
				model = model + '\n'
		print (model)
# print(make_queen_sat(4))

# draw_queen_sat_sol('-1 -2 3 -4 5 -6 -7 -8 -9 -10 -11 12 -13 14 -15 -16 17 -18 -19 -20 21 -22 -23 -24 -25')
def read_file():
	f = open('out','r')
	return f.read()

def experiment_stat(n):
	i = 2
	while True:
		f = open('queens.txt','w+')
		f.write(make_queen_sat(i))
		f.close()
		start_time = time.time()
		os.system('minisat queens.txt out')
		elapsed_time = time.time() - start_time()
		print ('Minisat number' + str(i) + '\n' + 'Time taken is' + str(elapsed_time))
		# draw_queen_sat_sol(read_file())
		if read_file == 'UNSAT':
			print ('Unsat')
		if elapsed_time > n:
			print ('MAX_N = ' + str(i-1) + '\n' + 'Time taken is less than' + str(n))
			break
		i = i + 1
	return i 

