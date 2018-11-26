from data_loader import GithubDataLoader
from df_builder import DataFrameBuilder

owner = 'apache'
repository = 'ant'


if __name__ == '__main__':
    loader = GithubDataLoader(owner, repository)
    df_builder = DataFrameBuilder(owner, repository)

    print('Loading branches')
    loader.load_branches()

    print('Building DataFrame of branches')
    branches = df_builder.branches()
    branches.to_csv('branches.csv', index=False)

    print(branches.head())

    master_sha = branches[branches['name'] == 'master']['commit_sha'].iloc[0]

    print('Loading commits from master branch')
    loader.load_commits(master_sha, verbose=True)

    print('Building DataFrame of commits')
    commits = df_builder.commits()
    commits.to_csv('commits.csv', index=False)

    print(commits.head())
