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
To Install requirement file
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

> Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

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

To setup CI/CD pipeline in heroku we need 3 information

  1. HEROKU_EMAIL : <heroku_email>
  2. HEROKU_API_KEY = <heroku_api_key>
  3. HEROKU_APP_NAME = <heroku_app_name>

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .
```

> Note: Image name for docker must be lowercase

To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```

To check running container in docker
```
docker ps
```

Tos stop docker conatiner
```
docker stop <container_id>
```

```
python setup.py install
```

Install Ipynb-kernal
```
pip install ipykernel
```

Install PyYAML
```
pip install PyYAML
```

> Data Drift: When your datset stats gets change we call it as data drift