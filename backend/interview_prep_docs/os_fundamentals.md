# Operating Systems Interview Q&A

## Question: What is the difference between a process and a thread?
A process is an independent program in execution with its own memory space (isolated from other processes). A thread is a lightweight unit of execution within a process, sharing the process's memory space with other threads of the same process. Threads are cheaper to create and switch between since they share resources, but that shared memory also makes them prone to race conditions.

## Question: Explain the difference between multiprocessing and multithreading.
Multiprocessing runs multiple processes in parallel, each with isolated memory — true parallelism on multi-core CPUs, but higher overhead for creation and inter-process communication. Multithreading runs multiple threads within a single process sharing memory — lower overhead, but in Python specifically, the Global Interpreter Lock (GIL) prevents true parallel execution of threads for CPU-bound tasks (though it's fine for I/O-bound tasks).

## Question: What is a deadlock and what are its four necessary conditions?
A deadlock occurs when two or more processes are stuck waiting for each other indefinitely. Four necessary conditions (Coffman conditions) must all hold: Mutual Exclusion (resources can't be shared), Hold and Wait (a process holds a resource while waiting for another), No Preemption (resources can't be forcibly taken away), and Circular Wait (a cycle of processes each waiting on the next).

## Question: What is virtual memory and why is it used?
Virtual memory is an abstraction that gives each process the illusion of having its own large, contiguous address space, independent of actual physical RAM. It's managed via paging, where the OS maps virtual addresses to physical addresses and swaps pages to/from disk as needed. This allows running programs larger than physical RAM and provides memory isolation/protection between processes.

## Question: Explain paging and segmentation.
Paging divides memory into fixed-size blocks (pages in virtual memory, frames in physical memory), avoiding external fragmentation but can cause internal fragmentation. Segmentation divides memory into variable-sized logical units (code, stack, heap) based on the program's structure, which maps more naturally to how programs are organized but can suffer external fragmentation.

## Question: What is the difference between a mutex and a semaphore?
A mutex (mutual exclusion) is a locking mechanism allowing only one thread to access a critical section at a time — it has ownership, meaning only the thread that locked it can unlock it. A semaphore is a signaling mechanism with a counter that can allow a fixed number of threads to access a resource concurrently — it doesn't have ownership, so any thread can signal/release it.

## Question: What are the different CPU scheduling algorithms?
First-Come-First-Served (FCFS) processes in arrival order, simple but can cause long wait times (convoy effect). Shortest Job First (SJF) picks the shortest burst time next, minimizing average wait time but risks starvation for long jobs. Round Robin gives each process a fixed time quantum cyclically, fair and good for time-sharing systems. Priority Scheduling runs the highest-priority process first, which can also cause starvation without aging mechanisms.

## Question: What is thrashing in the context of operating systems?
Thrashing occurs when a system spends more time swapping pages in and out of memory (paging) than executing actual processes, usually because too many processes are competing for too little physical RAM. It causes system performance to collapse. It's mitigated by limiting the degree of multiprogramming or increasing available memory.

## Question: Explain the difference between a system call and a library call.
A system call is a direct request to the OS kernel for a service requiring elevated privileges (e.g., file I/O, process creation, memory allocation) and involves a context switch from user mode to kernel mode. A library call is a regular function call to code within a user-space library, which may or may not internally invoke a system call.

## Question: What is a race condition and how do you prevent it?
A race condition occurs when multiple threads/processes access shared data concurrently and the final outcome depends on the unpredictable timing of their execution, leading to inconsistent results. It's prevented using synchronization mechanisms like mutexes, semaphores, or atomic operations to ensure only one thread modifies shared state at a time (critical section protection).
