# motherstarter

A network tool to accelerate the adoption of network automation by providing a command-line interface to convert input file sources to various network automation output formats.

## Nomenclature

Throughout the tool and subsequent code, it's important to establish some terminology which is used. Unsuprisingly, each automation solution uses slightly different names for the same thing. A reference table
is supplied below:

### Definitions

| motherstarter | nornir | ansible | pyats |
| -------------- | ----- | ------- | ----- |
| inventory |hosts|hosts|devices|
|groups |groups|groups|Not applicable|
| Not applicable |defaults|all|Not applicable|

motherstarter will make frequent usage of `inventory` and `groups` throughout the code and templates, so this table is a handy reference when trying to understand the differences.

## What is with the name?

Do you appreciate a good sourdough? As part of the process, bakers will nuture a 'starter' (or mother starter) consisting of flour, water and wild yeast. Each day they take some of the starter to make loaves and the rest is fed with fresh water and flour. Over time, the 'motherstarter' increases in complexity and makes even tastier sourdough bread. From basic, freely avialable ingredents, a very tasty bread is made.

motherstarter is a take on this concept. You feed the tool good "data", and you can take it's output to make great solutions. Over time, you feed it even more data and as a result, you can solve more complex and interesting problems on more devices.
 
## What is motherstarter?

motherstarter was created to bridge the gap between those wanting to use network automation and those who already are with fully formed network automation platforms.

At it's core, motherstarter is designed to address three primary-use cases:

1) Take one input type (json, csv, xlsx) and convert to one or many outputs
2) Provide a facility to promote experimentation with multiple network automation frameworks/solutions
3) Provide a translation layer between "traditional" inventory sources (spreadsheets) and more modern inventory
sources
4) Provide extensibility to leverage custom data to enrich metadata about your inventory

### motherstarter is not ...

It's important to understand that motherstarter does not intend, nor plan to be a permanent, enterprise-class inventory solution. motherstarter cannot substitute for a first-class system such as netbox. It's anticipated that you will reach the limits of motherstarter as an inventory solution, if you plan to make the inventory files available in multiple locations over multiple solutions.

You may temporarily get around this by saving the outputs to Git and using version control to track changes. But, again a proper, permanent solution should be considered beyond that.

### Why should you use motherstarter?

motherstarter is a value to those who are:
- Looking to "seed" new network automation platforms. For example, use nornir/napalm to get facts about a network and then populate a system such as netbox.
- Looking to trial and experiment different automation frameworks. For example, you want to try pyATS for a certain feature, or use Ansible modules because they solve a specific use-case for fact gathering.
- Who move between multiple environments and need reliable inventory sources for automation solutions. For example, you are a consultant who has to perform network audits or perform repetitive work between multiple customers.
- Need an interim inventory offering, prior to migrating to a more robust solution.



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

```bash
pip install -r requirements.txt
```

## Usage

To use motherstarter, please look at the command-line helper below:

```
> python motherstarter.py convert --help
Usage: motherstarter.py convert [OPTIONS]

  Convert source file(s) into network automation inventory outputs based on
  multiple command-line inputs.

  For example:     Input type: json     Output type: nornir

Options:
  -l, --log-level [debug|info|warning|error|critical]
                                  Specify the logging level.  [default: debug]
  -st, --source-type [csv|json|xlsx]
                                  Specify the source file type.  [default:
                                  json]

  -sd, --source-dir TEXT          Specify the source directory for the source
                                  files. Default is tree structure under the
                                  'inputs/' folder.

  -o, --output-type [all|csv|json|nornir|pyats|xlsx]
                                  Specify the output file types.  This
                                  argument only takes one option.  [default:
                                  all]

  --help                          Show this message and exit.

```

To run using the defaults, execute the following:

```python
cd motherstarter/
python motherstarter.py convert
```