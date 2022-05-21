package soot.jimple.infoflow.solver.onlineSolver;

import java.util.Map;
import java.util.Map.Entry;

import heros.solver.Pair;
import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.solver.fastSolver.FastSolverLinkedNode;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;

public class AggressivePartitionMananger<N, D extends FastSolverLinkedNode<D, N>, I extends BiDiInterproceduralCFG<N, SootMethod>>
	extends AbstractPartitionManager<N, D, I> {

	public AggressivePartitionMananger(I icfg) {
		super(icfg);
	}

	@Override
	public D addPathEdge(D d1, N n, D d2) {
		if (icfg.isExitStmt(n) || icfg.isCallStmt(n) || loopHeaderQuerier.isLoopEntry(n)) {
			SootMethod m = icfg.getMethodOf(n);
			Partitions p = pathEdges.putIfAbsentElseGet(new Pair<>(m, d1), Partitions::new);
			return p.insert(n, d2);
		}
		return null;
	}

	@Override
	public void increaseReferenceCount(D d1, N n, D d2) {
		if (icfg.isExitStmt(n) || icfg.isCallStmt(n) || loopHeaderQuerier.isLoopEntry(n)) {
			SootMethod m = icfg.getMethodOf(n);
			Partitions p = pathEdges.get(new Pair<>(m, d1));
			p.refCount.incrementAndGet();
		}
	}

	@Override
	public void decreaseReferenceCount(D d1, N n, D d2) {
		if (!(icfg.isExitStmt(n) && icfg.isCallStmt(n) && loopHeaderQuerier.isLoopEntry(n)))
			return;

		SootMethod m = icfg.getMethodOf(n);
		Pair<SootMethod, D> alpha = new Pair<>(m, d1);
		Partitions p = pathEdges.get(alpha);
		p.refCount.decrementAndGet();

		if (p.refCount.get() == p.callEdges.size()) {
			p.headerEdges.clear();

			// check ref counts for forward and backward solver
			if (solverPeerGroup.checkRemovalCondition(alpha)) {
				p.clear();

				Map<N, Map<D, D>> inc = getIncoming(m, d1);
				if (inc != null && !inc.isEmpty()) {
					for (Entry<N, Map<D, D>> entry : inc.entrySet()) {
						for (Entry<D, D> facts: entry.getValue().entrySet()) {
							PathEdge<N, D> callPathEdge = new PathEdge<>(facts.getKey(), entry.getKey(), facts.getValue());
							decreaseWaitCount(callPathEdge);
						}
					}
				}
			}
		}
	}

}
