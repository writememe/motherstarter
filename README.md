# mother-starter

A network tool to accelerate the adoption of network automation

## Installation Instructions

Follow the installation instructions below:

1. Clone the repository to the machine on which you will run the application from:

```bash
git clone https://github.com/writememe/motherstarter.git
cd motherstarter
```

2. Create the virtual environment to run the application in:

```bash
virtualenv --python=`which python3` venv
source venv/bin/activate
```

3. Install the requirements:

pip install -r requirements.txt


## Usage

To use motherstarter, please look at the command-line helper below:

```python
> python motherstarter.py --help

usage: motherstarter.py [-h] [-l {debug,info,warning,error,critical}]
                        [-st {json,csv,xlsx}] [-sd SOURCE_DIR]
                        [-o {nornir,csv,xlsx,pyats,all}]

Translate source file(s) into network automation inventory outputs

optional arguments:
  -h, --help            show this help message and exit
  -l {debug,info,warning,error,critical}, --log {debug,info,warning,error,critical}
                        Specify the logging level
  -st {json,csv,xlsx}, --source-type {json,csv,xlsx}
                        Specify the source file type. Default is JSON
  -sd SOURCE_DIR, --source-dir SOURCE_DIR
                        Specify the source directory for the source files.
                        Default is tree structure under the 'inputs/' folder.
  -o {nornir,csv,xlsx,pyats,all}, --output-type {nornir,csv,xlsx,pyats,all}
                        Specify the output file types. Default is all file
                        types. This arguement only takes one option.

```

To run using the defaults, execute the following:

```python
python motherstarter.py 
```