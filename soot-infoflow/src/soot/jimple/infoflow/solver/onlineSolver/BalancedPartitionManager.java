package soot.jimple.infoflow.solver.onlineSolver;

import soot.SootMethod;
import soot.jimple.infoflow.solver.fastSolver.FastSolverLinkedNode;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;

public class BalancedPartitionManager<N, D extends FastSolverLinkedNode<D, N>, I extends BiDiInterproceduralCFG<N, SootMethod>> 
	extends AbstractPartitionManager<N, D, I> {

	public BalancedPartitionManager(I icfg) {
		super(icfg);
	}

}
