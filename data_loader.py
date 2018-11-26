from json_io import JsonFileReaderWriter
from json_parser import JsonCommitParser

import requests
import json

__all__ = ['GithubDataLoader']

# Secret access token
# Instructions to get it:
# https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/ 

with open('/Users/oleks/.tokens/github-api-token.txt', 'r') as file:
    SECRET_TOKEN = file.read()


class GithubDataLoader:
    def __init__(self, owner, repository):
        self.__owner = owner
        self.__repository = repository
        
        self.__commit_parser = JsonCommitParser()
        self.__json_io = JsonFileReaderWriter(owner, repository)
        
        # Template for GET requests
        self.__api = 'https://api.github.com/repos/{owner}/{repository}/{query}?{params}'

    
    def load_commits(self, commit_sha, verbose=False):
        commits = self.__load_next_100_commits(commit_sha, verbose)
        last_sha = self.__get_last_sha(commits)
        counter = 1

        while last_sha != commit_sha:
            commit_sha = last_sha
            self.__json_io.save_commits(commits, str(counter) + '__' + commit_sha)
            commits = self.__load_next_100_commits(commit_sha, verbose)
            last_sha = self.__get_last_sha(commits)
            counter += 1
            
            
    def load_patch(self, commit_sha):    
        patch = self.__load_patch(commit_sha)
        self.__json_io.save_patch(patch, commit_sha)
            
            
    def load_branches(self):
        branches = self.__load_branches()
        self.__json_io.save_branches(branches)
            
            
    def __request(self, query, param_dict={}, need_auth=True):
        if need_auth:
            param_dict['access_token'] = SECRET_TOKEN
            
        params = self.__dict_to_param_str(param_dict)

        url = self.__api.format(
            owner=self.__owner,
            repository=self.__repository,
            query=query,
            params=params)

        r = requests.get(url)
        
        if r.status_code == 200:
            with open('response.log', 'w') as f:
                json.dump(r.json(), f)
                
            return r.json()
        else:
            raise Exception(r.content)
    
    
    def __load_next_100_commits(self, commit_sha, verbose):
        """Loads the next 100 commits starting with a given commit.
        
        @param commit_sha: str
            SHA of the last commit that was loaded by the previous request.

        @param verbose: bool
            if True, the message will be printed before loading commits.
            
        @return
            JSON object - list of commits"""
        
        if verbose:
            print('Loadding commits starting at {}'.format(commit_sha))

        return self.__request('commits', {'per_page': 100, 'sha': commit_sha})
    
    
    def __load_patch(self, commit_sha):
        query = 'commits/' + commit_sha
        return self.__request(query, need_auth=False)
    
    
    def __load_branches(self):
        return self.__request('branches')

        
    def __dict_to_param_str(self, params):
        """Converts a dictionary of parameters to HTTP parameter string.
        
        @param params
            dictionary of parameters (key-value)
            
        @return
            parameter list as string in a form key1=value1&key2=value2"""

        if len(params) == 0:
            return ''

        pairs = ['{}={}'.format(key, value) for key, value in params.items()]
        param_str = '&'.join(pairs)

        return param_str

    
    def __get_last_sha(self, commits):
        return [self.__commit_parser.extract_sha(commit)
                for commit in commits][-1]