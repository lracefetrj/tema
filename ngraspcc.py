#!/usr/bin/env python3.7

# Copyright 2022, Gurobi Optimization, LLC

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#        x, y, z binary

import gurobipy as gp
from gurobipy import GRB

try:
    B = 2
    T = 20
    P = 3
    Vmax = 4

    C = {}
    C[0] = 0.5
    C[1] = 1.2
    C[2] = 0.8

    D = {}
    D[0] = 5
    D[1] = 2
    D[2] = 8
    
    Cmax = 5
    Dmax = 20
    Tmax = 10

    # Create a new model
    m = gp.Model("graspcc")

    # Create variables
    x_pitb = {}
    for p in range(P):
        for i in range(Vmax):
            for t in range(T):
                for b in range(B):
                    x_pitb[p,i,t,b] = m.addVar(obj=1,  vtype=gp.GRB.BINARY, name='x_' + str(p) + '_' + str(i) + '_' + str(t) + '_' + str(b) )

    # Set objective
    objective = gp.quicksum(x_pitb[p,i,t,b] * C[p] for b in range( B) for t in range( T) for i in range( Vmax) for p in range( P))

    m.ModelSense = gp.GRB.MAXIMIZE
    m.setObjective(objective)

    # Add constraint: Cost
    m.addConstr(gp.quicksum(x_pitb[p,i,t,b] * C[p] for b in range(B) for t in range(T) for i in range(Vmax) for p in range(P)) <= Cmax, "Cost")

    # Add constraint: Time
    for t in range(T):
        m.addConstr(gp.quicksum(x_pitb[p,i,t,b] for b in range(B) for i in range(Vmax) for p in range(P)) <= Tmax, "Time")
 
    # Add constraint: Storage
    for t in range(T):
        for b in range(B):
            m.addConstr(
                gp.quicksum(
                    x_pitb[p,i,t,b] * D[p] for i in range(Vmax) for p in range(P)
                )
                    <= 
                gp.quicksum(
                    Dmax * x_pitb[pp,ii,t,b] for ii in range(Vmax) for pp in range(P)
                ), "Storage")

    # Optimize model
    m.update()
    m.optimize()

    for v in m.getVars():
        print('%s %s' % (v.VarName, v.X))

    print('Obj: %g' % m.ObjVal)

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
