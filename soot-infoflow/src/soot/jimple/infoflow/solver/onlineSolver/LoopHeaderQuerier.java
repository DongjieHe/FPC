package soot.jimple.infoflow.solver.onlineSolver;

import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import soot.SootMethod;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.toolkits.graph.DirectedGraph;
import soot.toolkits.graph.MHGDominatorsFinder;

public class LoopHeaderQuerier<N, I extends BiDiInterproceduralCFG<N, SootMethod>> {

	protected I icfg;

	protected ConcurrentHashMap<SootMethod, Set<N>> loopHeaders;

	public LoopHeaderQuerier(I icfg) {
		this.icfg = icfg;
		loopHeaders = new ConcurrentHashMap<>();
	}

	public boolean isLoopEntry(N n) {
		SootMethod sm = icfg.getMethodOf(n);
		Set<N> headers = loopHeaders.get(sm);
		if (headers == null) {
			headers = getLoopheaders(icfg.getOrCreateUnitGraph(sm));
			loopHeaders.put(sm, headers);
		}
		return headers.contains(n);
	}

	private Set<N> getLoopheaders(DirectedGraph<N> g) {
		MHGDominatorsFinder<N> a = new MHGDominatorsFinder<N>(g);
		Set<N> loopHeaders = new HashSet<>();

		Iterator<N> iter = g.iterator();
		while (iter.hasNext()) {
			N n = iter.next();
			List<N> succs = g.getSuccsOf(n);
			List<N> dominators = a.getDominators(n);

			for (N succ : succs) {
				if (dominators.contains(succ)) {
					loopHeaders.add(succ);
				}
			}
		}

		return loopHeaders;
	}
}
