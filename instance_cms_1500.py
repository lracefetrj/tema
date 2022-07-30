import ngraspcc as model

P = 3

GF = {}
GF[0] = (93.856   * 3600)
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

B = 1

ds = {}
ds[0] = 30
ds[1] = 10

mc = {}
mc[0] = 2250
mc[1] = 24

gf = {}
gf[0] = 324000000
gf[1] = 3000

v = {}
v[0] = 45
v[1] = 10

Cmax = 2592
Tmax = 24
Vmax = 45

alpha1 = 0.5
alpha2 = 0.5

model.solucionar(P, GF, MC, DS, C, B, gf, mc, ds, v, Cmax, Vmax, Tmax, alpha1, alpha2, __file__)