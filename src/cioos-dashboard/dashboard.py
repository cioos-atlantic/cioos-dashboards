import json
from erddapy import ERDDAP
from panel.viewable import Viewable
from pandas import DataFrame
from typing import TypeVar, Generic

T = TypeVar['T']

class IDashboard:

    _settings: dict

    def __init__(this, **settings):
        this._settings = settings
        pass

    def getData(source : str) -> DataFrame:
        """Logic for extracting data from ERDDAP server."""
        pass

    def dataFrame() -> DataFrame:
        pass

    def getPanel() -> Viewable:
        pass

    def setTitle(title: str) -> None : 
        pass

    def changeParam(param: str) -> None :
        pass


class IDashboardBuilder:
    __dashboard: IDashboard

    def __init__(self, dashboard: IDashboard):
        self.__dashboard = dashboard
        self.reset

    def reset(self):
        self.__dashboard._settings.clear()

    def buildERDDAP(self, server: str, protocol: str = 'tabledap', auth: tuple = ("", ""), response: str = ""):
        """Builds the base Erddap settings (auth, url etc.)."""
        self.dashboard._settings['erddap'] = ERDDAP(server, protocol)
        self.dashboard._settings.erddap.auth = (auth)
        self.dashboard._settings.erddap.response = response
        return self

    def setVariables(self, variables: list = []):
        """Sets the base variable list to collect in ERDDAP."""
        if not self.dashboard._settings['erddap']:
            raise LookupError(
                "No base Erddap settings, please use .buildErddap() first.")
        self.__dashboard._settings.erddap.variables = variables
        return self

    def setConstraints(self, **constraints):
        self.__dashboard._settings.erddap.constraints = constraints
        return self

    def setLookups(self, ids: list, lookup_var: str = "waterbody_station"):
        """Sets a dictionary of lookup names and the corresponding dataset id."""
        def __getLookup(id, var='waterbody_station'):
            erddap = self.__dashboard._settings.erddap.copy()
            erddap.dataset_id = id
            erddap.variables = [var]
            return sorted(list(erddap
                               .to_pandas()
                               .waterbody_station
                               .astype(str)
                               .unique()))

        lookup_dict = {lookup[i]: val for val in ids for i,
                       lookup in __getLookup(val, lookup_var)}
        self.__dashboard._settings.lookup = lookup_dict
        self.__dashboard._settings.lookup_keys = lookup_dict.keys()

    def addItem(self, dataset_id: str):
        self.dashboard._settings.erddap.dataset_id = dataset_id

    def build(self) -> IDashboard:
        return IDashboard(self.__dashboard)


if __name__ == "__main__":
    pass
