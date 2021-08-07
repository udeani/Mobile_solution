# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 20:34:11 2021

@author: HENRY
"""
import pandas as pd
bu_info = pd.DataFrame({"bu_id": "B0109", "name": "FerryLand", "gps_loc": [12.92329, -7.70544]})

bu_info.to_csv("bu_info.csv")