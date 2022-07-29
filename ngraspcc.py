#!/usr/bin/env python3.7

import gurobipy as gp
from gurobipy import GRB

try:


    P = 3

    C = {}
    C[0] = 0.3
    C[1] = 0.35
    C[2] = 0.32

    DS = {}
    DS[0] = 4
    DS[1] = 0.7
    DS[2] = 3

    MC = {}
    MC[0] = 3.5
    MC[1] = 3.5
    MC[2] = 8

    GF = {}
    GF[0] = (1.3 * 3600)
    GF[1] = (1.5 * 3600)
    GF[2] = (1.2 * 3600)

    B = 1
    
    ds = {}
    ds[0] = 41
    ds[1] = 10

    mc = {}
    mc[0] = 16
    mc[1] = 24

    gf = {}
    gf[0] = 5067532
    gf[1] = 3000

    v = {}
    v[0] = 10
    v[1] = 10

    Cmax = 1000
    Tmax = 120
    Vmax = 11

    alpha1 = 0.5
    alpha2 = 0.5

    # Create a new model
    m = gp.Model("graspcc")

    # Create variables
    x_pitb = {}
    for p in range(P):
        for i in range(Vmax):
            for t in range(Tmax):
                for b in range(B):
                    x_pitb[p,i,t,b] = m.addVar(vtype=gp.GRB.BINARY, name='x_' + str(p) + '_' + str(i) + '_' + str(t) + '_' + str(b) )

    z = m.addVar(vtype=gp.GRB.INTEGER, name='z')

    # Set objective
    objective = alpha1 * gp.quicksum(
                    x_pitb[p,i,t,b] * C[p] for b in range( B) for t in range(Tmax) for i in range( Vmax) for p in range( P)
                ) + alpha2 * z

    m.ModelSense = gp.GRB.MINIMIZE
    m.setObjective(objective)

    # Add constraint: Cost
    m.addConstr(
            gp.quicksum(
                x_pitb[p,i,t,b] * C[p] for b in range(B) for t in range(Tmax) for i in range(Vmax) for p in range(P)
            ) 
            <= 
            Cmax, "Cost")

    # Add constraint: Disk
    for pp in range(P):
        for ii in range(Vmax):
            for t in range(Tmax):
                for b in range(B):
                    m.addConstr(
                        gp.quicksum(
                            DS[p] * x_pitb[p,i,t,b] for p in range(P) for i in range(Vmax) 
                        )
                        >= 
                        ds[b] * x_pitb[pp,ii,t,b]
                        , "Disk")

#    # Add constraint: Memory
#    for t in range(Tmax):
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
                x_pitb[p,i,t,b] * GF[p] for p in range(P) for i in range(Vmax) for t in range(Tmax)
            )
            >= 
            gf[b], "GFlops")

    # Add constraint: Sucessor
#    for p in range(P):
#        for i in range(Vmax):
#            for t in range(Tmax):
#                for b in range(B):
#                    m.addConstr(
#                        gp.quicksum(
#                            x_pitb[p,ii,t,bb] for ii in range(i) for bb in range(b, B)
#                        )
#                        <= 
#                        (1 - x_pitb[p,i,t,b]) 
#                        , "Sucessor")

#    # Add constraint: PrecursorBucket
#    for p in range(P):
#        for i in range(Vmax-1):
#            for t in range(Tmax):
#                    m.addConstr(
#                        gp.quicksum( x_pitb[p,i+1,t,b] for b in range(B))
#                        <= 
#                        gp.quicksum( x_pitb[p,i,t,b] for b in range(B))
#                        , "PrecursorBucket")

    # Add constraint: MaxVM
    for t in range(Tmax):
        m.addConstr(
            gp.quicksum(
                x_pitb[p,i,t,b] for p in range(P) for i in range(Vmax) for b in range(B)
            )
            <= 
            Vmax, "MaxVM")

    # Add constraint: MaxVMBuckect
#    for b in range(B):
#        for t in range(Tmax):
#            m.addConstr(
#                gp.quicksum(
#                    x_pitb[p,i,t,b] for i in range(i) for p in range(P)
#                )
#                <= 
#                v[b]
#                , "MaxVMBucket")

    # Add constraint: LastVMBucket
    for p in range(P):
        for i in range(Vmax):
            for t in range(Tmax):
                m.addConstr(
                    z >= t * 
                    gp.quicksum(
                        x_pitb[p,i,t,b] for b in range(B)
                    )
                    , "LastVMBucket")

    # Add constraint: Precursor
    for p in range(P):
        for i in range(Vmax-1):
            for t in range(Tmax):
                for b in range(B):
                    m.addConstr(
                        x_pitb[p,i+1,t,b] 
                        <= 
                        x_pitb[p,i,t,b] 
                        , "Precursor")

    # Optimize model
    m.update()
    m.optimize()
    #m.computeIIS()
    #m.write('model.ilp')

    m.write('model.sol') 

#    for v in m.getVars():
#        if v.X > 0:
#            print('%s %s' % (v.VarName, v.X))

    print('Obj: %g' % m.ObjVal)
#
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')
