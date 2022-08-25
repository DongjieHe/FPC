package soot.jimple.infoflow.solver.gcSolver.finegrain;

import heros.solver.Pair;
import heros.solver.PathEdge;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import soot.SootMethod;
import soot.jimple.infoflow.solver.gcSolver.GarbageCollectionTrigger;
import soot.jimple.infoflow.solver.gcSolver.IGCReferenceProvider;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

import java.util.Set;

public class NormalGarbageCollector<N, D> extends FineGrainedReferenceCountingGarbageCollector<N, D>{
    protected final AbstrationDependencyGraph<D> abstDependencyGraph;

    public NormalGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions, AbstrationDependencyGraph<D> adg) {
        super(icfg, jumpFunctions, null);
        this.abstDependencyGraph = adg;
    }

    @Override
    public boolean hasActiveDependencies(Pair<SootMethod, D> abstraction) {
        int changeCounter = -1;
        try {
            abstDependencyGraph.lock();
            do {
                // Update the change counter for the next round
                changeCounter = jumpFnCounter.getChangeCounter();

                // Check the method itself
                if (jumpFnCounter.get(abstraction) > 0)
                    return true;

                // Check the transitive callees
                Set<Pair<SootMethod, D>> references = abstDependencyGraph.reachableClosure(abstraction);
                for (Pair<SootMethod, D> ref : references) {
                    if (jumpFnCounter.get(ref) > 0)
                        return true;
                }
            } while (checkChangeCounter && changeCounter != jumpFnCounter.getChangeCounter());
        } finally {
            abstDependencyGraph.unlock();
        }
        return false;
    }

    @Override
    protected IGCReferenceProvider<Pair<SootMethod, D>> createReferenceProvider() {
        // TODO
        return null;
    }

//    @Override
//    /**
//     * Immediately performs garbage collection
//     */
//    protected void gcImmediate() {
//        if (gcScheduleSet != null && !gcScheduleSet.isEmpty()) {
//            // Check our various triggers for garbage collection
//            boolean gc = trigger == GarbageCollectionTrigger.Immediate;
//            gc |= trigger == GarbageCollectionTrigger.MethodThreshold && gcScheduleSet.size() > methodThreshold;
//            gc |= trigger == GarbageCollectionTrigger.EdgeThreshold && edgeCounterForThreshold.get() > edgeThreshold;
//
//            // Perform the garbage collection if required
//            if (gc) {
//                int tempMethods = 0;
//                onBeforeRemoveEdges();
//                for (Pair<SootMethod, D> abst : gcScheduleSet) {
//                    // Is it safe to remove this method?
//                    if (peerGroup != null) {
//                        if (peerGroup.hasActiveDependencies(abst))
//                            continue;
//                    } else if (hasActiveDependencies(abst))
//                        continue;
//
//                    // Get stats for the stuff we are about to remove
//                    Set<PathEdge<N, D>> oldFunctions = jumpFunctions.get(abst);
//                    if (oldFunctions != null) {
//                        int gcedSize = oldFunctions.size();
//                        gcedEdges.addAndGet(gcedSize);
//                        if (trigger == GarbageCollectionTrigger.EdgeThreshold)
//                            edgeCounterForThreshold.subtract(gcedSize);
//                    }
//
//                    // First unregister the method, then delete the edges. In case some other thread
//                    // concurrently schedules a new edge, the method gets back into the GC work list
//                    // this way.
//                    gcScheduleSet.remove(abst);
//                    if (jumpFunctions.remove(abst)) {
//                        gcedMethods.incrementAndGet();
//                        tempMethods++;
//                        if (validateEdges)
//                            oldEdges.addAll(oldFunctions);
//                    }
//                }
//                onAfterRemoveEdges(tempMethods);
//            }
//        }
//    }

    protected static final Logger logger = LoggerFactory.getLogger(NormalGarbageCollector.class);
    @Override
    public void notifySolverTerminated() {
        super.notifySolverTerminated();
        logger.info(String.format("#nodes of Abstraction Dependency Graph: %d", abstDependencyGraph.nodeSize()));
        logger.info(String.format("#edges of Abstraction Dependency Graph: %d", abstDependencyGraph.edgeSize()));
    }
}
