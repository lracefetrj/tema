#!/usr/bin/env python3.7

import gurobipy as gp
from gurobipy import GRB

try:
    B = 2
    T = 5
    P = 3
    Vmax = 4

    C = {}
    C[0] = 0.5
    C[1] = 1.2
    C[2] = 0.8

    DS = {}
    DS[0] = 3
    DS[1] = 6
    DS[2] = 4

    ds = {}
    ds[0] = 14
    ds[1] = 10
    
    MC = {}
    MC[0] = 2
    MC[1] = 8
    MC[2] = 6

    mc = {}
    mc[0] = 16
    mc[1] = 24

    GF = {}
    GF[0] = 100
    GF[1] = 300
    GF[2] = 200

    gf = {}
    gf[0] = 1000
    gf[1] = 1300


    Cmax = 10
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
                    x_pitb[p,i,t,b] = m.addVar(obj=0,  vtype=gp.GRB.BINARY, name='x_' + str(p) + '_' + str(i) + '_' + str(t) + '_' + str(b) )

    # Set objective
    objective = gp.quicksum(x_pitb[p,i,t,b] * C[p] for b in range( B) for t in range(T) for i in range( Vmax) for p in range( P))

    m.ModelSense = gp.GRB.MINIMIZE
    m.setObjective(objective)

    # Add constraint: Cost
    m.addConstr(gp.quicksum(x_pitb[p,i,t,b] * C[p] for b in range(B) for t in range(T) for i in range(Vmax) for p in range(P)) <= Cmax, "Cost")

    # Add constraint: Time
    m.addConstr(gp.quicksum(x_pitb[p,i,t,b] for b in range(B) for t in range(T) for i in range(Vmax) for p in range(P)) <= Tmax, "Time")
 
#    # Add constraint: Storage
#    for t in range(T):
#        for b in range(B):
#            m.addConstr(
#                gp.quicksum(
#                    x_pitb[p,i,t,b] * DS[p] for i in range(Vmax) for p in range(P)
#                )
#                    >= 
#                gp.quicksum(
#                   x_pitb[pp,ii,t,b] * ds[b] for ii in range(Vmax) for pp in range(P)
#                ), "Storage")

#    # Add constraint: Memory
#    for t in range(T):
#        for b in range(B):
#            m.addConstr(
#                gp.quicksum(
#                    x_pitb[p,i,t,b] * MC[p] for i in range(Vmax) for p in range(P)
#                )
#                    >= 
#                gp.quicksum(
#                    x_pitb[pp,ii,t,b] * mc[b] for ii in range(Vmax) for pp in range(P)
#                ), "Memory")

    # Add constraint: GFlops
    for b in range(B):
        m.addConstr(
            gp.quicksum(
                x_pitb[p,i,t,b] * GF[p] for i in range(Vmax) for p in range(P) for t in range(T)
            )
            >= 
            gf[b], "GFlops")

    # Add constraint: Precursor
    for p in range(P):
        for i in range(Vmax-1):
            for t in range(T):
                for b in range(B):
                    m.addConstr(
                        x_pitb[p,i+1,t,b] 
                        <= 
                        x_pitb[p,i,t,b] 
                        , "Precursor")

    # Add constraint: Sucessor
    for p in range(P):
        for i in range(Vmax):
            for t in range(T):
                for b in range(B):
                    m.addConstr(
                        gp.quicksum(
                            x_pitb[p,ii,t,bb] for ii in range(i) for bb in range(b, B)
                        )
                        <= 
                        (1 - x_pitb[p,i,t,b]) 
                        , "Sucessor")

    # Optimize model
    m.update()
    m.optimize()

    for v in m.getVars():
        print('%s %s' % (v.VarName, v.X))

    print('Obj: %g' % m.ObjVal)
#
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
