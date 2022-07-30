#!/usr/bin/env python3.7
import gurobipy as gp
from gurobipy import GRB


def solucionar(P, GF, MC, DS, C, B, gf, mc, ds, v, Cmax, Vmax, Tmax, alpha1, alpha2, arqmodel):

    try:

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

        # Add constraint: C27
        m.addConstr(
                gp.quicksum(
                    x_pitb[p,i,t,b] * C[p] for b in range(B) for t in range(Tmax) for i in range(Vmax) for p in range(P)
                ) 
                <= 
                Cmax, "C27")

        # Add constraint: C28
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
                            , "C28")

        # Add constraint: C29
        for pp in range(P):
            for ii in range(Vmax):
                for t in range(Tmax):
                    for b in range(B):
                        m.addConstr(
                            gp.quicksum(
                                MC[p] * x_pitb[p,i,t,b] for p in range(P) for i in range(Vmax) 
                            )
                            >= 
                            mc[b] * x_pitb[pp,ii,t,b]
                            , "C29")

        # Add constraint: C30
        for b in range(B):
            m.addConstr(
                gp.quicksum(
                    x_pitb[p,i,t,b] * GF[p] for p in range(P) for i in range(Vmax) for t in range(Tmax)
                )
                >= 
                gf[b], "C30")

        # Add constraint: C31
        for p in range(P):
            for i in range(Vmax):
                for t in range(Tmax):
                    for b in range(B):
                        m.addConstr(
                            gp.quicksum(
                                x_pitb[p,ii,t,bb] for ii in range(i) for bb in range((b+1), B)
                            )
                            <= 
                            (1 - x_pitb[p,i,t,b]) 
                            , "C31")

        # Add constraint: C32
        for p in range(P):
            for i in range(Vmax-1):
                for t in range(Tmax):
                        m.addConstr(
                            gp.quicksum( x_pitb[p,i+1,t,b] for b in range(B))
                            <= 
                            gp.quicksum( x_pitb[p,i,t,b] for b in range(B))
                            , "C32")

        # Add constraint: C33
        for t in range(Tmax):
            m.addConstr(
                gp.quicksum(
                    x_pitb[p,i,t,b] for p in range(P) for i in range(Vmax) for b in range(B)
                )
                <= 
                Vmax, "C33")

        # Add constraint: C34
        for b in range(B):
            for t in range(Tmax):
                m.addConstr(
                    gp.quicksum(
                        x_pitb[p,i,t,b] for p in range(P) for i in range(Vmax) 
                    )
                    <= v[b]
                    , "C34")

        # Add constraint: C35
        for p in range(P):
            for i in range(Vmax):
                for t in range(Tmax):
                    m.addConstr(
                        z >= t * 
                        gp.quicksum(
                            x_pitb[p,i,t,b] for b in range(B)
                        )
                        , "C35")

        # Add constraint: C36
        for p in range(P):
            for i in range(Vmax):
                for t in range(Tmax-1):
                    for b in range(B):
                        m.addConstr(
                            x_pitb[p,i,(t+1),b] 
                            <= 
                            x_pitb[p,i,t,b] 
                            , "C36")

        # Optimize model
        m.update()
        m.optimize()
        #m.computeIIS()
        #m.write('model.ilp')

        m.write(arqmodel + '.sol') 

        cost = gp.quicksum(
                    x_pitb[p,i,t,b] * C[p] for b in range(B) for t in range(Tmax) for i in range(Vmax) for p in range(P)
                )

        print('Custo: %g' % (cost.getValue()))

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')
