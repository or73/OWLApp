"""
File Path: application/aux_funcs.py
Description: Application Constants
Copyright (c) 2019. This Application has been developed by OR73.
"""
import ast
import os
from dotenv import load_dotenv

load_dotenv()


class AuxFuncs:
    @staticmethod
    def previous_page(prev_string: str) -> str:
        fuzzy = ast.literal_eval(os.environ.get('FUZZY'))
        paths = fuzzy['PATHS']
        funcs = fuzzy['FUNCS']

        best_match_position = -1
        for func in funcs:
            if func in prev_string:
                best_match_position = funcs.index(func)
        if best_match_position == -1:
            best_prev_link = 'user_bp.users'
        else:
            best_prev_link = paths[best_match_position]
        return best_prev_link
