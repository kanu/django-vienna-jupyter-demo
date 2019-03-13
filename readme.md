# Installation

create a virtual environment
```bash
virtualenv venv
```
activate venv
```bash
source venv/bin/activate
```
install the requirements
```bash
pip install -r demo/requirements.txt
```
start the notebook server
```bash
cd demo
python manage.py shell_plus --notebook
```
Look for these lines in the output and follow the instructions
```bash
[C 08:38:20.350 NotebookApp]
    To access the notebook, open this file in a browser:
        file:///YOUR_PATH_TO_JUPYTER/Jupyter/runtime/nbserver-82609-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=YOUR_TOKEN
``` 

open the `demo/setting_up_the_demo.ipynb` Notebook and run it.

when setup is complete you can use `demo/loading_meetup_data.ipynb` to load meetup groups.
 