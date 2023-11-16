"""
CVXPY Model
"""
import numpy as np
import cvxpy as cp

from .mmt import MMT
from .error import NotSolvable

class CVXPY(MMT):
    """
    A Model class that solves the multi-model transportation optimization problem.
    """
    def build_model(self) -> None:
        """
        overall function to build up model objective and constraints.
        build up the mathematical programming model's objective and constraints using CVXPY framework.
        """
        # 4 dimensional binary decision variable matrix
        self.var = cp.Variable(self.route_num * self.dateSpace * self.goods, boolean=True, name='x')
        self.x = np.zeros((self.portSpace, self.portSpace, self.dateSpace, self.goods)).astype('object')
        self.x[self.var_location] = list(self.var)
        # 3 dimensional container number matrix
        self.var_2 = cp.Variable(self.route_num * self.dateSpace, integer=True, name='y')
        self.y = np.zeros((self.portSpace, self.portSpace, self.dateSpace)).astype('object')
        self.y[self.var_2_location] = list(self.var_2)
        # 3 dimensional route usage matrix
        self.var_3 = cp.Variable(self.route_num * self.dateSpace, boolean=True, name='z')
        self.z = np.zeros((self.portSpace, self.portSpace, self.dateSpace)).astype('object')
        self.z[self.var_3_location] = list(self.var_3)
        # warehouse related cost
        warehouseCost, arrTime, stayTime = self.warehouse_fee(self.x)
        ###objective###
        transportCost = np.sum(self.y * self.tranCost) + np.sum(self.z * self.tranFixedCost)
        transitDutyCost = np.sum(np.sum(np.dot(self.x, self.kValue), axis=2) * self.transitDuty)
        taxCost = np.sum(self.taxPct * self.kValue) + transitDutyCost
        objective = cp.Minimize(transportCost + warehouseCost + taxCost)
        ###constraint###
        constraints = []
        # 1.Goods must be shipped out from its origin to another node and shipped to its destination.
        constraints += [np.sum(self.x[self.kStartPort[k], :, :, k]) == 1 for k in range(self.goods)]
        constraints += [np.sum(self.x[:, self.kEndPort[k], :, k]) == 1 for k in range(self.goods)]
        # 2.For each goods k, it couldn't be shipped out from its destination or shipped to its origin.
        constraints += [np.sum(self.x[:, self.kStartPort[k], :, k]) == 0 for k in range(self.goods)]
        constraints += [np.sum(self.x[self.kEndPort[k], :, :, k]) == 0 for k in range(self.goods)]
        # 3.constraint for transition point
        for k in range(self.goods):
            for j in range(self.portSpace):
                if (j != self.kStartPort[k]) & (j != self.kEndPort[k]):
                    constraints.append(np.sum(self.x[:, j, :, k]) == np.sum(self.x[j, :, :, k]))
        # 4.each goods can only be transitioned in or out of a port for at most once
        constraints += [np.sum(self.x[i, :, :, k]) <= 1 for k in range(self.goods) for i in range(self.portSpace)]
        constraints += [np.sum(self.x[:, j, :, k]) <= 1 for k in range(self.goods) for j in range(self.portSpace)]
        # 5.transition-out should be after transition-in
        constraints += [stayTime[j, k] >= 0 for j in range(self.portSpace) for k in range(self.goods)]
        # 6.constraint for number of containers used
        numCtn = np.dot(self.x, self.kVol) / self.ctnVol
        constraints += [self.y[i, j, t] - numCtn[i, j, t] >= 0 \
                        for i in range(self.portSpace) for j in range(self.portSpace) for t in
                        range(self.dateSpace) if not isinstance(self.y[i, j, t] - numCtn[i, j, t] >= 0, bool)]
        # 7. constraint to check whether a route is used
        constraints += [self.z[i, j, t] >= (np.sum(self.x[i, j, t, :]) * 10e-5) \
                        for i in range(self.portSpace) for j in range(self.portSpace) for t in
                        range(self.dateSpace) if
                        not isinstance(self.z[i, j, t] >= (np.sum(self.x[i, j, t, :]) * 10e-5), bool)]
        # 8.time limitation constraint for each goods
        constraints += [np.sum(arrTime[:, self.kEndPort[k], :, k]) <= self.kDDL[k] for k in range(self.goods)
                        if not isinstance(np.sum(arrTime[:, self.kEndPort[k], :, k]) <= self.kDDL[k], bool)]
        model = cp.Problem(objective, constraints)

        self.objective = objective
        self.constraints = constraints
        self.model = model

    def pre_solve_model(self, solver=cp.CBC) -> None:
        try:
            self.objective_value = self.model.solve(solver)
            self.xs = np.zeros((self.portSpace, self.portSpace, self.dateSpace, self.goods))
            self.xs[self.var_location] = self.var.value
            self.ys = np.zeros((self.portSpace, self.portSpace, self.dateSpace))
            self.ys[self.var_2_location] = self.var_2.value
            self.zs = np.zeros((self.portSpace, self.portSpace, self.dateSpace))
            self.zs[self.var_3_location] = self.var_3.value
        except Exception as error:
            print(error)
            raise NotSolvable()