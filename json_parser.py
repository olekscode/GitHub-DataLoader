from collections import OrderedDict

__all__ = [
    'JsonCommitParser',
    'JsonBranchParser'
]


class JsonCommitParser:
    """Contains functions for parsing JSON commit data acquired from GitHub"""
    
    def extract_all_info(self, commit):
        return OrderedDict([
            ('sha', self.extract_sha(commit)),
            ('date', self.extract_date(commit)),
            ('author_name', self.extract_author_name(commit)),
            ('author_email', self.extract_author_email(commit)),
            ('message', self.extract_message(commit))
        ])
    
    def extract_sha(self, commit):
        return commit['sha']
    
    
    def extract_date(self, commit):
        return commit['commit']['author']['date']
    
    
    def extract_author_name(self, commit):
        return commit['commit']['author']['name']
    
    
    def extract_author_email(self, commit):
        return commit['commit']['author']['email']
    
    
    def extract_message(self, commit):
        return commit['commit']['message']


class JsonBranchParser:
    """Contains functions for parsing JSON branch data acquired from GitHub"""
    
    def extract_all_info(self, branch):
        return OrderedDict([
            ('name', self.extract_name(branch)),
            ('commit_sha', self.extract_commit_sha(branch))
        ])
    
    
    def extract_name(self, branch):
        return branch['name']
    
    
    def extract_commit_sha(self, branch):
        return branch['commit']['sha']