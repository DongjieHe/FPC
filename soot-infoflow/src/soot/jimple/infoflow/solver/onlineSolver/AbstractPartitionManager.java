package soot.jimple.infoflow.solver.onlineSolver;

import java.util.Map;
import java.util.Set;
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

	protected static final Logger logger = LoggerFactory.getLogger(AbstractPartitionManager.class);

	protected class Partitions {
		public AtomicLong refCount = new AtomicLong();
		protected final Map<Pair<N, D>, D> selfLoops = new ConcurrentHashMap<>();
		protected final Map<Pair<N, D>, D> callEdges = new ConcurrentHashMap<>();
		protected final Map<Pair<N, D>, D> headerEdges = new ConcurrentHashMap<>();
		protected final Map<Pair<N, D>, D> otherEdges = new ConcurrentHashMap<>();
		protected final Map<Pair<N, D>, D> endSummary = new ConcurrentHashMap<>();

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

		public boolean contains(N n, D d2) {
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

	public void cleanup() {
		this.pathEdges.clear();
		this.incoming.clear();
		this.waitingCount.clear();
	}

	public AbstractPartitionManager(I icfg) {
		this.icfg = icfg;
		this.loopHeaderQuerier = new LoopHeaderQuerier<>(icfg);
	}

	abstract public D addPathEdge(D d1, N n, D d2);

	public void initWaitCount(PathEdge<N, D> edge) {
		waitingCount.putIfAbsent(edge, new AtomicLong(0));
	}

	public long getCurrentWaitCount(PathEdge<N, D> edge) {
		return waitingCount.get(edge).get();
	}

	public void increaseWaitCount(PathEdge<N, D> edge) {
		waitingCount.get(edge).incrementAndGet();
	}

	public void decreaseWaitCount(PathEdge<N, D> edge) {
		AtomicLong wc = waitingCount.get(edge);
		// wc is not null means this call edge has an associated wait counting
		if (wc != null && wc.decrementAndGet() == 0) {
			decreaseReferenceCount(edge.factAtSource(), edge.getTarget(), edge.factAtTarget());
		}
	}

	abstract public void increaseReferenceCount(D d1, N n, D d2);

	abstract public void decreaseReferenceCount(D d1, N n, D d2);

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

	public void removeIncoming(SootMethod m, D d1) {
		incoming.remove(new Pair<>(m, d1));
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

	public void setPeerGroup(OnlineSolverPeerGroup solverPeerGroup) {
		this.solverPeerGroup = solverPeerGroup;
	}

	public void printPartitions() {
		for (Map.Entry<Pair<SootMethod, D>, Partitions> entry: pathEdges.entrySet()) {
			logger.info(entry.getValue().refCount.get() + " - " + entry.getKey().getO1() + " with " + entry.getKey().getO2());
			logger.info(String.format("\t#self loop: %d, #call edge: %d, #loop header: %d, #others: %d, #summary: %d",
				entry.getValue().selfLoops.size(),
				entry.getValue().callEdges.size(),
				entry.getValue().headerEdges.size(),
				entry.getValue().otherEdges.size(),
				entry.getValue().endSummary.size()));
		}

		long cnt = 0;
		for (Map.Entry<PathEdge<N, D>, AtomicLong> entry: waitingCount.entrySet()) {
			if (entry.getValue().get() != 0)
				cnt += 1;
		}
		logger.info(String.format("#wc != 0 / #calledges = %d / %d", cnt, waitingCount.size()));
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
