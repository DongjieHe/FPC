FROM hdjay2013/jupx:v8
ENV workdir /FPC
WORKDIR $workdir
ENV user root
USER $user
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install maven -y
COPY artifacts/android-platforms/ $workdir/android-platforms/
COPY artifacts/benchmarks/sparsedroidBenchmark/ $workdir/benchmarks/sparsedroidBenchmark/
COPY artifacts/benchmarks/diskDroidBenchmarks/ $workdir/benchmarks/diskDroidBenchmarks/
COPY artifacts/sample/ $workdir/sample/
COPY artifacts/soot-infoflow-cmd-jar-with-dependencies.jar $workdir/soot-infoflow-cmd-jar-with-dependencies.jar
COPY artifacts/SourcesAndSinks.txt $workdir/SourcesAndSinks.txt
COPY artifacts/requirements.txt $workdir/requirements.txt
COPY artifacts/*.py $workdir/
COPY artifacts/LICENSE $workdir/
# prepare sources
COPY soot-infoflow/ ${workdir}/src/soot-infoflow/
COPY soot-infoflow-cmd/ ${workdir}/src/soot-infoflow-cmd/
COPY soot-infoflow-android/ ${workdir}/src/soot-infoflow-android/
COPY soot-infoflow-summaries/ ${workdir}/src/soot-infoflow-summaries/
COPY pom.xml ${workdir}/src/pom.xml
# COPY run.sh ${workdir}/src/run.sh
COPY README.MD ${workdir}/src/README.MD
CMD /bin/bash
