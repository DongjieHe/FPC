FROM hdjay2013/jupx:v8
ENV workdir /FPC
WORKDIR $workdir
ENV user root
USER $user
COPY artifacts/android-platforms/ $workdir/android-platforms/
COPY artifacts/benchmarks/sparsedroidBenchmark/ $workdir/benchmarks/sparsedroidBenchmark/
COPY artifacts/benchmarks/diskDroidBenchmarks/ $workdir/benchmarks/diskDroidBenchmarks/
COPY artifacts/sample/ $workdir/sample/
COPY artifacts/soot-infoflow-cmd-jar-with-dependencies.jar $workdir/soot-infoflow-cmd-jar-with-dependencies.jar
COPY artifacts/SourcesAndSinks.txt $workdir/SourcesAndSinks.txt
COPY artifacts/*.py $workdir/
COPY artifacts/LICENSE $workdir/
CMD /bin/bash
