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
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'Knapsack')
    solver.set_time_limit(timeout)

    solver.Init(values, [weights], [capacity])
    total_value = solver.Solve()
    total_weight = sum([weights[x] for x in range(0, len(weights)) if solver.BestSolutionContains(x)])
    processing_time = time.time() - start_time

    return total_value, total_weight, processing_time

def main():
    global timeout 
    timeout = 1
    
    files_path = glob.glob(r'kplib-master\00Uncorrelated\*\*\*.kp')
    with open("result.txt", "w") as f:
        f.write("filePath,totalValue,totalWeight,processingTime")

    for file_path in files_path:
        values, weights, capacity = read_data(file_path)
        total_value, total_weight, processing_time = solve(values, weights, capacity)
        
        with open('result.txt', 'a') as f:
            f.write(f'\n{file_path[13:]},{total_value},{total_weight},{processing_time}')
    print('Completed')

    # values, weights, capacity = read_data(r'kplib-master\00Uncorrelated\n00050\R01000\s094.kp')
    # total_value, total_weight, processing_time = solve(values, weights, capacity)
        
    # print(total_value, total_weight, processing_time)
if __name__ == '__main__':
    main()
