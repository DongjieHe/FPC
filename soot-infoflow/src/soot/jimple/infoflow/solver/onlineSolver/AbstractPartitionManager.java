package soot.jimple.infoflow.solver.onlineSolver;

import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import heros.solver.Pair;
import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.collect.MyConcurrentHashMap;
import soot.jimple.infoflow.solver.fastSolver.FastSolverLinkedNode;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;

public abstract class AbstractPartitionManager<N, D extends FastSolverLinkedNode<D, N>, I extends BiDiInterproceduralCFG<N, SootMethod>> {

	protected final I icfg;

	protected final LoopHeaderQuerier<N, I> loopHeaderQuerier;

	protected OnlineSolverPeerGroup solverPeerGroup;

	protected AtomicLong maxPathEdgeNum = new AtomicLong();

	protected static final Logger logger = LoggerFactory.getLogger(AbstractPartitionManager.class);

	protected class Partitions {
		public AtomicLong refCount = new AtomicLong();
		public Map<Pair<N, D>, D> selfLoops = new ConcurrentHashMap<>();
		public Map<Pair<N, D>, D> callEdges = new ConcurrentHashMap<>();
		public Map<Pair<N, D>, D> headerEdges = new ConcurrentHashMap<>();
		public Map<Pair<N, D>, D> otherEdges = new ConcurrentHashMap<>();
		public Map<Pair<N, D>, D> endSummary = new ConcurrentHashMap<>();

		private Map<Pair<N, D>, D> select(N stmt) {
			if (icfg.isStartPoint(stmt))
				return selfLoops;
			if (icfg.isCallStmt(stmt))
				return callEdges;
			if (icfg.isExitStmt(stmt))
				return endSummary;
			if (loopHeaderQuerier.isLoopEntry(stmt))
				return headerEdges;
			return otherEdges;
		}

		public D insert(N n, D d2) {
			return select(n).putIfAbsent(new Pair<>(n, d2), d2);
		}

		public boolean containts(N n, D d2) {
			return select(n).containsKey(new Pair<>(n, d2));
		}

		public void clear() {
			selfLoops.clear();
			otherEdges.clear();
			headerEdges.clear();
			callEdges.clear();
		}

		public long size() {
			return selfLoops.size() + callEdges.size() + headerEdges.size() 
				+ otherEdges.size() + endSummary.size();
		}
	}

	protected final MyConcurrentHashMap<Pair<SootMethod, D>, Partitions> pathEdges = new MyConcurrentHashMap<>();

	protected final MyConcurrentHashMap<Pair<SootMethod, D>, MyConcurrentHashMap<N, Map<D, D>>> incoming = new MyConcurrentHashMap<>();

	protected final MyConcurrentHashMap<PathEdge<N, D>, AtomicLong> waitingCount = new MyConcurrentHashMap<>();

	public AbstractPartitionManager(I icfg) {
		this.icfg = icfg;
		this.loopHeaderQuerier = new LoopHeaderQuerier<>(icfg);
	}

	public D addPathEdge(D d1, N n, D d2) {
		SootMethod m = icfg.getMethodOf(n);
		Partitions p = pathEdges.putIfAbsentElseGet(new Pair<>(m, d1), Partitions::new);
		return p.insert(n, d2);
	}

	public boolean containsPathEdge(D d1, N n, D d2) {
		SootMethod m = icfg.getMethodOf(n);
		Partitions p = pathEdges.get(new Pair<>(m, d1));
		if (p == null)
			return false;
		return p.containts(n, d2);
	}

	public void initWaitCount(PathEdge<N, D> edge) {
		waitingCount.put(edge, new AtomicLong());
	}

	public void increaseWaitCount(PathEdge<N, D> edge) {
		waitingCount.get(edge).incrementAndGet();
	}

	public void decreaseWaitCount(PathEdge<N, D> edge) {
		AtomicLong wc = waitingCount.get(edge);
		// wc is not null means this call edge has an assciated wait counting
		if (wc != null && wc.decrementAndGet() == 0) {
			decreaseReferenceCount(edge.factAtSource(), edge.getTarget(), edge.factAtTarget());
		}
	}

	public void increaseReferenceCount(D d1, N n, D d2) {
		SootMethod m = icfg.getMethodOf(n);
		Partitions p = pathEdges.get(new Pair<>(m, d1));
		p.refCount.incrementAndGet();
	}

	public void decreaseReferenceCount(D d1, N n, D d2) {
		if (icfg.isCallStmt(n) && waitingCount.get(new PathEdge<N, D>(d1, n, d2)).get() != 0)
			return;

		SootMethod m = icfg.getMethodOf(n);
		Pair<SootMethod, D> alpha = new Pair<>(m, d1);
		Partitions p = pathEdges.get(alpha);
		p.refCount.decrementAndGet();

		// check ref counts for forward and backward solver
		if (solverPeerGroup.checkRemovalCondition(alpha)) {
			updateMaxPathEdgeNum();
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

	public boolean checkSourceAbstraction(SootMethod m, D d1) {
		Partitions p = pathEdges.get(new Pair<>(m, d1));
		return p == null || p.refCount.get() > 0;
	}

	public Set<Pair<N, D>> getEndSummary(SootMethod m, D d3) {
		Partitions p = pathEdges.get(new Pair<>(m, d3));
		if (p == null)
			return null;
		return p.endSummary.keySet();
	}

	public Map<N, Map<D, D>> getIncoming(SootMethod m, D d1) {
		return incoming.get(new Pair<>(m, d1));
	}

	public boolean addIncoming(SootMethod m, D d3, N n, D d1, D d2) {
		MyConcurrentHashMap<N, Map<D, D>> summaries = incoming.putIfAbsentElseGet(new Pair<>(m, d3),
				MyConcurrentHashMap::new);
		Map<D, D> set = summaries.putIfAbsentElseGet(n, ConcurrentHashMap::new);
		return set.put(d1, d2) == null;
	}

	public boolean hasAssociatedPathEdges(Pair<SootMethod, D> alpha) {
		Partitions p = pathEdges.get(alpha);
		if (p == null)
			return false;
		return p.refCount.get() != 0;
	}

	public long size() {
		long result = 0;
		for (Partitions p: pathEdges.values()) {
			result += p.size();
		}
		return result;
	}

	protected void updateMaxPathEdgeNum() {
		long cur = size();
		if (maxPathEdgeNum.get() < cur) {
			maxPathEdgeNum.set(cur);
//			if (loopHeaderQuerier.direction)
//				logger.info("f cur = " + cur + ", max = " + maxPathEdgeNum.get());
//			else
//				logger.info("b cur = " + cur + ", max = " + maxPathEdgeNum.get());
		}
	}

	public long getMaxPathEdgeNum() {
		return maxPathEdgeNum.get();
	}

	public void setPeerGroup(OnlineSolverPeerGroup solverPeerGroup) {
		this.solverPeerGroup = solverPeerGroup;
	}

	public void printPartitions() {
		for (Map.Entry<Pair<SootMethod, D>, Partitions> entry: pathEdges.entrySet()) {
			logger.info(entry.getKey().getO1().toString() + " -> " + entry.getValue().size());
		}
	}

	public OnlineSolverPeerGroup getSolverPeerGroup() {
		return this.solverPeerGroup;
	}

	public long getPathEdgeCount() {
		long ret = 0;
		for(Partitions p: pathEdges.values()) {
			ret += p.size();
		}
		return ret;
	}
}
