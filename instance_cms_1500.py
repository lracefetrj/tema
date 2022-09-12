import ngraspcclb as model

P = 1
L = 2

GF = {}
GF[0] = (100      * 3600)
GF[1] = (332.8    * 3600)
GF[2] = (1123.856 * 3600)

MC = {}
MC[0] = 23
MC[1] = 60.5
MC[2] = 23

DS = {}
DS[0] = 1680
DS[1] = 3360 
DS[2] = 1680

C = {}
C[0] = 1.3
C[1] = 2.4
C[2] = 2.1

B = {}
B[0] = 1
B[1] = 1

ds = {}
ds[0,0] = 1000
ds[1,0] = 1000

mc = {}
mc[0,0] = 30
mc[1,0] = 30

gf = {}
gf[0,0] = 370000
gf[1,0] = 370000

v = {}
v[0,0] = 10
v[1,0] = 10

Cmax = 5000
Tmax = 4
Vmax = 4

alpha1 = 0.5
alpha2 = 0.5

model.solucionar(P, GF, MC, DS, C, B, L, gf, mc, ds, v, Cmax, Vmax, (Tmax+1), alpha1, alpha2, __file__)