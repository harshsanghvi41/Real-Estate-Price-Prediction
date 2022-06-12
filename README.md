## Start Machine Learning project.

### Software and account Requirement.
 
1. [Github Account](https://github.com/)
2. [Heroku Account](https://id.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT CLI](https://git-scm.com/downloads)


Create a conda environment
```
conda create -p mlproject python==3.7 -y
```
Activate Virtual Environment
```
conda activate mlproject
```
OR
``` 
conda activate mlproject/
```
pip install -r requirements.txt
```

To Add files to git
```
git add .
```
OR
```
git add <file_name>
```
Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

To check the git status
```
git status
```
To check all version maintained by git
```
git log
```
To create version/commit all changes by git
```
git commit -m "message"
```
To send version/changes to github
```
git push origin main
```
To check remote url
```
git remote -v
```