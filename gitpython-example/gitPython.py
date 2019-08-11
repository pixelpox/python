#https://gitpython.readthedocs.io/en/stable/tutorial.html
#https://stackoverflow.com/questions/13166595/how-can-i-pull-a-remote-repository-with-gitpython
#https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python


from git import Repo
import shutil

def main():
	print("GIT PYTHON EXAMPLE")

	repoFileLocation = '~/github/pixelpox.github.io/'

	repo = Repo(repoFileLocation)
	
	print('pull any changes from remote server...')
	github = repo.remotes.origin
	github.pull()

	print('move files to folder')

	#shutil.copy2()

	print('files to commit')
	print(repo.untracked_files)

	print('commiting files...')
	repo.index.add(['python.test'])
	repo.index.commit('adding new files')

	print('pushing files to github...')
	github.push()


if __name__ == "__main__":
	main()