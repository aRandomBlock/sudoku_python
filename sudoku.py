import random, time

def possible_solution(values):
	mul = 1
	for _,v in values.items():
		mul *= len(v)
	print("possible_solution:",mul)


def cross(A,B):
	return [a+b for a in A for b in B]

digits = '123456789'
rows = 'abcdefghi'
cols = digits
squares = cross(rows,digits)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('abc','def','ghi') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

grid = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
# print(grid)

def grid_values(grid):
	chars = [c for c in grid if c in digits or c in '0.']
	assert len(chars) == 81
	return dict(zip(squares, chars))

# print(grid_values(grid))
def parse_grid(grid):
	values = dict((s, digits) for s in squares)
	# possible_solution(values)
	if (isinstance(grid,dict)) :
		input_grid = grid
	else:
		input_grid = grid_values(grid)
	
	for s in squares:
		d = input_grid[s]	
		if d in digits:
			values = updatewithassign(values,s,d)
			if values == False:
				return False			
	# possible_solution(values)
	if solve_checker(values):
		return values

	# print('remain')
	for unit in unitlist:
		unsolved = [i for i in unit if len(values[i])>1]
		if unsolved == []:
			continue
		other_values = list(set(digits)-set([values[i] for i in unit]))			
		for o in other_values:
			oplaces = [u for u in unsolved if o in values[u]]
			if (len(oplaces)==0):
				return False
			elif (len(oplaces)==1):
				values = updatewithassign(values,oplaces[0],o)
				if values==False:
					return False		
	# possible_solution(values)
	return values	


def updatewithassign(values,s,d):		
	# print(s,d)
	other_values = values[s].replace(d,'')
	values[s] = d
	if len(d) == 1:
		for s2 in peers[s]:
			if len(values[s2])==1:
				continue			
			if d in values[s2]:
				values[s2] = values[s2].replace(d,'')
				if len(values[s2]) == 0:								
					return False
				elif len(values[s2]) == 1:				
					values = updatewithassign(values,s2, values[s2])
					if values == False:					
						return False				
	for u in units[s]:
		other_values = list(set(digits)-set([values[i] for i in u]))		
		other_values = sorted(other_values)		
		for o in other_values:											
			oplaces = [i for i in u if o in values[i]]								
			if (len(oplaces) == 0):				
				return False
			elif (len(oplaces) == 1) and (values[oplaces[0]] != o):								
				values = updatewithassign(values,oplaces[0], o)
				if values == False:
					return False
	# print('end', s, d)
	# displaySudoku(values)
	return values

def displaySudoku(values):
	if values == False:
		print(False)
	else:		
		width = 1+max(len(values[s]) for s in squares)
		line = '+'.join(['-'*(width*3)]*3)
		for r in rows:
			print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
			if r in 'cf': print(line)

def solve_checker(values):
	unitsolved = lambda unit: set(values[s] for s in unit) == set(digits)	
	return values is not False and all([unitsolved(unit) for unit in unitlist])

def unsolved_count(values):
	return len([s for s in squares if len(values[s])>1])


def recursive_solver(values, solution=[]):	
	if values is False:				
		# print('unsolved')		
		return False
	if all(len(values[s]) == 1 for s in squares):
		# print('solved')	
		solution.append(values)
		return values
	sortbymin = sorted([(len(values[s]),s) for s in squares if len(values[s])>1])	
	s = sortbymin[0][1]
	for d in values[s]:		
		copy_values = values.copy()
		copy_values = updatewithassign(copy_values, s, d)
		# print(s,d)		
		if copy_values is not False:			
		 	copy_values = recursive_solver(copy_values, solution)
		 	if solve_checker(copy_values):		 		
		 		if len(solution) > 1:		 			
		 			print("heelo",len(solution))
		 			return copy_values
		# else:
		# 	print('bluh')		
	return copy_values

