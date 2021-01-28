import pandas as pd
import github.api as api

class Repository(api.Worker):

    def __init__(self, token):
        super().__init__(token)
        
