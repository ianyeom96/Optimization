#-------------------------------------------------------------------------------
# Name:       plant location problem
# Purpose:
#
# Author:      vhemmelm
#
# Created:     11.10.2022
# Copyright:   (c) vhemmelm 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pulp


def main():


    #section for data
    potFacilities=["A", "B", "C", "D", "E"]
    demandPoints=[0,1,2,3,4,5,6]
    fixed_cost={"A": 5, "B": 7, "C": 5, "D":6, "E": 5}
    variable_cost={'A': {0: 1, 1: 2, 2: 10, 3: 9, 4: 6, 5: 7, 6: 3},
    'B': {0: 2, 1: 9, 2: 0, 3: 7, 4: 3, 5: 6, 6: 10},
    'C': {0: 7, 1: 6, 2: 1, 3: 5, 4: 3, 5: 10, 6: 5},
    'D': {0: 6, 1: 5, 2: 10, 3: 2, 4: 6, 5: 3, 6: 6},
    'E': {0: 6, 1: 4, 2: 6, 3: 3, 4: 7, 5: 2, 6: 6}}


    #model
    #create object that represents the specific instance of the model
    plp = pulp.LpProblem (" The plant location problem ", pulp.LpMinimize ) # problem

    #variables
    y = pulp.LpVariable.dicts ("y",( potFacilities),0, 1 , pulp.LpBinary )
    x = pulp.LpVariable.dicts ("x",( potFacilities, demandPoints ),0, 1 , pulp.LpBinary )

    #add objective
    #The objective function is logically entered first, with an important comma , at the end of the statement and a short string explaining what this objective function is:
    plp += pulp.lpSum (fixed_cost[i] *y[i] for i in potFacilities)+  pulp.lpSum(variable_cost [i][j] * x[i][j] for i in potFacilities for j in demandPoints )," objective function "


    #add constraints
    for j in demandPoints :
        plp += pulp.lpSum(x[i][j] for i in potFacilities ) == 1,f"satisfy demand {j}"
    for j in demandPoints:
        for i in potFacilities:
            plp += x[i][j] <= y[i] ,f"serve from existing facilities {i}{j}"


    #optional: generate an lp file
    plp.writeLP ("plp.lp")

    #solve with default solver
    plp.solve()



    #solution output
    print(" Status:",pulp.LpStatus[plp.status ])
    print(" objective  value: ",pulp.value(plp.objective ))



    for  var in  plp.variables():
        #if var.varValue >0:
            print(var.name ,"=", var.varValue)




if __name__ == '__main__':
    main()
