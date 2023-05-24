## Reducing the Memory Footprint of IFDS-based Data-Flow Analyses Using Fine-Grained Garbage Collection (Artifact)

The outline of this guide is given below:

- Requirements
- Getting Started
  - Run Docker Image
  - Directory Structure
  - Test driven script
  - Test Table/Figures Generation Script
- Detailed Instructions
  - Step 1: run `runBen.py`
  - Step 2: generate tables and figures
  - Step 3: validate paper claims

### Requirements
We will provide a ready-to-use docker image for artifact evaluation. Our tool, FPC, has been open-sourced at https://github.com/DongjieHe/FPC.git. 

For users who want to use our tool on their local machines, we briefly introduce the 
requirements or dependencies of `FPC` below.

The artifact built on the latest version of Ubuntu relies on the following softwares: `Python3`, `open-jdk8`, `xetex`, and `Python3-pip`. If one want to build the source code, then `maven` is also required. These softwares can be installed by following commands: 
```
# apt-get install -y openjdk-8-jdk-headless
# apt-get install python3 -y
# apt-get install python3-pip -y
# apt-get install texlive-xetex -y
# apt-get install maven -y
```
The python scripts in this artifact have used a few third-party packages: `matplotlib`, `numpy`, `prettytable`, and `brokenaxes`.
We have prepared them in `requirements.txt` so that users can use the following commands to install them all by one command:
```
# pip3 install -r requirements.txt
```

As described in the experimental Setting in our paper, our experiments are performed on a Linux server, running Ubuntu 22.04.1 LTS (Jammy Jellyfish), with 8 CPU cores and 256GB RAM. The time budget we use is 3 hours per app. We wish the reviewers could obtain enough resources to evaluate our artefact.

## Getting Started (in about 5 mins)
### Run Docker Image
* install Docker on your machine: https://docs.docker.com/engine/install/
* download docker image and this README.md file from `Zenodo`
* load docker image:
```
# docker load < fpc_artifact.tar.gz
```
* run the docker image:
```
# docker run -it hdjay2013/fpc:latest
```
If everything is correct, you should be in the `/FPC/` directory.
One can use the following command to create a connection directory from you host machine with the one in container.
```
# docker run --mount type=bind,source=/local/path/to/result,target=/FPC/result -it hdjay2013/fpc:latest
```

Remember to use the command below if you have encountered any requirements issues:
```
# pip3 install -r requirements.txt
```

### Directory Structure
In this artifact, 
* `android-platforms/` contains many `android.jar` files of different platform versions. They will be used by `FlowDroid` (as well as `CleanDroid` and `FPC`) when analyzing Android applications. 
* Under `benchmarks/`, we have provided all benchmarks used in our evaluation, including the ones from `DiskDroid` and `SparseDroid`. 
* `src/` contains the project of `FlowDroid`. The source code of `CleanDroid` and `FPC` are under `src/soot-infolow/src/soot/jimple/infoflow/solver/gcSolver` and `src/soot-infolow/src/soot/jimple/infoflow/solver/gcSolver/fpc`, respectively. For those who are interested in the source code of `FPC`, the algorithm in Figure 4 (in the paper) is implemented in `fpc/IFDSSolver.java` and the algorithm in Figure 6 is implemented in following files: `fpc/NormalGarbageCollector.java`, `fpc/FineGrainedReferenceCountingGarbageCollector.java`, and `fpc/AbstractionDependencyGraph.java`. We do not provide comments in those implementations since the code is very short and trivial. Note that the implementation of `fpc/AggressiveGarbageCollector.java` has been discussed in Section 3.5 in our paper.
* `soot-infoflow-cmd-jar-with-dependencies.jar` is the only executable files used in the evaluation. It can be compiled from the source code by using `mvn -DskipTests install` (the compilation result will be in `soot-infoflow-cmd/target/`).
* `sample/` includes the three runs of experimental data used in our paper. Lazy reviewers can use these provided data to reproduce all evaluation results used in our paper ^^.
* `*.py` are scripts used for evaluation.

