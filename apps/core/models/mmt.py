"""
MMT Model
"""
from itertools import product
import numpy as np
import pandas as pd
import json

from .error import NotSolvable


class MMT:
    """
    A Model class that solves the multi-model transportation optimization problem.
    """
    def __init__(self) -> None:
        # parameters
        self.portSpace = None
        self.dateSpace = None
        self.goods = None
        self.indexPort = None
        self.portIndex = None
        self.maxDate = None
        self.minDate = None
        self.tranCost = None
        self.tranFixedCost = None
        self.tranTime = None
        self.ctnVol = None
        self.whCost = None
        self.kVol = None
        self.kValue = None
        self.kDDL = None
        self.kStartPort = None
        self.kEndPort = None
        self.kStartTime = None
        self.taxPct = None
        self.transitDuty = None
        self.route_num = None
        self.available_routes = None
        # decision variables
        self.var = None
        self.x = None
        self.var_2 = None
        self.y = None
        self.var_3 = None
        self.z = None
        # result & solution
        self.xs = None
        self.ys = None
        self.zs = None
        self.whCostFinal = None
        self.transportCost = None
        self.taxCost = None
        self.solution_ = None
        self.arrTime_ = None
        self.objective_value = None
        # helping variables
        self.var_location = None
        self.var_2_location = None
        self.var_3_location = None

    def set_param(self, route: pd.DataFrame, order: pd.DataFrame) -> None:
        """set model parameters based on the read-in route and order information."""

        bigM = 100000
        route = route[route["Feasibility"] == 1]
        route.loc[route["Warehouse Cost"].isnull(), "Warehouse Cost"] = bigM
        
        route = route.reset_index()

        portSet = set(route["Source"]) | set(route["Destination"])

        self.portSpace = len(portSet)
        self.portIndex = dict(zip(range(len(portSet)), portSet))
        self.indexPort = dict(zip(self.portIndex.values(), self.portIndex.keys()))

        self.maxDate = np.max(order["Required Delivery Date"])
        self.minDate = np.min(order["Order Date"])
        self.dateSpace = (self.maxDate - self.minDate).days
        startWeekday = self.minDate.weekday() + 1
        weekday = np.mod((np.arange(self.dateSpace) + startWeekday), 7)
        weekday[weekday == 0] = 7
        weekdayDateList = {i: [] for i in range(1, 8)}
        for i in range(len(weekday)):
            weekdayDateList[weekday[i]].append(i)
        for i in weekdayDateList:
            weekdayDateList[i] = json.dumps(weekdayDateList[i])

        source = list(route["Source"].replace(self.indexPort))
        destination = list(route["Destination"].replace(self.indexPort))
        DateList = list(route["Weekday"].replace(weekdayDateList).apply(json.loads))

        self.goods = order.shape[0]
        self.tranCost = np.ones([self.portSpace, self.portSpace, self.dateSpace]) * bigM
        self.tranFixedCost = (
            np.ones([self.portSpace, self.portSpace, self.dateSpace]) * bigM
        )
        self.tranTime = np.ones([self.portSpace, self.portSpace, self.dateSpace]) * bigM

        for i in range(route.shape[0]):
            self.tranCost[source[i], destination[i], DateList[i]] = route["Cost"][i]
            self.tranFixedCost[source[i], destination[i], DateList[i]] = route[
                "Fixed Freight Cost"
            ][i]
            self.tranTime[source[i], destination[i], DateList[i]] = route["Time"][i]

        self.transitDuty = np.ones([self.portSpace, self.portSpace]) * bigM
        self.transitDuty[source, destination] = route["Transit Duty"]

        # make the container size of infeasible routes to be small enough, similar to bigM
        self.ctnVol = np.ones([self.portSpace, self.portSpace]) * 0.1
        self.ctnVol[source, destination] = route["Container Size"]
        self.ctnVol = self.ctnVol.reshape(self.portSpace, self.portSpace, 1)
        self.whCost = route[["Source", "Warehouse Cost"]].drop_duplicates()
        self.whCost["index"] = self.whCost["Source"].replace(self.indexPort)
        self.whCost = np.array(self.whCost.sort_values(by="index")["Warehouse Cost"])
        self.kVol = np.array(order["Volume"])
        self.kValue = np.array(order["Order Value"])
        self.kDDL = np.array((order["Required Delivery Date"] - self.minDate).dt.days)
        self.kStartPort = np.array(order["Ship From"].replace(self.indexPort))
        self.kEndPort = np.array(order["Ship To"].replace(self.indexPort))
        self.kStartTime = np.array((order["Order Date"] - self.minDate).dt.days)
        self.taxPct = np.array(order["Tax Percentage"])

        # add available route indexes
        self.route_num = route[["Source", "Destination"]].drop_duplicates().shape[0]
        routes = (
            route[["Source", "Destination"]].drop_duplicates().replace(self.indexPort)
        )
        self.available_routes = list(zip(routes["Source"], routes["Destination"]))
        # localization variables of decision variables in the matrix
        var_location = product(
            self.available_routes, range(self.dateSpace), range(self.goods)
        )
        var_location = [(i[0][0], i[0][1], i[1], i[2]) for i in var_location]
        self.var_location = tuple(zip(*var_location))

        var_2_location = product(self.available_routes, range(self.dateSpace))
        var_2_location = [(i[0][0], i[0][1], i[1]) for i in var_2_location]
        self.var_2_location = tuple(zip(*var_2_location))

        self.var_3_location = self.var_2_location

    def build_model(self) -> None:
        pass

    def pre_solve_model(self) -> None:
        pass

    def solve_model(self) -> None:
        """
        solve the optimization model & cache the optimized objective value, route and arrival time for each goods.
        :param solver: the solver to use to solve the LP problem when framework is CVXPY, has no effect to the model
        when framework is DOCPLEX. Default solver is cvxpy.CBC, other open source solvers do not perform that well.
        :return: None
        """
        self.pre_solve_model()
        nonzeroX = list(zip(*np.nonzero(self.xs)))
        nonzeroX = sorted(nonzeroX, key=lambda x: x[2])
        nonzeroX = sorted(nonzeroX, key=lambda x: x[3])
        nonzeroX = list(map(lambda x: (self.portIndex[x[0]], self.portIndex[x[1]], \
                                       (self.minDate + pd.to_timedelta(x[2], unit='days')).date().isoformat(),
                                       x[3]), nonzeroX))

        self.whCostFinal, arrTime, _ = self.warehouse_fee(self.xs)
        self.transportCost = np.sum(self.ys * self.tranCost) + np.sum(self.zs * self.tranFixedCost)
        self.taxCost = np.sum(self.taxPct * self.kValue) + \
                       np.sum(np.sum(np.dot(self.xs, self.kValue), axis=2) * self.transitDuty)
        self.solution_ = {}
        self.arrTime_ = {}
        for i in range(self.goods):
            self.solution_['goods-' + str(i + 1)] = list(filter(lambda x: x[3] == i, nonzeroX))
            self.arrTime_['goods-' + str(i + 1)] = (self.minDate + pd.to_timedelta \
                (np.sum(arrTime[:, self.kEndPort[i], :, i]), unit='days')).date().isoformat()

    def get_output_(self):
        """
        After the model is solved, return total cost, final solution and arrival
        time for each of the goods.
        """
        return self.objective_value, self.solution_, self.arrTime_

    def warehouse_fee(self, x):
        """Return warehouse fee, arrival time and stay time for each port."""
        startTime = np.arange(self.dateSpace).reshape(1, 1, self.dateSpace, 1) * x
        arrTimeMtrx = startTime + self.tranTime.reshape(self.portSpace, \
                                                        self.portSpace, self.dateSpace, 1) * x
        arrTime = arrTimeMtrx.copy()
        arrTimeMtrx[:, self.kEndPort.tolist(), :, range(self.goods)] = 0
        stayTime = np.sum(startTime, axis=(1, 2)) - np.sum(arrTimeMtrx, axis=(0, 2))
        stayTime[self.kStartPort.tolist(), range(self.goods)] -= self.kStartTime
        # warehouseCost = np.sum(np.sum(stayTime * self.kVol, axis=1) * self.whCost)

        return 0, arrTime, stayTime

    def txt_solution(self, route: pd.DataFrame, order: pd.DataFrame):
        """transform the cached results to text."""

        travelMode = dict(
            zip(zip(route["Source"], route["Destination"]), route["Travel Mode"])
        )
        txt = "Solution"
        txt += "\nNumber of goods: " + str(order["Order Number"].count())
        txt += "\nTotal cost: " + str(
            self.transportCost + self.whCostFinal + self.taxCost
        )
        txt += "\nTransportation cost: " + str(self.transportCost)
        txt += "\nWarehouse cost: " + str(self.whCostFinal)
        txt += "\nTax cost: " + str(self.taxCost)

        for i in range(order.shape[0]):
            txt += "\n------------------------------------"
            txt += "\nGoods-" + str(i + 1) + "  Category: " + order["Commodity"][i]
            txt += (
                "\nStart date: "
                + pd.to_datetime(order["Order Date"]).iloc[i].date().isoformat()
            )
            txt += "\nArrival date: " + str(self.arrTime_[f"goods-{str(i + 1)}"])
            txt += "\nRoute:"
            solution = self.solution_[f"goods-{str(i + 1)}"]
            
            route_txt = "".join(
                f"\n({a + 1})Date: {j[2]}  From: {j[0]}  To: {j[1]}  By: {travelMode[j[0], j[1]]}"
                for a, j in enumerate(solution)
            )
            txt += route_txt

        return txt

    
    def solution(self, order: pd.DataFrame) -> str:
        """Transform the cached results"""
        if self.arrTime_['goods-1'] == "NaT":
            raise NotSolvable()
            
        txt = ""
        txt += "\nMercancia: " + order["Commodity"][0]
        txt += (
            "\nFecha inicio: "
            + pd.to_datetime(order["Order Date"]).iloc[0].date().isoformat()
        )
        txt += f"\nFecha fin: {self.arrTime_['goods-1']}"
        txt += "\nRutas:"
        solution = self.solution_["goods-1"]
        
        route_txt = ""
        a = 1
        
        for i in solution:
            route_txt += "\n(" + str(a) + ")Fecha: " + i[2]
            route_txt += "  Desde: " + i[0]
            route_txt += "  Hacia: " + i[1]
            a += 1
        txt += route_txt
        txt += "\n------------------------------------"

        return txt