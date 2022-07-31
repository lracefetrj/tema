import ngraspcc as model

# - the available packages:  n1-standard-2-d, n1-standard-4-d, n1-standard-8-d, n1-standard-2, n1-standard-4, n1-standard-8, 
# n1-highmem-2-d, n1-highmem-4-d, n1-highmem-8-d, n1-highmem-2, n1-highmem-4, n1-highmem-8, 
# n1-highcpu-2-d, n1-highcpu-4-d, n1-highcpu-8-d, n1-highcpu-2, n1-highcpu-4, n1-highcpu-8
# the package types number
P = 18

# Gflops of each package type, considering CPU Xeon E5-2670 2.6GHz with 8 cores (~ 4 x CPU Core i3-2120T 2.6GHz with 2 cores)
GF = [41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4]
GF = [vlr * 3600 for vlr in GF]

# GBs of RAM of each package type
MC = [7.5, 15, 30, 7.5, 15, 30, 13, 26, 52, 13, 26, 52, 1.8, 3.6, 7.2, 1.8, 3.6, 7.2]

# GBs of disk (HD) of each package type
DS = [870, 1770, 3540, 0, 0, 0, 870, 1770, 3540, 0, 0, 0, 870, 1770, 3540, 0, 0, 0] 

# the price per time unit of each package type
C = [0.276, 0.552, 1.104, 0.240, 0.480, 0.960, 0.318, 0.636, 1.272, 0.254, 0.508, 1.016, 0.17, 0.34, 0.68, 0.136, 0.272, 0.544]

# - the client requirements:
# the maximum cost that the client can pay
Cmax = 1950

# Buckets
B = 1

# the minimum Gflops that the client's aplication need by bucket
gf = [230342400]

# the total RAM memory (GBs) that the client's aplication need by bucket
mc = [213.5]

# the maximum disk capacity (GBs) that the client's aplication need by bucket
ds = [142.3]

# the maximum package number by bucket
v = [20]

# the maximum time (per time unit:hour)
Tmax = 60

# the maximum package number that it can be utilized
Vmax = 20

# Peso (alpha1 + alpha2 = 1)
alpha1 = 0.5
alpha2 = (1 - alpha1) 

model.solucionar(P, GF, MC, DS, C, B, gf, mc, ds, v, Cmax, Vmax, Tmax, alpha1, alpha2, __file__)