def solvermain(values):		
	print("Step:", unsolved_count(values))
	possible_solution(values)
	displaySudoku(values)
	solution = []
	r = recursive_solver(values,solution)

	displaySudoku(r)
	# displaySudoku(values)
	for i in range(len(solution)):
		print("Solution {} =>".format(i+1))
		displaySudoku(solution[i])	
	# print(len(solution))

def unitwise_solver(values):
	if not isinstance(values, dict):
		print('Convert into dictionary')
		return False
	print("Unsolved:", len([s for s in squares if len(values[s])!=1]))
	displaySudoku(values)
	for unit in unitlist:
		values = unitwiseaction(values, unit)
		# break
	# print(' ')
	print("Unsolved:", len([s for s in squares if len(values[s])!=1]))
	# displaySudoku(values)

		# print(remaining_freq)
		# break
def unitwiseaction(values, unit):
	remaining = [s for s in unit if len(values[s])!=1]
	sub_grid = {s:values[s] for s in remaining}
	rs_sub_grid = sorted(sub_grid.items(), key=lambda x:len(x[1]), reverse=True)
	# print(rs_sub_grid)
	
	for i,a in enumerate(rs_sub_grid):
		if len(a[1]) == len(rs_sub_grid): continue
		gr = [a[0]]
		for b in rs_sub_grid[i+1:]:
			if len(a[1]) == len(b[1]):
				if a[1] == b[1]:
					gr.append(b[0])
			else:
				diff = set(b[1])-set(a[1])
				if len(diff)==0:
					gr.append(b[0])
		if len(gr)>1: 
			if len(gr)==len(a[1]): 
				# print(len(rs_sub_grid), len(gr))
				# print(a,gr)
				for s in remaining:
					if s in gr: continue
					change = False
					for d in a[1]:
						if d in values[s]:
							print(s,d, values[s], a, gr)
							values[s] = values[s].replace(d,'')
							change = True
							if len(values[s]) == 0: 
								return False
							elif len(values[s]) == 1:
								values = updatewithassign(values, s, values[s])
								if values == False:
									return False
					if change:
						for u in units[s]:
							values = unitwiseaction(values,u)
				# displaySudoku(values)
	return values

def convertInpuzzle(values): 
	if (isinstance(values,dict) is not True):
		return False
	for k,v in values.items():
		if v == digits:
		 values[k] = '.'
	# print(values)
	return values

def gen_sudoku_grid(try_count=0):
	if try_count == 10: return False

	values = dict((s,digits) for s in squares)
	unsolved = [i for i in squares]
	solved = False
	for i in range(81):
		m = min(len(values[s]) for s in unsolved)
		c = random.choice([s for s in unsolved if len(values[s])==m])
		r = random.choice(values[c])
		
		values = updatewithassign(values, c, r)
		if values == False:
			break
		if solve_checker(values):
			solved = True
			break
		unsolved.remove(c)
		
	if solved == False:		
		values = gen_sudoku_grid(try_count+1)
	# print(try_count)
	return values

def gen_sudoku_puzzle(values, remaining_cells = [], attempts = 0, count =0): 	
	# print(chr(27) + "[2J")
	if remaining_cells == []:
		remaining_cells = [s for s in squares]
	# print(attempts, len(remaining_cells), count)
	# print(remaining_cells)
	if attempts>15:
		# print(attempts)
		# print(len(remaining_cells))
		return values

	if (len(remaining_cells) == 27):		
		# print(2)
		return values
	if (len(set([v for k,v in values.items() if k in remaining_cells])) == 8):
		# print(3)
		return values

	copy_values = values.copy()
	r = random.choice(remaining_cells)	
	og_val = copy_values[r]
	copy_values[r] = digits	

	# displaySudoku(copy_values)
	simplified = parse_grid(copy_values)
	# simplified = False

	if (solve_checker(simplified)): 
		remaining_cells.remove(r)
		copy_values = gen_sudoku_puzzle(copy_values, remaining_cells, attempts, count+1)
	else:
		# print(1)
		res = iterative_solver(simplified)
		# solution = []
		# res = recursive_solver(simplified, solution)		
		
		# if res == False or len(solution)>1:	
		if res == False:	
			# print(r)
			# print('error')	
			copy_values[r] = og_val
			copy_values = gen_sudoku_puzzle(copy_values, remaining_cells,attempts+1, count+1)
		else:
			remaining_cells.remove(r)			
			# displaySudoku(convertInpuzzle(copy_values))
			copy_values = gen_sudoku_puzzle(copy_values, remaining_cells, attempts, count+1)
	# print(copy_values)
	return copy_values

