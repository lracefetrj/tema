import ngraspcclb as model

P = 1  # VM Type
L = 2  # Layers

GF = {} # GFLOPS {vm type}
GF[0] = (100)
GF[1] = (332.8    * 3600)
GF[2] = (1123.856 * 3600)

MC = {} # RAM {vm type}
MC[0] = 10
MC[1] = 60.5
MC[2] = 23

DS = {} # DISK {vm type}
DS[0] = 10
DS[1] = 3360 
DS[2] = 1680

C = {} # COST {vm type}
C[0] = 1
C[1] = 2.4
C[2] = 2.1

B = {} # Bucket {layer}
B[0] = 2
B[1] = 2

ds = {} # DISK {layer, bucket}
ds[0,0] = 20
ds[0,1] = 20
ds[1,0] = 20
ds[1,1] = 20

mc = {} # RAM {layer, bucket}
mc[0,0] = 20
mc[0,1] = 20
mc[1,0] = 20
mc[1,1] = 20

gf = {} # GFLOPS {layer, bucket}
gf[0,0] = 220
gf[0,1] = 220
gf[1,0] = 220
gf[1,1] = 220

v = {} # VM {layer, bucket}
v[0,0] = 2
v[0,1] = 2
v[1,0] = 2
v[1,1] = 2

Cmax = 20 # Max Cost
Tmax = 10 # Max Time
Vmax = 2 # Max VM

alpha1 = 0.5
alpha2 = 0.5

model.solucionar(P, GF, MC, DS, C, B, L, gf, mc, ds, v, Cmax, Vmax, (Tmax+1), alpha1, alpha2, __file__)