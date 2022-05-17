package soot.jimple.infoflow.solver.onlineSolver;

public class ThreadedMemAndPEMonitor {
    private class ThreadedMonitor extends Thread {

        private boolean finished = false;

        public ThreadedMonitor() {
            setName("Threaded Memory and PathEdge Monitor");
        }

        @Override
        public void run() {
            while (!finished) {
                computeImmediate();

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
    private OnlineSolverPeerGroup peerGroup;

    private final ThreadedMonitor monitor;

    public ThreadedMemAndPEMonitor(OnlineSolverPeerGroup peerGroup) {
        this.peerGroup = peerGroup;
        monitor = new ThreadedMonitor();
        monitor.start();
    }

    public void computeImmediate() {
        int pec = 0;
        for(AbstractPartitionManager<?, ?, ?> mgr : peerGroup.getManagers()) {
            pec += mgr.getPathEdgeCount();
        }
        this.maxPathEdgeCount = Math.max(this.maxPathEdgeCount, pec);
        this.maxMemoryConsumption = Math.max(this.maxMemoryConsumption, getUsedMemory());
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

    public void notifySolverTerminated() {
        computeImmediate();
        monitor.finish();
    }

    /**
     * Sets the time to wait between garbage collection cycles in seconds
     *
     * @param sleepTimeSeconds The time to wait between GC cycles in seconds
     */
    public void setSleepTimeSeconds(int sleepTimeSeconds) {
        this.sleepTimeSeconds = sleepTimeSeconds;
    }

}
