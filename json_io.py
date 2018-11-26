import os
import json
import errno


__all__ = ['JsonFileReaderWriter']


class JsonFileReaderWriter:
    def __init__(self, owner, repository):
        self.__owner = owner
        self.__repository = repository
        
        self.commits_directory = self.__data_directory('commits')
        self.patches_directory = self.__data_directory('patches')
        self.branches_directory = self.__data_directory('branches')
        
        self.BRANCHES_FILE_NAME = 'branches'
        
        
    def save_commits(self, commits, earliest_date):
        self.__save_data(commits, self.commits_directory, earliest_date)
        
        
    def save_patch(self, patch, commit_sha):
        self.__save_data(patch, self.patches_directory, commit_sha)
        
        
    def save_branches(self, branches):
        self.__save_data(branches, self.branches_directory, self.BRANCHES_FILE_NAME)
        
        
    def load_commits(self, earliest_date):
        return self.__load_data(self.commits_directory, earliest_date)
    
    
    def load_patch(self, commit_sha):
        return self.__load_data(self.patches_directory, commit_sha)
    
    
    def load_branches(self):
        return self.__load_data(self.branches_directory, self.BRANCHES_FILE_NAME)
    
    
    def __data_directory(self, kind):
        return 'data/{}/{}/{}'.format(
            kind,
            self.__owner,
            self.__repository)
        
    
    def __save_data(self, data, directory, name):
        file_name = '{}/{}.json'.format(directory, name)
        self.__save_json(data, file_name)
    
        
    def __load_data(self, directory, name):
        file_name = '{}/{}.json'.format(directory, name)
        return self.__load_json(file_name)
        
        
    def __save_json(self, json_data, file_name):
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        with open(file_name, 'w') as file:
            json.dump(json_data, file)
            
            
    def __load_json(self, file_name):
        with open(file_name, 'r') as file:
            return json.load(file)