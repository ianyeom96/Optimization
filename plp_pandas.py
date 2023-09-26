
import pulp
import pandas as pd


def main():


    #Pandas offers special kinds of data structures called DataFrame (two-dimensional) and Series (one-dimensional)

    #DataFrame for the assignment cost
    #index_col =0 means that column 0 is used as row label
    ac_df=pd.read_excel('LAGD_WLP.xlsx', sheet_name='assign_cost', index_col =0)
    #Series for the opening cost
    #squeeze="True": If the parsed data only contains one column then return a Series
    oc_df=pd.read_excel('LAGD_WLP.xlsx', sheet_name='f_cost', index_col=0,  squeeze="True")

    #to_dict converts the data frame/series to a dictionary


    #orient=‘index’ : dict like {index -> {column -> value}}
    assignment_cost=ac_df.to_dict(orient="index")
    opening_cost=oc_df.to_dict()


    #to_list returns a list
    #taken from index (row) label
    potFacilities=ac_df.index.tolist()

    #taken from columns label
    demandPoints=ac_df.columns.tolist()



    #model
    #create object that represents the specific instance of the model
    plp = pulp.LpProblem (" The plant location problem ", pulp.LpMinimize ) # problem

    #variables
    y = pulp.LpVariable.dicts ("y",( potFacilities),0, 1 , pulp.LpBinary )
    x = pulp.LpVariable.dicts ("x",( potFacilities, demandPoints ),0, 1 , pulp.LpBinary )

    #add objective
    #The objective function is logically entered first, with an important comma , at the end of the statement and a short string explaining what this objective function is:
    plp += pulp.lpSum (opening_cost[i] *y[i] for i in potFacilities)+  pulp.lpSum(assignment_cost [i][j] * x[i][j] for i in potFacilities for j in demandPoints )," objective function "


    #add constraints
    for j in demandPoints :
        plp += pulp.lpSum(x[i][j] for i in potFacilities ) == 1,f"satisfy demand {j}"
    for j in demandPoints:
        for i in potFacilities:
            plp += x[i][j] <= y[i] ,f"serve from existing facilities {i}-{j}"


    #optional: generate an lp file
    plp.writeLP ("plp.lp")

    #solve with default solver
    plp.solve()


    #solver=pulp.CPLEX_CMD()
    #plp.solve(solver)



    #solution output
    print(" Status:",pulp.LpStatus[plp.status ])
    print(" objective  value: ",pulp.value(plp.objective ))



    for  var in  plp.variables():
        if var.varValue >0:
            print(var.name ,"=", var.varValue)




if __name__ == '__main__':
    main()
