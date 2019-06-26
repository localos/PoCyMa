# PoCyMa
PotatoCyb0rMap - KI driven traffic analysis and reporting tool.

![alt text](https://github.com/localos/PoCyMa/blob/master/pocyma_logo.png "Logo PoCyMa")

## Idea behind
IT incidents can have a wide range of causes from a simple connection loss to an insistent attack. Once a potential IT security incident and system failure has been identified, deciding how to proceed is often complex. Especially, if the real cause is not directly determinable in detail. Therefore, we developed the concept of a Cyber Incident Handling Support System.

The developed system is enriched with information by multiple sources such as intrusion detection systems and monitoring tools. It uses over twenty key attributes like sync-package ratio to identify potential security incidents and to classify the data into different priority categories.
Afterwards, the system uses artificial intelligence to support the further decision-making process and to generate corresponding reports to brief the executive layer of a company. Originating from this information, appropriate and detailed suggestions are made regarding the causes and troubleshooting measures. Feedback from users regarding the problem solutions are included into future decision-making by using labelled flow data as input for the learning process. The prototype shows that the decision making can be sustainably improved and the Cyber Incident Handling process becomes much more effective.

The idea behind PoCyMa is to support decision makers as well as technicians when it comes to possible incidents, strange behaviour or similar based on traffic analysis and/or network monitoring tools.

### Goal
* Develop a tool for the community
* OpenSource
* Extensible
* Offline use

## Use Cases
A medium-sized company which uses troubleshooting, monitoring, and security systems is regarded as an application user. Failures and malfunctions of the IT systems lead to direct implications for the company's value creation process. Therefore, a fast recovery to a normal status of operation is highly important. Due to the legal situation, e.g. the obligation to report security critical incidents, the management is confronted with the topic of IT security. In context of Enterprise Architecture, the management wants to be informed about detected incidents and possible risks as well as to be involved in the solution process. In view of the often narrow financial resources for IT security, existing systems and information such as IDS should be used and integrated into the overall concept of the new AI-based security solution. The resulting data must be prepared and analysed in the overall context, hence eventually serving as the basis for best-practice proposed solutions. Furthermore, the data has to be explained in an understandable way to people with less technical affinity. Since best practices are only indicative and not applicable to all situations, a way to incorporate feedback must be provided.

### Short Overview of use cases
* Troubleshooting
* Incident Response
* Decision support
* Individual operational situation picture
* Forensics

## Requirements
The previous application example and the scientific questions result in different requirements for decision support systems for IT incidents:
* __Analysis of data:__ Processing large and different data types leads to the challenges of Big Data.
* __Pattern Recognition:__ In connection with data analysis, adequate solutions have to be provided by specifying recognized incidents based on known values and correlations.
* __Decision and command support:__ The core functions of the system are to provide solutions and multiple possibilities to act during detected incidents. These suggested solutions are intended to provide an overview of detailed and adequate measures that the user can take to counteract an attack and to recover.
* __Feedback embedding:__ The ability to evaluate individual solution proposals by user feedback to treat future events in a better way.
* __Anonymisation:__ With the new EU law of the General Data Protection Regulation (GDPR), personal data has to be anonymized in order to prevent possible conclusions about company-specific architectures or processes.
* __Extensibility:__ The integration of new functions should be possible at any time. Errors and maintenance should be easily identified - handled respectively - and improved during operation in order to save resources.
* __Automation:__ The user should be able to generate a report for the participation of the higher company levels. This should show the management level recognized situations and describe their effects on the IT infrastructure.

## Concept
PoCyMa is a Cyber Incident Response System (we know that the term Cyber sucks ^^), which include multiple sources like vulnerability databases to be aware of up-to-date attack vectors and geo-databases for IP-Geolocation to identify attack sources. Nevertheless, this
presented approach is also usable as stand alone application. The working title PoCyMa (PotatoCyberMap) originate from a live attack event on a twitter stream from a person alias cyber potato during a security conference in 2016. After this
event, we started to develop a comprehensive countermeasurement, which this approach is part of.

## Architecture
A more or less small overview can be found [here](https://github.com/localos/PoCyMa/blob/master/architecture/pocyma_full.pdf)

Based on the Model-View-Controller principle, the PoCyMa architecture consists of the three planes, being the Data-, Control, and Business Intelligence (BI) Plane. Every plane is responsible for a defined task.

The Control Plane is used to monitor and configure the usage of the program. The Data Plane is used to prepare and bundle data from different sources like IDS, SIEM, geolocation, and vulnerabilities with tools like Nagios and Tranalyzer for flow information. These are used for visualization in respect to the different hierarchy levels. The project resides inside the BI plane, which is used to support AI-based solutions. This includes data, that is produced internally in a company like from troubleshooting systems, self developed rescue plans and monitoring information. Due to logging of events with a ticket system and wiki as well as their respective solutions, there is a broad knowledge base to use. The overlying objective is to provide suggestions for adequate solutions, based on best practices and solved events.

### Structure and Control Plane
The system is built with a modular approach to ensure both, easy maintainability and expandability. The main module provides the main interface for the user and serves as the controller of PoCyMa BI plane. The AI consists of a fully connected Deep Feed Forward Neural Network (NN) which uses two hidden layers and gets trained via supervised learning. The NN is represented by the AI-Module. The four layers of the NN are needed to ensure the correct handling of the variable complexity. A leaky rectified linear unit algorithm is used as the activation function inside the NN. The functionality is based on the classical maximum principle to identify thresholds of the key attributes of the input values. The output layer of the NN uses a standard softmax function, which helps dividing the probability onto the different possible outcomes z. It is typically used for scenarios with multiple classification and regression models as we focus on. The variable z represents the input value from a specific neuron j. Each input value of the multiple neuron (1 to K) influences the output value of the considered and firing neuron. Training optimization is realised by using the Adaptive Moment Estimation (ADAM). The train module includes the data analysis and data processing in accordance with the Extract-Transfer-Load (ETL) process and therefore handles the preparation of the input data. This is used by the AI and the train module. The prediction module analyses new data in coordination with the AI module and puts out weighted treatment options, out of an array of trained solutions. Those solutions can be printed via the output module and exported as PDF file.
To ensure a continual improvement of the suggested solutions and treatment options, the given user feedback is used inside the training process. This feedback contains a valuation of the given solutions in respect to their usability
and how well the solution fits the initial problem or event. With these user provided inputs, new training sets get created which are then used to further train the NN, which leads to helpful solutions being suggested more often and to a more and more personalized NN.

#### Components
* Controller
* Configuration
* Administration Board
* GUI Analysis

### Data Plane
According to the structure of PoCyMa, the needed data is getting extracted from the data plane. This data is flow-based and contains information from at least one IDS. According on this data, a first analysis in regards of certain incidents and attack vectors, as well as a first flow labelling is being made. Non-relevant flows are filtered out of the data set. The flow data is then transformed into values between zero and one by using an arithmetic function, so that they can be used in the training process. A zero representing a normal behaviour and a one representing a abnormal one. This arithmetic function varies in respect to the transformed data type and its minimum and maximum value. After the data has been properly labelled and transformed, it is transferred to the AI module according to the load step of the ETL process. At this time, the data set contains 23 different attributes, which are used by the NN. These are not limited and can be extended with geoinformation and vulnerability codes.
For each flow of data, the values are calculated according to the attributes of the table. As a measure, scaling and generalization are necessary. Metrics defined in a metrics collection are used for this purpose. Since the AI is a neural network, floating point numbers between 0 and 1 are required. The calculation of every key attribute is similar for all input values. Discrete values like the port number have a special form. The index value of the current attribute is divided by the maximum index number defined by the standard or request for comments (RFC). Subsequently, a two-dimensional mapping of the attributed flows to the input data template of the processing pipeline takes place. Nevertheless, each flow is analysed individually, before a correlation between multiple flows takes place.

| ID | Attribute | Description |
| --- | --- | --- |
| 1 | Flowindex | ID of concatenated flows |
| 2 | Duration | Timelength of a flow |
| 3 | IP Destination | IP Address of destination |
| 4 | Source Port | Source Port of sender |
| 5 | Destination Port | Destination Port of the receiver |
| 6 | L4 Protocol | Protocol of transport layer |
| 7 | DstPortClass | Classification of the port |
| 8 | TCP-Rate | Relation between TCP-Packets and all Packets of a flow |
| 9 | TCPPAckCntAsm | TCP-ACK-Asymmetrie |
| 10 | PktAsm | Paket-Asymmetrie |
| 11 | BytAsm | Byte-Asymmetrie |
| 12 | TCPStat | TCP Status |
| 13 | IPMinTTL | Minimum IP Time to live |
| 14 | IPMaxTTL | Maximum IP Time to live |
| 15 | PerPS | Relation between packets send per Flow |
| 16 | TCPSeqFCnt-Rate | Relation between TCPSeqFaultCnt and TCPSeqCnt |
| 17 | TCPAckFCnt-Rate | Relation between TCPAckFaultCnt and TCPAckCnt |
| 18 | EstBwPFlow | Average Bandwith of a flow |
| 19 | TCPAggrFlags | TCP-Flags of a flow |
| 20 | TCPAggrAnomaly | Aggregated TCP-Header, Anomaly-Flags |
| 21 | TCPAggrOptions* | Aggregated TCP Options |
| 22 | TCPStates | States of a TCP connection |
| 23 | Label | Scenario based label including feedback |

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

### Business Intelligence Plane
Takes information from the data plane and does some black magic ;)

The Decision Support and Feedback Usage works as follows: The NN is constructed in a way, that it can create treatment recommendations based on the enriched flow data, by classifying the data after they were analysed and prepared by the ETL process. For the first prototype, we limited the classification to normal traffic, service incident, and denial-of-service attack. According to these classifications, the user gets shown an array of treatment recommendations, which are based on known best practices and information from solved events. These solutions can then be rated by the user in respect to their efficiency. This rating gets included into the training of the NN by using an updated training set, which considers the before made ratings of the user, for every training process that occurs. This contributes to the aforementioned continual solution improvement. After a successful check, the set is loaded and the training is performed with a subset of the data. After that the changed weights of the net will be saved in a suitable form. If the check reveals that an unexpected deletion of the set has taken place, the entire original set is used to carry out the training in retrain mode.

#### Components
* [NERD](https://github.com/localos/PoCyMa/blob/master/components/NERD)
* Relational database management system
* Artifical Intelligence
* Data Extractor
* Normalizer
* Aggregator
* Anonemizer
* Loading-Module

## License
The content of this project itself is licensed under [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), and the underlying source code is licensed under [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
