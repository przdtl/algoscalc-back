from typing import Union

import numpy as np


class SimplexModel:
    """Implement the linear programming problem in tableau form.
    Parameters:
        - tableau: a numpy array representing the tableau on which perform operations
        - basic_var: a list of initial basic variables
        - integer: a boolean value indicating if the solution has to be integer

    Attributes:
        - tableau: the current tableau
        - basic_var: a numpy array containing indexes of the current basic variables
        - integer: a boolean value indicating if the solution has to be integer
        - solution: an array representing the final solution if exists
        - z: the optimal value if exists
        - optimal: boolean value if the tableau is in optimal form
        - unbounded: boolean value
        - infeasible: boolean value"""

    def __init__(self, tableau, basic_var, integer=False):
        self.tableau = tableau
        self.basic_var = basic_var
        self.integer = integer
        self.solution = []
        self.z = 0
        self.optimal = False
        self.unbounded = False
        self.infeasible = False

    def get_solution(self):
        if self.solution != None:
            return (self.solution, self.z,)
        elif self.unbounded:
            raise ValueError('Эта таблица бесконечна')
        elif self.infeasible:
            raise ValueError('Решения нет')

    # parameters: tableau, index t of the row, index h of the column
    def pivot_operation(self, t, h):
        '''
        Performs the pivot operations of the cell represented by the input values for row t and column h
        '''
        tableau = self.tableau
        # shape of the tableau
        m = tableau.shape[0]
        n = tableau.shape[1]
        pivot = tableau[t][h]
        # divide the pivot row by the pivot element
        for i in range(n):
            tableau[t][i] /= pivot
        # update all the other rows
        save = pivot
        for i in range(m):
            if i != t and tableau[i][h] != 0:
                save = tableau[i][h]
                for j in range(n):
                    tableau[i][j] -= save * tableau[t][j]

    def primal_simplex_method(self):
        '''
        Solve the model using the primal simplex method in tableau form.
        '''
        tableau = self.tableau
        beta = self.basic_var

        # number of rows in the tableau
        m = tableau.shape[0]
        # number of columns in the tableau
        n = tableau.shape[1]

        # final cases
        unbounded = False
        optimal = False

        while optimal == False and unbounded == False:
            # get the vector of costs
            costs = [tableau[0][c] for c in range(1, n)]
            # verify if all the costs are >= 0, thus the tableau is in optimal form
            if all(c >= 0 for c in costs):
                optimal = True
                break
            else:
                # index of the non basic variable
                h = 0
                # Find the first cost < 0 and choose a non basic variable
                for i, c in enumerate(tableau[0]):
                    if i != 0 and c < 0:
                        h = i
                        # print('Variable of index {} will enter the basis'.format(h))
                        break
                # check if all the a[i, h] are < 0 so the problem is unbounded
                if all(tableau[i, h] < 0 for i in range(m)):
                    unbounded = True
                    break
                else:
                    # choose the variable that will leave the basis
                    min = 100000
                    t = 1
                    for i in range(1, m):
                        if tableau[i][h] > 0 and tableau[i][0] / tableau[i][h] < min:
                            min = tableau[i][0] / tableau[i][h]
                            t = i

                    # pivot operation
                    self.pivot_operation(t, h)

                    # update the vector beta, containing the indices of the basis variables
                    beta[t - 1] = h

        if optimal:
            # solution
            x = [0] * (n - 1)
            for i, b in enumerate(beta):
                x[b - 1] = tableau[i + 1][0]
            self.optimal = True
            self.solution = x
            self.z = -tableau[0][0]
        elif unbounded:
            self.unbounded = True


def main(tableau: list[list[float]], basic_var: list[float]) -> dict[str, Union[list[float], float]]:
    tableau = np.array(tableau)
    basic_var = np.array(basic_var)
    model = SimplexModel(tableau, basic_var)
    model.primal_simplex_method()
    optimal_solution, optimal_value = model.get_solution()
    return {'optimal_solution': optimal_solution, 'optimal_value': optimal_value}


if __name__ == '__main__':
    tableau = [[0., -1., -1., 0., 0.],
               [24., 6., 4., 1., 0.],
               [6., 3., -2., 0., 1.]]
    basic_var = [1, 2]
    print(main(tableau, basic_var))