### Test driven script
`driver.py` is the driven script for running different benchmarks with different tools (`FlowDroid`|`CleanDroid`|`FPC`). The grammar for running this script is given below:
```
cmd := ./driver.py argumentList
argumentList := argument | argument argumentList
argument := -print | -out={OUTPUT-PATH} | -st={SLEEP-TIME} | -solver={SOLVER} | APP-PATH
```
For more details, please open the script and read the code^^.

Below, we use `com.alfray.timeriffic_10905.apk` as a test benchmark to check whether `FlowDroid`, `CleanDroid`, and `FPC` can run successfully. 

+ Test `FlowDroid` (should be finished in 1 min) 
```
# ./driver.py benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk -print
```
+ Test `CleanDroid` (should be finished in 1 min)
```
# ./driver.py benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk -print -solver=GC
```
+ Test `FPC` (should be finished in 1 min)
```
# ./driver.py benchmarks/diskDroidBenchmarks/group1/com.alfray.timeriffic_10905.apk -print -solver=FPC
```
### Test Table/Figures Generation Script
`genFigTabs.py` is the script for generating figures and tables in our paper. The grammar for running this script is given below:
```
cmd := ./genFigTabs.py argumentList
argumentList := argument | argument argumentList
argument := -sample | -out={RUN-PATH}
```
We use the exprimental results (running on our server and provided in `sample`) to test this script:
```
# ./genFigTabs.py -sample
```
The command should generate the following files: `adgSize.pdf`, `tp.pdf`, `mp.pdf`, `speedupsOverFD.pdf`, `SpeedUpMemInterval.pdf`, and `table1.tex`. Just use the following command to compile `table1.tex` into a PDF file:
```
# xelatex table1.tex
```
The table below maps the generated files with their names used in the paper:
| File Name in Artifact  | File Name in Paper |
| ---------------------- | ------------------ |
| table1.pdf             | Table 1            |
| mp.pdf                 | Figure 7           |
| adgSize.pdf            | Figure 8           |
| speedupsOverFD.pdf     | Figure 9           |
| tp.pdf                 | Figure 10          |
| SpeedUpMemInterval.pdf | Figure 11          |

## Detailed Instructions
It is ready to evaluate our artifact. The evaluation contains three steps:

+ Step 1: use `runBen.py` (which invokes `driver.py`) to obtain execution results produced by `FlowDroid`, `CleanDroid`, and `FPC` on each benchmarks under each setting. This step will take most of your time.
+ Step 2: use `genFigTabs.py` to generate Tables and Figures by using the output of `runBen.py` (under `output` directory by default).
+ Step 3: using the generated figures and tables to validate our paper claims.
  
### Step 1: run `runBen.py` (in about 4 days)
In `runBen.py`, the `appPaths` list includes all the benchmarks evaluated in our paper. Note that different machine with diffent CPU and Memory may result in different analysis time, memory consumption, and scalability. However, the conclusion that `FPC` is more efficient than `CleanDroid` and `FlowDroid` can be guaranteed.

The apps in `appPaths` are ordered in ascending order by their analysis time of `CleanDroid`. For reviewers who could not evaluate some large apps, please comment them in `appPaths` since validating the claim of our paper does not require to reproduce all apps (although `FPC` is more efficient on large apps).

Let us start by running following command (full executions require about 4 days (mainly due to the last 7 apps in Table 1)):
```
# mkdir output
# ./runBen.py
```
The experimental results are saved in `output` by default. Reviewers can change this value by modifing the variable `run` in `runBen.py`.


### Step 2: generate tables and figures (in less than 5 seconds)
just run the following commands:
```
# python3 genFigTabs.py -out=output/
# xelatex table1.tex
```

The files and their corresponding names used in the paper have already given in the table above.

### Step 3: validate paper claims (in 1 mins)
The paper makes the following claims:
* `FPC` can collect more path edges than `CleanDroid` (evidenced by `table1.pdf`, `mp.pdf`, `tp.pdf`).
* `FPC` is more efficient than `CleanDroid` in both analysis time and memory consumption (evidenced by `table1.pdf`, `mp.pdf`, `tp.pdf`, and `speedupsOverFD.pdf`).
* Overhead of `FPC` is small (evidenced by `adgSize.pdf` and  `SpeedUpMemInterval.pdf`).

That's all. Have fun.
