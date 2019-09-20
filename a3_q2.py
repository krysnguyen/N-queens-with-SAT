import random
from itertools import combinations
import subprocess
import time
class Graph:
    def __init__(self, graph_dict):
        self.graph_dict = {}

    def connect(self, A, B):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.graph_dict[A].append(B)
        self.graph_dict[B].append(A)

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
        # return '1'

    def add_nodes_loop(self,n):
        for i in range (n):
            self.graph_dict.setdefault(i,[])


def rand_graph(n, p):
    G = Graph(graph_dict = {})
    G.add_nodes_loop(n)
    for u, v in combinations(G.graph_dict, 2):
         if random.random() < p:
             G.connect(u, v)
    return G.graph_dict

def nodes(g):
    nodes_list = []
    for k in g.keys():
        nodes_list.append(k+1)
    return nodes_list

def edge_not_exist(edge,edgeList):
    for i in edgeList :
        if edge == i or edge == i[::-1]:
            return False
    return True


def edges(g):
    edge_list = []
    for k in g.keys():
        for v in g[k]:
            edge = [k+1,v+1]
            if (edge_not_exist(edge,edge_list) == True):
                edge_list.append(edge)
    return edge_list

def variables(nodes,k):
    variables_list = []
    for i in range (len(nodes)):
        var_list = []
        for j in range (i*k+1,k*(i+1)+1):
            var_list.append(j)
        variables_list.append(var_list)
    return variables_list

def edge_list(list_edge,k):
    constraint_lst = []
    for i in list_edge:
        for j in range(k):
            edge_pair = []
            for m in i:
                edge_pair.append(-((m-1)*k + j+1))
            constraint_lst.append(edge_pair)
    return constraint_lst

def make_constraints(variable_list,k,type):
    if type == 'exactly_one':
        constraints = ''
        for i in variable_list:
            for j in i:
                constraints = constraints + str(j) + ' '
            constraints = constraints + '0' + '\n'
        return constraints
    elif type == 'at_most_one':
        constraints = ''
        for i in range(len(variable_list)-1):
            constraints = constraints + '-' + str(variable_list[i]) + '\n'
        constraints = constraints + '-' + str(variable_list[len(variable_list)-1]) + ' 0' + '\n'
        return constraints
    else:
        constraints = ''
        edge_vars = edge_list(variable_list,k)
        for i in edge_vars:
            for j in i:
                constraints = constraints + str(j) + ' '
            constraints = constraints + '0' + '\n'
        return constraints

def make_ice_breaker_sat(graph, k):
    n = nodes(graph)
    e = edges(graph)
    variable_list = variables(n,k)
    N = len(graph)
    CNF_constraints = ''
    CNF_constraints = CNF_constraints + make_constraints(variable_list,k,'exactly_one')
    for i in variable_list:
        CNF_constraints = CNF_constraints + make_constraints(i,k,'at_most_one')
    CNF_constraints = CNF_constraints + make_constraints(e,k,'diff_one')
    first_line = 'c Ice Breaker Revisited problem (sat)'
    number_lines = CNF_constraints.count(' 0')
    second_line = 'p cnf ' + str(k*N) + ' ' + str(number_lines) + '\n'
    CNF_constraints = first_line + '\n' + second_line + CNF_constraints
    return CNF_constraints

def team_count(solution,k):
	group_lst = []
	for i in solution:
		if i > 0:
			group_lst.append((i%k)+1)
	return group_lst

def read_file():
	f = open('out','r')
	return f.read()

def run_able():
	try:
		subprocess.run(['minisat','satContraint.txt','out'])
	except:
		return False
	return True

def find_min_teams(graph):
    for i in range (1, len(graph)+1):
        cnf_constr = make_ice_breaker_sat(graph,i)
        f = open("satContraint.txt","w+")
        f.write(cnf_constr)
        f.close()
        if(run_able()):
            solution = read_file()
            a = solution.split()
            solution_list = []
            if a[0] == 'UNSAT':
                print('Unsat with k = ' + str(i))
            else:
                solution_list = list(map(int,a[1:-1]))
                print('Minimum number of teams' + str(max(team_count(solution_list,i))))
                return max(team_count(solution_list,i))

def run_q3(n):
    time_record_big =[]
    team_record_big = []
    for n in range (5):
        time_record = []
        team_record  = []
        graphs = [rand_graph(n, 0.1), rand_graph(n, 0.2), rand_graph(n, 0.3), rand_graph(n, 0.4), rand_graph(n, 0.5),rand_graph(n, 0.6),rand_graph(n, 0.7),rand_graph(n, 0.8),rand_graph(n, 0.9)]
        for j in range(len(graphs)):
            start_time = time.time()
            min_teams = find_min_teams(j)
            elapsed_time = time.time() - start_time
            time_record.append(elapsed_time)
            team_record.append(min_teams)
        time_record_big.append(time_record)
        team_record_big.append(team_record)
        

# g = {0: [1, 2,3], 1: [0], 2: [0,4], 3: [0],4:[2]} 
# print(edges(g))
# print(variables(nodes(g),8))
# print(G.graph_dict)
# print(get_edges(g))
# print(make_ice_breaker_sat(g, 4))
g = {0: [1, 2,3], 1: [0], 2: [0,4], 3: [0],4:[2]} 
print(find_min_teams(g))
# print(edges(g))
# print(edge_vars(edges(g),4))
