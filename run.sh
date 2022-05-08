#!/bin/bash

mvn -DskipTests install
mv soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar artifacts/