def iterative_solver(values):
	# tree = []
	megalist = []	
	sol = []
	count = 0
	# by_min = sorted([(len(values[s]),s,values[s]) for s in squares if len(values[s]) > 1])
	# min_val = by_min[0][0]
	megalist.append([unsolved_count(values) ,values])
	while len(megalist) > 0:		
		current = megalist[0][:]
		megalist.pop(0)
		count = current[0]
		cur_values = current[-1]
		current = current[1:-1]		
		# by_min = sorted([(len(copy_values[s]),s,copy_values[s]) for s in squares if len(copy_values[s]) > 1])
		by_min = sorted([(len(cur_values[s]),s) for s in squares if len(cur_values[s]) > 1])
		s = by_min[0][1]		
		# print(s)
		for d in cur_values[s]:
			copy_values = cur_values.copy()
			seq = current[:] + [(s,d)]
			# print(seq)

			copy_values = updatewithassign(copy_values, s, d)			
			# displaySudoku(copy_values)
			if copy_values is False:
				# print(2)
				seq.append(False)
				# tree.append(seq)
			elif solve_checker(copy_values):
				# print(1)
				seq.append(copy_values)
				# tree.append(seq)
				sol.append(copy_values)
				if len(sol) > 1:
					return False
				# print(seq)
			else:
				megalist.append([unsolved_count(copy_values)]+seq+[copy_values])
				megalist = sorted(megalist)
				# print(megalist)
		# break
		count+=1
		if count > 100: break

	# print(sol)
	# for s in sol:
	# 	displaySudoku(s)
	# print(megalist)
	# print(count)
	# for i in tree:
		# print(i)
	# print(tree)
	if len(sol) == 1:
		return sol[0]		
	else: 
		return False

def test():	
	# start_time = time.clock()
	# values = gen_sudoku_grid()
	# displaySudoku(values)
	# r = gen_sudoku_puzzle(values)
	# print(r)
	# displaySudoku(convertInpuzzle(r))
	# end_time = time.clock()
	# print(end_time-start_time)

	# displaySudoku(grid_values(grid))
	# grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300' #easy

	# grid = '002000500010705020400090007049000730801030409036000210200080004080902060007000800' #easy
	# grid = '000000000079050180800000007007306800450708096003502700700000005016030420000000000' #med
	# grid = '000000085000210009960080100500800016000000000890006007009070052300054000480000000' #med
	# grid = '000003017015009008060000000100007000009000200000500004000000020500600340340200000' #hard
	# grid = '380000000000400785009020300060090000800302009000040070001070500495006000000000092' #hard
	# grid = '000700800006000031040002000024070000010030080000060290000800070860000500002006000' #hard

	res = parse_grid(grid)
	displaySudoku(res)
	# r = solvermain(res)
	r = iterative_solver(res)
	displaySudoku(r)
	# print(r, len(r))
	# displaySudoku(r)
	# if res!= False:
	# 	solved = solve_checker(res)
	# 	# displaySudoku(res)
	# 	if solved:
	# 		displaySudoku(res)
	# 	else:		
	# 		x = iterative_solver(res)		
	# 		# print(type(x))
	# 		displaySudoku(x)
	# else:
	# 	print(res)

if __name__ == "__main__":
	test()
