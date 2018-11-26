from json_io import JsonFileReaderWriter
from json_parser import JsonCommitParser
from json_parser import JsonBranchParser

import os
import pandas as pd


class DataFrameBuilder:
    def __init__(self, owner, repository):
        self.__json_io = JsonFileReaderWriter(owner, repository)
        self.__commit_parser = JsonCommitParser()
        self.__branch_parser = JsonBranchParser()

        
    def commits(self):
        commit_infos = []
        commit_files = self.__commit_file_names()
        
        for name in commit_files:
            commits = self.__json_io.load_commits(name)
            
            for commit in commits:
                info = self.__commit_parser.extract_all_info(commit)
                commit_infos.append(info)
        
        return self.__df_from_list_of_dicts(commit_infos)
    
    
    def branches(self):
        branches = self.__json_io.load_branches()
        
        branch_infos = [self.__branch_parser.extract_all_info(branch)
                       for branch in branches]
        
        return self.__df_from_list_of_dicts(branch_infos)
    
    
    def __commit_file_names(self):
        path = self.__json_io.commits_directory
        
        file_names = [f for f in os.listdir(path)
                      if os.path.isfile(os.path.join(path, f))]
        
        file_names = [f for f in file_names if f[-5:] == '.json']
        file_names = [f[:-5] for f in file_names]
        
        return file_names
    
    def __df_from_list_of_dicts(self, dicts):
        col_names = dicts[0].keys()
        rows = [d.values() for d in dicts]
        
        return pd.DataFrame(rows, columns=col_names)