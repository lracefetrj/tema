#!/usr/bin/env python3.7
import gurobipy as gp
from gurobipy import GRB


def solucionar(P, GF, MC, DS, C, B, L, gf, mc, ds, v, Cmax, Vmax, Tmax, alpha1, alpha2, arqmodel):

    try:
        M = 1

        # Create a new model
        m = gp.Model("graspcclb")

        # Create variables
        x_pitbl = {}
        for p in range(P):
            for i in range(Vmax):
                for t in range(1,Tmax):
                    for l in range(L):
                        for b in range(B[l]):
                            x_pitbl[p,i,t,b,l] = m.addVar(vtype=gp.GRB.BINARY, name='x_' + str(p) + '_' + str(i) + '_' + str(t) + '_' + str(b) + '_' + str(l))


        z_pi = {}
        for p in range(P):
            for i in range(Vmax):
                z_pi[p,i] = m.addVar(vtype=gp.GRB.INTEGER, name='z_' + str(p) + '_' + str(i))

        z = m.addVar(vtype=gp.GRB.INTEGER, name='z')

        # Set objective
        objective = (alpha1 * gp.quicksum(
                        (z_pi[p,i] * C[p] for p in range(P) for i in range(Vmax))
                    ) / Cmax) + (alpha2 * (z / Tmax))

        m.ModelSense = gp.GRB.MINIMIZE
        m.setObjective(objective)

        # Add constraint: C40
        j = 0
        for pp in range(P):
            for ii in range(Vmax):
                for t in range(1,Tmax):
                    for l in range(L):
                        for b in range(B[l]):
                            j += 1
                            m.addConstr(
                                gp.quicksum(
                                    DS[p] * x_pitbl[p,i,t,b,l] for p in range(P) for i in range(Vmax) 
                                )
                                >= 
                                ds[l,b] * x_pitbl[pp,ii,t,b,l]
                                , "C40_" + str(j))


        # Add constraint: C41
        j = 0
        for pp in range(P):
            for ii in range(Vmax):
                for t in range(1,Tmax):
                    for l in range(L):
                        for b in range(B[l]):
                            j += 1
                            m.addConstr(
                                gp.quicksum(
                                    MC[p] * x_pitbl[p,i,t,b,l] for p in range(P) for i in range(Vmax) 
                                )
                                >= 
                                mc[l,b] * x_pitbl[pp,ii,t,b,l]
                                , "C41_" + str(j))


        # Add constraint: C42
        j = 0
        for l in range(L):
            for b in range(B[l]):
                j += 1
                m.addConstr(
                    gp.quicksum(
                        x_pitbl[p,i,t,b,l] * GF[p] for p in range(P) for i in range(Vmax) for t in range(1,Tmax)
                    )
                    >= 
                    gf[l,b]
                    , "C42_" + str(j))

        # Add constraint: C43
        j = 0
        for p in range(P):
            for i in range(Vmax):
                for t in range(1,Tmax):
                    for l in range(L):
                        for b in range(B[l]):
                            j += 1
                            m.addConstr(
                                gp.quicksum(
                                    x_pitbl[p,ii,t,bb,l] for ii in range(i) for bb in range((b+1), B[l])
                                )
                                <= 
                                (1 - x_pitbl[p,i,t,b,l]) * M
                                , "C43_" + str(j))                    

        # Add constraint: C44
        j = 0
        for p in range(P):
            for i in range(Vmax-1):
                for t in range(1,Tmax):
                        j += 1
                        m.addConstr(
                            gp.quicksum( x_pitbl[p,i+1,t,b,l] for l in range(L) for b in range(B[l]))
                            <= 
                            gp.quicksum( x_pitbl[p,i,t,b,l] for l in range(L) for b in range(B[l]))
                            , "C44_" + str(j))


        # Add constraint: C45
        j = 0
        for p in range(P):
           for i in range(Vmax):
               for t in range(1,Tmax):
                   for l in range(L):
                       for b in range(B[l]):
                           j += 1
                           m.addConstr(
                               gp.quicksum(
                                   x_pitbl[pp,ii,tt,bb,ll] for pp in range(P) for ii in range(Vmax) for tt in range(1,t+1) for ll in range(l+1, L) for bb in range(B[ll]) 
                               )
                               <= 
                               (1 - x_pitbl[p,i,t,b,l]) * M
                               , "C45_" + str(j))

        # Add constraint: C46
        j = 0
        for t in range(1,Tmax):
            j += 1
            m.addConstr(
                gp.quicksum(
                   x_pitbl[p,i,t,b,l] for p in range(P) for i in range(Vmax) for l in range(L) for b in range(B[l])
                )
                <= 
                Vmax, "C46_" + str(j))

        # Add constraint: C47
        j = 0
        for t in range(1,Tmax):
            for l in range(L):
                for b in range(B[l]):
                    j += 1
                    m.addConstr(
                        gp.quicksum(
                            x_pitbl[p,i,t,b,l] for p in range(P) for i in range(Vmax) 
                        )
                        <= 
                        v[l,b]
                        , "C47_" + str(j))

        # Add constraint: C48
        j = 0
        for p in range(P):
            for i in range(Vmax):
                for t in range(1,Tmax):
                    j += 1
                    m.addConstr(
                        z_pi[p,i] >= (t * 
                        gp.quicksum(
                            x_pitbl[p,i,t,b,l] for l in range(L) for b in range(B[l])
                        ))
                        , "C48_" + str(j))
                        
        # Add constraint: C49
        j = 0
        for p in range(P):
            for i in range(Vmax):
                    j += 1
                    m.addConstr(
                        z >= z_pi[p,i]
                        , "C49_" + str(j))


        # Add constraint: C50
        C50 = gp.quicksum(
            C[p] * z_pi[p,i] for i in range(Vmax) for p in range(P)
        )

        m.addConstr(C50 <= Cmax, "C50")                        

        # Optimize model
        m.update()
        m.optimize()
        # m.computeIIS()
        # m.write('model.ilp')
        # print(m.display())
        m.write(arqmodel + '.sol') 
        m.write(arqmodel + '.lp') 

        print('Custo: %g' % (C50.getValue()))

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')
