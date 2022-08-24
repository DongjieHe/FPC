package soot.jimple.infoflow.solver.gcSolver.finegrain;

import heros.solver.Pair;
import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.solver.gcSolver.IGCReferenceProvider;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

public class AggressiveGarbageCollector<N, D> extends FineGrainedReferenceCountingGarbageCollector<N, D> {
    public AggressiveGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions, IGCReferenceProvider<D, N> referenceProvider) {
        super(icfg, jumpFunctions, referenceProvider);
    }

    public AggressiveGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions) {
        super(icfg, jumpFunctions);
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
