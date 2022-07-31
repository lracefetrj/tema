#include "gurobi_c++.h"
using namespace std;

void printSolution(GRBModel& model, int nCategories, int nFoods,
                   GRBVar* buy, GRBVar* nutrition);

int
main(int argc,
     char *argv[])
{

  GRBEnv* env = 0;

  try
  {

    const unsigned int P = 18;
    const unsigned int B = 1;
    const unsigned int Vmax = 20;
    const unsigned int Tmax = 60;

    const double Cmax = 1950.0;

    double alpha1, alpha2;
    alpha1 = 0.5;
    alpha2 = 1 - alpha1;

    //# Gflops of each package type, considering CPU Xeon E5-2670 2.6GHz with 8 cores (~ 4 x CPU Core i3-2120T 2.6GHz with 2 cores)
    double GF[] = {41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4, 41.6, 83.2, 166.4};
    for (int j=0; j < (sizeof(GF)/sizeof(GF[0])); j++)
      GF[j] *= 3600;

    //# GBs of RAM of each package type
    const double MC[] = {7.5, 15, 30, 7.5, 15, 30, 13, 26, 52, 13, 26, 52, 1.8, 3.6, 7.2, 1.8, 3.6, 7.2};

    //# the price per time unit of each package type
    const double C[] = {0.276, 0.552, 1.104, 0.240, 0.480, 0.960, 0.318, 0.636, 1.272, 0.254, 0.508, 1.016, 0.17, 0.34, 0.68, 0.136, 0.272, 0.544};

    //# GBs of disk (HD) of each package type
    const double DS[] = {870, 1770, 3540, 0, 0, 0, 870, 1770, 3540, 0, 0, 0, 870, 1770, 3540, 0, 0, 0};


    //# the maximum disk capacity (GBs) that the client's aplication need by bucket
    const double ds[] = {142.3};

    //# the minimum Gflops that the client's aplication need by bucket
    const double gf[] = {230342400.0};

    //# the total RAM memory (GBs) that the client's aplication need by bucket
    const double mc[] = {213.5};

    //# the maximum package number by bucket
    const int v[] = {20};

    // Model
    env = new GRBEnv();
    GRBModel model = GRBModel(*env);
    model.set(GRB_StringAttr_ModelName, "ngraspcc");

    // Create decision variables
    GRBVar x_pitb[P][Vmax][Tmax][B];
    for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
            for (int t = 0; t < Tmax; t++)
                for (int b = 0; b < B; b++) 
                    x_pitb[p][i][t][b] = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "x_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t) + "_" + to_string(b));
                
    GRBVar z = model.addVar(0, GRB_INFINITY, 0, GRB_INTEGER, "z");

    GRBLinExpr C27 = 0;
    for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
            for (int t = 0; t < Tmax; t++)
                for (int b = 0; b < B; b++) 
                    C27 += (x_pitb[p][i][t][b] * C[p]);

    // Set objective
    GRBLinExpr objective = alpha1 * C27 + alpha2 * z;

    model.setObjective(objective, GRB_MINIMIZE);

    // #Add constraint: C27
    model.addConstr(C27 <= Cmax, "C27");

    // #Add constraint: C28
    for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
            for (int t = 0; t < Tmax; t++)
                for (int b = 0; b < B; b++) 
                {
                  GRBLinExpr C28 = 0;
                  for (int pp = 0; pp < P; pp++)
                    for (int ii = 0; ii < Vmax; ii++)
                      C28 += (DS[pp] * x_pitb[pp][ii][t][b]);

                  model.addConstr(C28 >= (ds[b] * x_pitb[p][i][t][b]), "C28_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t) + "_" + to_string(b));
                }

    // #Add constraint: C29
    for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
            for (int t = 0; t < Tmax; t++)
                for (int b = 0; b < B; b++) 
                {
                  GRBLinExpr C29 = 0;
                  for (int pp = 0; pp < P; pp++)
                    for (int ii = 0; ii < Vmax; ii++)
                      C29 += (MC[pp] * x_pitb[pp][ii][t][b]);

                  model.addConstr(C29 >= (mc[b] * x_pitb[p][i][t][b]), "C29_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t) + "_" + to_string(b));
                }

    // Add constraint: C30
    for (int b = 0; b < B; b++)
    { 
      GRBLinExpr GFBucket = 0;
      for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
          for (int t = 0; t < Tmax; t++)
            GFBucket += (GF[p] * x_pitb[p][i][t][b]);

      model.addConstr(GFBucket >= gf[b], "C30_" + to_string(b));
    }

    //# Add constraint: C31
    for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
            for (int t = 0; t < Tmax; t++)
                for (int b = 0; b < B; b++)
                {
                  GRBLinExpr C31 = 0;
                  for (int bb = (b+1); bb < B; bb++)
                    for (int ii = 0; ii < i; ii++)
                      C31 += x_pitb[p][ii][t][bb];

                  model.addConstr(C31 <= (1 -  x_pitb[p][i][t][b]), "C31_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t) + "_" + to_string(b));
                } 

    // # Add constraint: C32
    for (int p = 0; p < P; p++)
        for (int i = 0; i < (Vmax-1); i++)
            for (int t = 0; t < Tmax; t++)
            {
                GRBLinExpr C32S = 0;
                GRBLinExpr C32A = 0;
                for (int b = 0; b < B; b++)
                {
                  C32S += x_pitb[p][(i+1)][t][b];
                  C32A += x_pitb[p][i][t][b];
                }
                model.addConstr(C32S <= C32A, "C32_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t));
            }


    //# Add constraint: C33
    for (int t = 0; t < Tmax; t++)
    {
      GRBLinExpr C33 = 0;
      for (int p = 0; p < P; p++)
        for (int i = 0; i < Vmax; i++)
          for (int b = 0; b < B; b++)
            C33 += x_pitb[p][i][t][b];

      model.addConstr(C33 <= Vmax, "C33_" + to_string(t));
    }

    //# Add constraint: C34
    for (int b = 0; b < B; b++)
      for (int t = 0; t < Tmax; t++)
      {
        GRBLinExpr C34 = 0;
        for (int p = 0; p < P; p++)
          for (int i = 0; i < Vmax; i++)
            C34 += x_pitb[p][i][t][b];

        model.addConstr(C34 <= v[b], "C34_" + to_string(t) + "_" + to_string(b));
      }


    // # Add constraint: C35
    for (int p = 0; p < P; p++)
      for (int i = 0; i < Vmax; i++)
        for (int t = 0; t < Tmax; t++)
        {
          GRBLinExpr C35 = 0;
          for (int b = 0; b < B; b++)
            C35 += x_pitb[p][i][t][b];
          
          model.addConstr(z >= (t * C35), "C35_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t));
        }


    //# Add constraint: C36
    for (int p = 0; p < P; p++)
      for (int i = 0; i < Vmax; i++)
        for (int t = 0; t < Tmax-1; t++)
            for (int b = 0; b < B; b++)
              model.addConstr(x_pitb[p][i][(t+1)][b] <= x_pitb[p][i][t][b], "C36_" + to_string(p) + "_" + to_string(i) + "_" + to_string(t) + "_" + to_string(b));


    // Solve
    model.update();
    model.optimize();

    model.write("teste.sol"); 

    cout << "z: " << z.get(GRB_DoubleAttr_X) << endl;    
    cout << "Custo: " << C27.getValue() << endl;

  }
  catch (GRBException e)
  {
    cout << "Error code = " << e.getErrorCode() << endl;
    cout << e.getMessage() << endl;
  }
  catch (...)
  {
    cout << "Exception during optimization" << endl;
  }

  delete env;
  return 0;
}

void printSolution(GRBModel& model, int nCategories, int nFoods,
                   GRBVar* buy, GRBVar* nutrition)
{
  if (model.get(GRB_IntAttr_Status) == GRB_OPTIMAL)
  {
    cout << "\nCost: " << model.get(GRB_DoubleAttr_ObjVal) << endl;
    cout << "\nBuy:" << endl;
    for (int j = 0; j < nFoods; ++j)
    {
      if (buy[j].get(GRB_DoubleAttr_X) > 0.0001)
      {
        cout << buy[j].get(GRB_StringAttr_VarName) << " " <<
        buy[j].get(GRB_DoubleAttr_X) << endl;
      }
    }
    cout << "\nNutrition:" << endl;
    for (int i = 0; i < nCategories; ++i)
    {
      cout << nutrition[i].get(GRB_StringAttr_VarName) << " " <<
      nutrition[i].get(GRB_DoubleAttr_X) << endl;
    }
  }
  else
  {
    cout << "No solution" << endl;
  }

}