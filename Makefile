# Copyright 2022, Gurobi Optimization, LLC

PLATFORM = linux64
TWOUP    = ..
KEEPTU   = ../..
INC      = /home/lalvarenga/gurobi952/linux64/include/
CPP      = g++
CARGS    = -m64 -O
CPPLIB   = -L/home/lalvarenga/gurobi952/linux64/lib -lgurobi_c++cpl -lgurobi95

all: ngraspcc_c++

run: run_cpp

run_cpp: run_ngraspcc

ngraspcc_c++: ngraspcc.cpp
	$(CPP) $(CARGS) -o $@ $< -I$(INC) $(CPPLIB) -lm

run_ngraspcc: ngraspcc_c++
	./ngraspcc_c++

clean:
	rm -rf *.o *_c++ *.log *.sol
