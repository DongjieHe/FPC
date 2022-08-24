package soot.jimple.infoflow.solver.gcSolver.finegrain;

import heros.solver.Pair;
import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.solver.gcSolver.IGCReferenceProvider;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

public class NormalGarbageCollector<N, D> extends FineGrainedReferenceCountingGarbageCollector<N, D>{
    public NormalGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg, ConcurrentHashMultiMap<Pair<SootMethod, D>, PathEdge<N, D>> jumpFunctions, IGCReferenceProvider referenceProvider) {
        super(icfg, jumpFunctions, referenceProvider);
    }

    @Override
    public boolean hasActiveDependencies(Pair<SootMethod, D> abstraction) {
        // TODO
        return false;
    }

    @Override
    protected IGCReferenceProvider<Pair<SootMethod, D>> createReferenceProvider() {
        // TODO
        return null;
    }
}
