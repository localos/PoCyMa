# PoCyMa
PotatoCyb0rMap - KI driven traffic analysis and reporting tool.

![alt text](https://github.com/localos/PoCyMa/blob/master/pocyma_logo.png "Logo PoCyMa")

## Idea behind
The idea behind PoCyMa is to support decision makers as well as technicians when it comes to possible incidents, strange behaviour or similar based on traffic analysis and/or network monitoring tools.  

### Goal
* Develop a tool for the community
* OpenSource
* Extensible
* Offline use

## Use Cases
tba.

### Troubleshooting
tba.

### Incident Response
tba.

### Decision support
tba.

### Individual operational situation picture
tba.

### Forensics
tba.

## Architecture
A more or less small overview can be found [here](https://github.com/localos/PoCyMa/blob/master/architecture/pocyma_full.pdf)

### Data Plane
tba.

#### Components
* [Anteater](https://tranalyzer.com/) (Tranalyzer2)
* [Apache Solr](https://lucene.apache.org/solr/)
* Some IDS ...doesn't matter which one (almost ^^)
* OpenStreetView server
* [IPTrollNG](https://github.com/localos/IPTrollNG)
* Some relational database management system
* Some parser, wrapper and nodejs stuff
* Frontend
* ...

### Control Pane
tba.

#### Components
* Controller
* Config stuff
* Admin frontend
* ...

### Business Intelligence Plane
Takes information from the data plane and does some black magic ,)

#### Components
* [NERD](https://github.com/localos/PoCyMa/blob/master/components/NERD)
* Some relational database management system
* ...

## License
The content of this project itself is licensed under [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), and the underlying source code is licensed under [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
