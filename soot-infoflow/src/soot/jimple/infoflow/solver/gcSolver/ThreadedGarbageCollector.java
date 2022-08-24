package soot.jimple.infoflow.solver.gcSolver;

import heros.solver.PathEdge;
import soot.SootMethod;
import soot.jimple.infoflow.solver.onlineSolver.AbstractPartitionManager;
import soot.jimple.toolkits.ide.icfg.BiDiInterproceduralCFG;
import soot.util.ConcurrentHashMultiMap;

/**
 * Garbage collector that performs its tasks in a separate thread
 * 
 * @author Steven Arzt
 *
 * @param <N>
 * @param <D>
 */
public class ThreadedGarbageCollector<N, D> extends MethodLevelReferenceCountingGarbageCollector<N, D> {

	private class GCThread extends Thread {

		private boolean finished = false;

		public GCThread() {
			setName("IFDS Garbage Collector");
		}

		@Override
		public void run() {
			while (!finished) {
				gcImmediate();

				if (sleepTimeSeconds > 0) {
					try {
						Thread.sleep(sleepTimeSeconds * 1000);
					} catch (InterruptedException e) {
						break;
					}
				}
			}
		}

		/**
		 * Notifies the thread to finish its current garbage collection and then
		 * terminate
		 */
		public void finish() {
			finished = true;
			interrupt();
		}

	}

	private int sleepTimeSeconds = 1;
	private int maxPathEdgeCount = 0;
	private int maxMemoryConsumption = 0;

	private GCThread gcThread;

	public ThreadedGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg,
			ConcurrentHashMultiMap<SootMethod, PathEdge<N, D>> jumpFunctions,
			IGCReferenceProvider referenceProvider) {
		super(icfg, jumpFunctions, referenceProvider);
	}

	public ThreadedGarbageCollector(BiDiInterproceduralCFG<N, SootMethod> icfg,
			ConcurrentHashMultiMap<SootMethod, PathEdge<N, D>> jumpFunctions) {
		super(icfg, jumpFunctions);
	}

	@Override
	protected void initialize() {
		super.initialize();

		// Start the garbage collection thread
		gcThread = new GCThread();
		gcThread.start();
	}

	@Override
	public void gc() {
		// nothing to do here
	}

	@Override
	public void notifySolverTerminated() {
		gcImmediate();
		gcThread.finish();
	}

	/**
	 * Sets the time to wait between garbage collection cycles in seconds
	 * 
	 * @param sleepTimeSeconds The time to wait between GC cycles in seconds
	 */
	public void setSleepTimeSeconds(int sleepTimeSeconds) {
		this.sleepTimeSeconds = sleepTimeSeconds;
	}

	private int getUsedMemory() {
		Runtime runtime = Runtime.getRuntime();
		return (int) Math.round((runtime.totalMemory() - runtime.freeMemory()) / 1E6);
	}

	public long getMaxPathEdgeCount() {
		return this.maxPathEdgeCount;
	}

	public int getMaxMemoryConsumption() {
		return this.maxMemoryConsumption;
	}

	@Override
	protected void onAfterRemoveEdges(int gcedMethods) {
		int pec = 0;
		for(Integer i : jumpFnCounter.values()) {
			pec += i;
		}
		this.maxPathEdgeCount = Math.max(this.maxPathEdgeCount, pec);
		this.maxMemoryConsumption = Math.max(this.maxMemoryConsumption, getUsedMemory());
	}
}
