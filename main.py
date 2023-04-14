from ortools.algorithms import pywrapknapsack_solver
import os
import glob
import time

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Đọc giá trị capacity
        capacity = int(lines[2])
        # Đọc giá trị values và weights
        values = []
        weights = []
        for line in lines[4:]:
            value, weight = map(int, line.split())
            values.append(value)
            weights.append(weight)
        return values, weights, capacity
    
def solve(values, weights, capacity):
    start_time = time.time()
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_SCIP_MIP_SOLVER, 'Knapsack')
    solver.set_time_limit(timeout)

    solver.Init(values, [weights], [capacity])
    total_value = solver.Solve()
    total_weight = sum([weights[x] for x in range(0, len(weights)) if solver.BestSolutionContains(x)])
    processing_time = time.time() - start_time

    return total_value, total_weight, processing_time

def main():
    global timeout 
    timeout = 300
    
    files_path = glob.glob(r'kplib-master\09*\n0[0-1]*\*\*.kp')
    result_path = r'SCIP result\09test.csv'

    # Uncomment this code to create new file
    with open(result_path, "w") as f:
        f.write("class,n,R,s,totalValue,totalWeight,processingTime")

    # Uncomment this code to append existing file
    # last_file_path =  r'kplib-master\09SpannerStronglyCorrelated\n00500\R10000\s006.kp'
    # i = files_path.index(last_file_path)
    # files_path = files_path[i+1:]

    for file_path in files_path:
        values, weights, capacity = read_data(file_path)
        total_value, total_weight, processing_time = solve(values, weights, capacity)
        
        with open(result_path, 'a') as f:
            path_split = file_path.split('\\')
            f.write(f'\n{path_split[1]},{path_split[2]},{path_split[3]},{path_split[4]},{total_value},{total_weight},{processing_time}')
    print('Completed')

    # values, weights, capacity = read_data(r'kplib-master\00Uncorrelated\n00050\R01000\s094.kp')
    # total_value, total_weight, processing_time = solve(values, weights, capacity)
        
    # print(total_value, total_weight, processing_time)

if __name__ == '__main__':
    main()
