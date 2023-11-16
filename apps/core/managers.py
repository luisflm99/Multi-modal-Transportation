import numpy as np
import pandas as pd

from django.db import models


class RouteManager(models.Manager):
    def routes_dataframe(self) -> pd.DataFrame:
        models = self.all()
        routes = [route.to_dataframe for route in models]
        routes = pd.concat(routes, ignore_index=True)
        routes["Cost"] = routes[routes.columns[7:12]].sum(axis=1)
        routes["Time"] = np.ceil(routes[routes.columns[14:18]].sum(axis=1) / 24)
        routes = routes[
            list(routes.columns[:4])
            + [
                "Fixed Freight Cost",
                "Time",
                "Cost",
                "Warehouse Cost",
                "Travel Mode",
                "Transit Duty",
            ]
            + list(routes.columns[-9:-2])
        ]
        routes = pd.melt(
            routes,
            id_vars=routes.columns[:10],
            value_vars=routes.columns[-7:],
            var_name="Weekday",
            value_name="Feasibility",
        )
        routes["Weekday"] = routes["Weekday"].replace(
            {
                "Monday": 1,
                "Tuesday": 2,
                "Wednesday": 3,
                "Thursday": 4,
                "Friday": 5,
                "Saturday": 6,
                "Sunday": 7,
            }
        )

        return routes
