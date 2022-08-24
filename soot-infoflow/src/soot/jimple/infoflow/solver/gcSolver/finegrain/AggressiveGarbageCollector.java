package soot.jimple.infoflow.solver.gcSolver.finegrain;

import heros.solver.Pair;
import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.solver.gcSolver.AbstractReferenceCountingGarbageCollector;
import soot.jimple.infoflow.solver.gcSolver.IGCReferenceProvider;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

public class AggressiveGarbageCollector<N, D> extends AbstractReferenceCountingGarbageCollector<N, D, Pair<SootMethod, D>> {
    public AggressiveGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions, IGCReferenceProvider<D, N> referenceProvider) {
        super(icfg, jumpFunctions, referenceProvider);
    }

    public AggressiveGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions) {
        super(icfg, jumpFunctions);
    }

    private class GCThread extends Thread {

        private boolean finished = false;

        public GCThread() {
            setName("Fine-grained aggressive IFDS Garbage Collector");
        }

        @Override
        public void run() {
            while (!finished) {
                gcImmediate();

                if (sleepTimeSeconds > 0) {
                    try {
                        Thread.sleep(sleepTimeSeconds * 1000);
                    } catch (InterruptedException e) {
                        break;
                    }
                }
            }
        }

        /**
         * Notifies the thread to finish its current garbage collection and then
         * terminate
         */
        public void finish() {
            finished = true;
            interrupt();
        }

    }

    private int sleepTimeSeconds = 1;
    private int maxPathEdgeCount = 0;
    private int maxMemoryConsumption = 0;

    private GCThread gcThread;


    @Override
    protected void initialize() {
        super.initialize();

        // Start the garbage collection thread
        gcThread = new GCThread();
        gcThread.start();
    }

    @Override
    public void gc() {
        // nothing to do here
    }

    @Override
    public void notifySolverTerminated() {
        gcImmediate();
        gcThread.finish();
    }

    /**
     * Sets the time to wait between garbage collection cycles in seconds
     *
     * @param sleepTimeSeconds The time to wait between GC cycles in seconds
     */
    public void setSleepTimeSeconds(int sleepTimeSeconds) {
        this.sleepTimeSeconds = sleepTimeSeconds;
    }

    private int getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return (int) Math.round((runtime.totalMemory() - runtime.freeMemory()) / 1E6);
    }

    public long getMaxPathEdgeCount() {
        return this.maxPathEdgeCount;
    }

    public int getMaxMemoryConsumption() {
        return this.maxMemoryConsumption;
    }

    @Override
    protected void onAfterRemoveEdges(int gcedMethods) {
        int pec = 0;
        for(Integer i : jumpFnCounter.values()) {
            pec += i;
        }
        this.maxPathEdgeCount = Math.max(this.maxPathEdgeCount, pec);
        this.maxMemoryConsumption = Math.max(this.maxMemoryConsumption, getUsedMemory());
    }

    @Override
    protected Pair<SootMethod, D> genAbstraction(PathEdge<N, D> edge) {
        SootMethod method = icfg.getMethodOf(edge.getTarget());
        return new Pair<>(method, edge.factAtSource());
    }

    @Override
    public boolean hasActiveDependencies(Pair<SootMethod, D> abstraction) {
        int changeCounter = -1;
        do {
            // Update the change counter for the next round
            changeCounter = jumpFnCounter.getChangeCounter();

            // Check the method itself
            if (jumpFnCounter.get(abstraction) > 0)
                return true;

        } while (checkChangeCounter && changeCounter != jumpFnCounter.getChangeCounter());
        return false;
    }
}
