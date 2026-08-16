# DSA Interview Patterns

## Question: What is the Two Pointer technique and when should I use it?
Two Pointer is used on sorted arrays or linked lists when you need to find pairs, triplets, or compare elements from both ends. You maintain two indices (often start and end) and move them based on a condition, avoiding nested loops.
Common use cases: Two Sum (sorted array), 3Sum, Container With Most Water, Trapping Rain Water, removing duplicates from sorted array.
Time complexity is typically O(n) instead of O(n^2) for the brute force nested-loop version.

## Question: What is the Sliding Window pattern?
Sliding Window is used for problems involving contiguous subarrays or substrings, where you expand a window by moving the right pointer and shrink it by moving the left pointer based on a condition, avoiding recomputation from scratch.
Common use cases: Longest Substring Without Repeating Characters, Maximum Sum Subarray of size K, Minimum Window Substring, Longest Substring with K Distinct Characters.
Fixed-size windows track a constant window length; variable-size windows grow/shrink dynamically based on a constraint.

## Question: Explain Kadane's Algorithm.
Kadane's Algorithm finds the maximum sum contiguous subarray in O(n) time. You maintain a running sum (currentMax) and a global maximum (globalMax). At each element, decide whether to extend the previous subarray or start fresh: currentMax = max(arr[i], currentMax + arr[i]). Update globalMax if currentMax exceeds it.
This pattern generalizes to problems like Maximum Product Subarray (track both max and min due to negative number flips) and Maximum Circular Subarray Sum.

## Question: What is the Fast and Slow Pointer (Floyd's Cycle Detection) technique?
Two pointers move through a linked list or array at different speeds (slow moves 1 step, fast moves 2 steps). If there's a cycle, they will eventually meet. If fast reaches null, there's no cycle.
Used for: detecting cycles in linked lists, finding the middle of a linked list, finding the start of a cycle (Floyd's Tortoise and Hare), detecting duplicate numbers in an array using index-as-pointer.

## Question: What is the Merge Intervals pattern?
Used when dealing with overlapping intervals. Sort intervals by start time, then iterate through and merge any interval whose start is less than or equal to the previous interval's end.
Common use cases: Merge Intervals, Insert Interval, Meeting Rooms (can a person attend all meetings), Meeting Rooms II (minimum conference rooms needed).

## Question: Explain BFS and DFS traversal templates for trees and graphs.
BFS (Breadth-First Search) explores level by level using a queue. Useful for shortest path in unweighted graphs, level-order tree traversal.
```python
from collections import deque
def bfs(root):
    if not root: return []
    queue, result = deque([root]), []
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    return result
```
DFS (Depth-First Search) explores as far as possible before backtracking, using recursion or a stack. Useful for path-finding, detecting cycles, topological sort.
```python
def dfs(node, visited):
    if not node or node in visited: return
    visited.add(node)
    for neighbor in graph[node]:
        dfs(neighbor, visited)
```

## Question: What is the Dutch National Flag algorithm and where is it used?
It's a one-pass, three-way partitioning algorithm (used in Sort Colors / Sort 0s 1s 2s) that partitions an array into three sections using three pointers: low, mid, high. Elements equal to the pivot stay in the middle, smaller elements go left, larger go right. It achieves O(n) time and O(1) space without extra sorting.

## Question: What is the Leaders in an Array pattern?
An element is a "leader" if it's greater than all elements to its right. Traverse the array from right to left, maintaining the maximum seen so far. If the current element is greater than max, it's a leader. This runs in O(n) time with a single reverse pass instead of the O(n^2) brute force check.

## Question: How do you detect if a number is a power of 2 using bit manipulation?
A power of 2 has exactly one bit set in its binary representation. The trick: `n > 0 and (n & (n - 1)) == 0`. Subtracting 1 flips the rightmost set bit and all bits after it; ANDing with the original clears that bit, resulting in zero only if there was exactly one set bit.

## Question: What is the difference between a Greedy approach and Dynamic Programming?
Greedy makes the locally optimal choice at each step, hoping it leads to a global optimum — it never reconsiders past decisions, so it's fast but only works when the problem has the "greedy choice property." DP breaks a problem into overlapping subproblems, solves each once, and stores results (memoization or tabulation) to avoid recomputation — used when a problem has optimal substructure but greedy choices don't guarantee a global optimum (e.g., 0/1 Knapsack, Longest Common Subsequence).

## Question: How do you approach a Binary Search on a Rotated Sorted Array?
Standard binary search assumes a fully sorted array. In a rotated array, at each midpoint, determine which half (left or right of mid) is properly sorted by comparing arr[left] with arr[mid]. If the left half is sorted, check if the target lies within that range; otherwise search the right half, and vice versa. This preserves O(log n) time.

## Question: What is Trapping Rain Water and how do you solve it efficiently?
Given an elevation map, calculate how much water can be trapped after rain. The water trapped at each index equals min(maxLeft, maxRight) - height[i]. Brute force computes maxLeft/maxRight for every index in O(n^2). The optimal two-pointer solution uses leftMax and rightMax pointers moving inward, achieving O(n) time and O(1) space by always processing the side with the smaller max first.
