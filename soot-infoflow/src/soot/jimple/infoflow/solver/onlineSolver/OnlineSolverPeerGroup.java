package soot.jimple.infoflow.solver.onlineSolver;

import java.util.Collection;
import java.util.HashSet;

import heros.solver.Pair;
import soot.SootMethod;
import soot.jimple.infoflow.solver.IInfoflowSolver;
import soot.jimple.infoflow.solver.SolverPeerGroup;
import soot.jimple.infoflow.solver.fastSolver.FastSolverLinkedNode;

public class OnlineSolverPeerGroup extends SolverPeerGroup {

	Collection<AbstractPartitionManager<?, ?, ?>> managers;

	public OnlineSolverPeerGroup() {
		this.managers = new HashSet<>();
	}

	@Override
	public void addSolver(IInfoflowSolver solver) {
		InfoflowSolver onlineSolver = (InfoflowSolver) solver;
		this.managers.add(onlineSolver.getPartitionManager());
	}

	public <D extends FastSolverLinkedNode<D, ?>> boolean checkRemovalCondition(Pair<SootMethod, D> alpha) {
		for (AbstractPartitionManager<?, ?, ?> manager: managers) {
			@SuppressWarnings("unchecked")
			AbstractPartitionManager<?, D, ?> m = (AbstractPartitionManager<?, D, ?>) manager;
			if (m.hasAssociatedPathEdges(alpha))
				return false;
		}
		return true;
	}
}
