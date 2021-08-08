from typing import List
import pandas as pd
from tabulate import tabulate


class datatransformer:
    
    def print_response_table(self, resp_list: List):
        tables = pd.DataFrame(resp_list)
        tables.columns = ["endpoint", "value", "mode",
                          "time", "status", "outcome"]
        return tabulate(tables, headers='keys', tablefmt='psql')
