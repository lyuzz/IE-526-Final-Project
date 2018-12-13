"""
The model is defined here.
"""

# importing
import time
import cplex
import pandas as pd

def model(customer_data, dist_time_data, c_f, c_d, c_w, t_un, D_max, W_max, V_max, T_thr, K):
    """model"""

    # collecting time
    start_time = time.time()

    # Basic settings
    c = cplex.Cplex()
    c.objective.set_sense(c.objective.sense.minimize)
    c.parameters.simplex.display.set(2)     # solving process report
    c.parameters.read.datacheck.set(1)      # checking consistency of data, better use it when testing model.
    
    # LP setting
    # c.parameters.lpmethod.set(c.parameters.lpmethod.values.primal)    # method used when solving lp
    
    # MIP setting
    c.parameters.mip.strategy.nodeselect.set(2)     # how to select node, see manual.
    
    # Memory settings
    c.parameters.emphasis.memory.set(1)
    c.parameters.mip.strategy.file.set(3)       # save tree nodes in a disk file, to save memory.
    c.parameters.workmem.set(6144)              # working memory, set to 6 GB.
    
    # Time setting
    # c.parameters.timelimit.set(3600)      # time limit

    # vehicle set
    vehicle = list(range(1, K + 1, 1))

    # Adding variables
    # x^k_ij: whether an edge (i, j) is chosen for vehicle k;
    print("Adding variables...")
    
    # x^k_ij.
    for k in vehicle:
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][0:]:
                if i == 0 and i != j:      # adding routes coming from origin
                    expr = 'from_node == 0 & to_node == ' + str(j)
                    c.variables.add(
                        obj = [c_f + c_d * dist_time_data.query(expr)['distance'].iloc[0]],
                        lb = [0.0],
                        ub = [1.0],
                        names = ['x.' + str(k) + '.0.' + str(j)],
                        types = "I"
                    )
                if i != 0 and i != j:      # adding other routes
                    expr = 'from_node == ' + str(i) + ' & to_node == ' + str(j)
                    c.variables.add(
                        obj = [c_d * dist_time_data.query(expr)['distance'].iloc[0]],
                        lb = [0.0],
                        ub = [1.0],
                        names = ['x.' + str(k) + '.' + str(i) + '.' + str(j)],
                        types = "I"
                    )    
    
    # Now y_i
    for i in customer_data['ID']:
        c.variables.add(
            obj = [c_w],
            lb = [0.0],
            names = ["y." + str(i)],
            types = "C"
        )
    print("All variables added.")

    # Adding constraints. According to report.pdf
    # (2.2)
    print("Adding Constraints...")
    print("(2.2)...")
    for k in vehicle:
        ind = [
            'x.' + str(k) + '.0.' + str(j)
            for j in customer_data['ID'][1:]
        ]
        val = [1.0] * len(customer_data['ID'][1:])
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "E",
            rhs = [1.0]
        )
        del ind, val

    # (2.3)'
    print("(2.3)...")
    for k in vehicle:
        ind = [
            'x.' + str(k) + '.' + str(i) + '.0'
            for i in customer_data['ID'][1:]
        ]
        val = [1.0] * len(ind)
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "E",
            rhs = [1.0]
        )
        del ind, val
    
    # (2.4)
    print("(2.4)...")
    for j in customer_data['ID'][1:]:
        ind = []
        for k in vehicle:
            for i in customer_data['ID'][0:]:
                if i != j:
                    ind.append('x.' + str(k) + '.' + str(i) + '.' + str(j))
        val = [1.0] * len(ind)
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "E",
            rhs = [1.0]
        )
        del ind, val
    
    # (2.5)
    print("(2.5)...")
    for k in vehicle:
        for j in customer_data['ID'][1:]:
            for i in customer_data['ID'][0:]:
                if i != j:
                    ind = []
                    if i == 0:
                        for h in customer_data['ID'][0:]:
                            if h != j:
                                ind.append('x.' + str(k) + '.' + str(j) + '.' + str(h))
                    else:
                        for h in customer_data['ID'][0:]:
                            if h != i and h != j:
                                ind.append('x.' + str(k) + '.' + str(j) + '.' + str(h))
                    val = [1.0] * len(ind)
                    ind.append('x.' + str(k) + '.' + str(i) + '.' + str(j))
                    val.append(-1.0)
                    c.linear_constraints.add(
                        lin_expr = [cplex.SparsePair(
                            ind = ind,
                            val = val
                        )],
                        senses = "G",
                        rhs = [0.0]
                    )
                    del ind, val
    
    # (2.6)
    print("(2.6)...")
    for k in vehicle:
        ind = []
        val = []
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][0:]:
                if i != j:
                    ind.append('x.' + str(k) + '.' + str(i) + '.' + str(j))
                    expr = 'from_node == ' + str(i) + ' & to_node == ' + str(j)
                    val.append(dist_time_data.query(expr)['distance'].iloc[0])
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "L",
            rhs = [D_max]
        )
        del ind, val
    
    # (2.7)
    print("(2.7)...")
    for k in vehicle:
        ind = []
        val = []
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][1:]:
                if i != j:
                    ind.append('x.' + str(k) + '.' + str(i) + '.' + str(j))
                    expr = 'ID == ' + str(j)
                    val.append(customer_data.query(expr)['pack_total_weight'].iloc[0])
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "L",
            rhs = [W_max]
        )
        del ind, val
    
    # (2.8)
    print("(2.8)...")
    for k in vehicle:
        ind = []
        val = []
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][1:]:
                if i != j:
                    ind.append('x.' + str(k) + '.' + str(i) + '.' + str(j))
                    expr = 'ID == ' + str(j)
                    val.append(customer_data.query(expr)['pack_total_volume'].iloc[0])
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "L",
            rhs = [V_max]
        )
        del ind, val
    
    # (2.9)
    print("(2.9)...")
    M = 1000
    for k in vehicle:
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][1:]:
                if i != j:
                    ind = [
                        'x.' + str(k) + '.' + str(i) + '.' + str(j),
                        'y.' + str(j),
                        'y.' + str(i)
                    ]
                    val = [
                        -1.0 * M,
                        1.0,
                        -1.0
                    ]
                    expr = 'from_node == ' + str(i) + ' & to_node == ' + str(j)
                    c.linear_constraints.add(
                        lin_expr = [cplex.SparsePair(
                            ind = ind,
                            val = val
                        )],
                        senses = "G",
                        rhs = [
                            t_un + dist_time_data.query(expr)['travel_time'].iloc[0] - M
                        ]
                    )
                    del ind, val
    
    # (2.10)
    print("(2.10)...")
    for i in customer_data['ID'][1:]:
        ind = ['y.' + str(i)]
        val = [1.0]
        expr = 'from_node == ' + str(i) + ' & to_node == 0'
        c.linear_constraints.add(
            lin_expr = [cplex.SparsePair(
                ind = ind,
                val = val
            )],
            senses = "L",
            rhs = [T_thr - t_un - dist_time_data.query(expr)['travel_time'].iloc[0]]
        )
        del ind, val
    
    # solving
    print("Constraints added.")
    print("Start solving...")
    file_name = "solution_{}.txt"
    file = open(file_name.format(K), "w+")
    file.write("\nNUMBER OF VEHICLES = " + str(K) + "\n\n")
    c.set_results_stream(file)
    c.solve()

    # printing to file
    file.write("\nModel runtime = " + str(time.time() - start_time) + "\n\n")
    file.write("Solution Status = " + str(c.solution.status[c.solution.get_status()]) + "\n")
    file.write("Optimal value = %f\n" % c.solution.get_objective_value())
    index = 0
    x = c.solution.get_values()
    line = "x.{}.{}.{} = {}\n"
    line_y = "y.{} = {}\n"
    for k in vehicle:
        for i in customer_data['ID'][0:]:
            for j in customer_data['ID'][0:]:
                if i != j:
                    if x[index] > 0:
                        file.write(line.format(k, i, j, x[index]))
                    index = index + 1
    for i in customer_data['ID'][0:]:
        file.write(line_y.format(i, x[index]))
        index = index + 1
    file.close()

    print("\n Seccessful run.\n")
    
    return 0
