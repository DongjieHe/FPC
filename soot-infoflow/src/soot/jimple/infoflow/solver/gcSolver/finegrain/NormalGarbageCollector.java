package soot.jimple.infoflow.solver.gcSolver.finegrain;

import heros.solver.Pair;
import heros.solver.PathEdge;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import soot.SootMethod;
import soot.jimple.infoflow.collect.MyConcurrentHashMap;
import soot.jimple.infoflow.solver.cfg.BackwardsInfoflowCFG;
import soot.jimple.infoflow.solver.gcSolver.IGCReferenceProvider;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

import java.util.Map;
import java.util.Set;

public class NormalGarbageCollector<N, D> extends FineGrainedReferenceCountingGarbageCollector<N, D>{
    protected final AbstrationDependencyGraph<D> abstDependencyGraph;
    protected final MyConcurrentHashMap<Pair<SootMethod, D>, Map<Pair<N, D>, D>> endSummary;

    public NormalGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions,
                                  MyConcurrentHashMap<Pair<SootMethod, D>, Map<Pair<N, D>, D>> endSummary, AbstrationDependencyGraph<D> adg) {
        super(icfg, jumpFunctions, null);
        this.abstDependencyGraph = adg;
        this.endSummary = endSummary;
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
            // we actually can remove these nodes.
//            Set<Pair<SootMethod, D>> references = abstDependencyGraph.reachableClosure(abstraction);
//            for (Pair<SootMethod, D> ref : references) {
//                abstDependencyGraph.remove(ref);
//            }
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

    protected static final Logger logger = LoggerFactory.getLogger(NormalGarbageCollector.class);
    @Override
    public void notifySolverTerminated() {
        super.notifySolverTerminated();
        String s = "forward";
        if (icfg instanceof BackwardsInfoflowCFG) {
            s = "backward";
        }
        logger.info(icfg.getClass().toString());
        logger.info(String.format("#nodes of %s Abstraction Dependency Graph: %d", s, abstDependencyGraph.nodeSize()));
        logger.info(String.format("#edges of %s Abstraction Dependency Graph: %d", s, abstDependencyGraph.edgeSize()));
        logger.info(String.format("#dummy end summary edges of %s: %d", s, this.endSummary.keySet().size()));
        long v = 0;
        for(Map<Pair<N, D>, D> m : this.endSummary.values()) {
            v += m.size();
        }
        logger.info(String.format("#end summary edges of %s: %d", s, v));
    }
}
