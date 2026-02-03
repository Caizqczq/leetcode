"""LeetCode Hot 100 题目数据 - 按官方顺序排列"""

HOT_100_PROBLEMS = [
    # ========== 哈希 ==========
    {"leetcode_id": 1, "title": "Two Sum", "title_cn": "两数之和", "difficulty": "Easy", "category": "哈希"},
    {"leetcode_id": 49, "title": "Group Anagrams", "title_cn": "字母异位词分组", "difficulty": "Medium", "category": "哈希"},
    {"leetcode_id": 128, "title": "Longest Consecutive Sequence", "title_cn": "最长连续序列", "difficulty": "Medium", "category": "哈希"},
    
    # ========== 双指针 ==========
    {"leetcode_id": 283, "title": "Move Zeroes", "title_cn": "移动零", "difficulty": "Easy", "category": "双指针"},
    {"leetcode_id": 11, "title": "Container With Most Water", "title_cn": "盛最多水的容器", "difficulty": "Medium", "category": "双指针"},
    {"leetcode_id": 15, "title": "3Sum", "title_cn": "三数之和", "difficulty": "Medium", "category": "双指针"},
    {"leetcode_id": 42, "title": "Trapping Rain Water", "title_cn": "接雨水", "difficulty": "Hard", "category": "双指针"},
    
    # ========== 滑动窗口 ==========
    {"leetcode_id": 3, "title": "Longest Substring Without Repeating Characters", "title_cn": "无重复字符的最长子串", "difficulty": "Medium", "category": "滑动窗口"},
    {"leetcode_id": 438, "title": "Find All Anagrams in a String", "title_cn": "找到字符串中所有字母异位词", "difficulty": "Medium", "category": "滑动窗口"},
    
    # ========== 子串 ==========
    {"leetcode_id": 560, "title": "Subarray Sum Equals K", "title_cn": "和为 K 的子数组", "difficulty": "Medium", "category": "子串"},
    {"leetcode_id": 239, "title": "Sliding Window Maximum", "title_cn": "滑动窗口最大值", "difficulty": "Hard", "category": "子串"},
    {"leetcode_id": 76, "title": "Minimum Window Substring", "title_cn": "最小覆盖子串", "difficulty": "Hard", "category": "子串"},
    
    # ========== 普通数组 ==========
    {"leetcode_id": 53, "title": "Maximum Subarray", "title_cn": "最大子数组和", "difficulty": "Medium", "category": "普通数组"},
    {"leetcode_id": 56, "title": "Merge Intervals", "title_cn": "合并区间", "difficulty": "Medium", "category": "普通数组"},
    {"leetcode_id": 189, "title": "Rotate Array", "title_cn": "轮转数组", "difficulty": "Medium", "category": "普通数组"},
    {"leetcode_id": 238, "title": "Product of Array Except Self", "title_cn": "除自身以外数组的乘积", "difficulty": "Medium", "category": "普通数组"},
    {"leetcode_id": 41, "title": "First Missing Positive", "title_cn": "缺失的第一个正数", "difficulty": "Hard", "category": "普通数组"},
    
    # ========== 矩阵 ==========
    {"leetcode_id": 73, "title": "Set Matrix Zeroes", "title_cn": "矩阵置零", "difficulty": "Medium", "category": "矩阵"},
    {"leetcode_id": 54, "title": "Spiral Matrix", "title_cn": "螺旋矩阵", "difficulty": "Medium", "category": "矩阵"},
    {"leetcode_id": 48, "title": "Rotate Image", "title_cn": "旋转图像", "difficulty": "Medium", "category": "矩阵"},
    {"leetcode_id": 240, "title": "Search a 2D Matrix II", "title_cn": "搜索二维矩阵 II", "difficulty": "Medium", "category": "矩阵"},
    
    # ========== 链表 ==========
    {"leetcode_id": 160, "title": "Intersection of Two Linked Lists", "title_cn": "相交链表", "difficulty": "Easy", "category": "链表"},
    {"leetcode_id": 206, "title": "Reverse Linked List", "title_cn": "反转链表", "difficulty": "Easy", "category": "链表"},
    {"leetcode_id": 234, "title": "Palindrome Linked List", "title_cn": "回文链表", "difficulty": "Easy", "category": "链表"},
    {"leetcode_id": 141, "title": "Linked List Cycle", "title_cn": "环形链表", "difficulty": "Easy", "category": "链表"},
    {"leetcode_id": 142, "title": "Linked List Cycle II", "title_cn": "环形链表 II", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 21, "title": "Merge Two Sorted Lists", "title_cn": "合并两个有序链表", "difficulty": "Easy", "category": "链表"},
    {"leetcode_id": 2, "title": "Add Two Numbers", "title_cn": "两数相加", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 19, "title": "Remove Nth Node From End of List", "title_cn": "删除链表的倒数第 N 个结点", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 24, "title": "Swap Nodes in Pairs", "title_cn": "两两交换链表中的节点", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 25, "title": "Reverse Nodes in k-Group", "title_cn": "K 个一组翻转链表", "difficulty": "Hard", "category": "链表"},
    {"leetcode_id": 138, "title": "Copy List with Random Pointer", "title_cn": "随机链表的复制", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 148, "title": "Sort List", "title_cn": "排序链表", "difficulty": "Medium", "category": "链表"},
    {"leetcode_id": 23, "title": "Merge k Sorted Lists", "title_cn": "合并 K 个升序链表", "difficulty": "Hard", "category": "链表"},
    {"leetcode_id": 146, "title": "LRU Cache", "title_cn": "LRU 缓存", "difficulty": "Medium", "category": "链表"},
    
    # ========== 二叉树 ==========
    {"leetcode_id": 94, "title": "Binary Tree Inorder Traversal", "title_cn": "二叉树的中序遍历", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 104, "title": "Maximum Depth of Binary Tree", "title_cn": "二叉树的最大深度", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 226, "title": "Invert Binary Tree", "title_cn": "翻转二叉树", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 101, "title": "Symmetric Tree", "title_cn": "对称二叉树", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 543, "title": "Diameter of Binary Tree", "title_cn": "二叉树的直径", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 102, "title": "Binary Tree Level Order Traversal", "title_cn": "二叉树的层序遍历", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 108, "title": "Convert Sorted Array to Binary Search Tree", "title_cn": "将有序数组转换为二叉搜索树", "difficulty": "Easy", "category": "二叉树"},
    {"leetcode_id": 98, "title": "Validate Binary Search Tree", "title_cn": "验证二叉搜索树", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 230, "title": "Kth Smallest Element in a BST", "title_cn": "二叉搜索树中第K小的元素", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 199, "title": "Binary Tree Right Side View", "title_cn": "二叉树的右视图", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 114, "title": "Flatten Binary Tree to Linked List", "title_cn": "二叉树展开为链表", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 105, "title": "Construct Binary Tree from Preorder and Inorder Traversal", "title_cn": "从前序与中序遍历序列构造二叉树", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 437, "title": "Path Sum III", "title_cn": "路径总和 III", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 236, "title": "Lowest Common Ancestor of a Binary Tree", "title_cn": "二叉树的最近公共祖先", "difficulty": "Medium", "category": "二叉树"},
    {"leetcode_id": 124, "title": "Binary Tree Maximum Path Sum", "title_cn": "二叉树中的最大路径和", "difficulty": "Hard", "category": "二叉树"},
    
    # ========== 图论 ==========
    {"leetcode_id": 200, "title": "Number of Islands", "title_cn": "岛屿数量", "difficulty": "Medium", "category": "图论"},
    {"leetcode_id": 994, "title": "Rotting Oranges", "title_cn": "腐烂的橘子", "difficulty": "Medium", "category": "图论"},
    {"leetcode_id": 207, "title": "Course Schedule", "title_cn": "课程表", "difficulty": "Medium", "category": "图论"},
    {"leetcode_id": 208, "title": "Implement Trie (Prefix Tree)", "title_cn": "实现 Trie (前缀树)", "difficulty": "Medium", "category": "图论"},
    
    # ========== 回溯 ==========
    {"leetcode_id": 46, "title": "Permutations", "title_cn": "全排列", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 78, "title": "Subsets", "title_cn": "子集", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 17, "title": "Letter Combinations of a Phone Number", "title_cn": "电话号码的字母组合", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 39, "title": "Combination Sum", "title_cn": "组合总和", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 22, "title": "Generate Parentheses", "title_cn": "括号生成", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 79, "title": "Word Search", "title_cn": "单词搜索", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 131, "title": "Palindrome Partitioning", "title_cn": "分割回文串", "difficulty": "Medium", "category": "回溯"},
    {"leetcode_id": 51, "title": "N-Queens", "title_cn": "N 皇后", "difficulty": "Hard", "category": "回溯"},
    
    # ========== 二分查找 ==========
    {"leetcode_id": 35, "title": "Search Insert Position", "title_cn": "搜索插入位置", "difficulty": "Easy", "category": "二分查找"},
    {"leetcode_id": 74, "title": "Search a 2D Matrix", "title_cn": "搜索二维矩阵", "difficulty": "Medium", "category": "二分查找"},
    {"leetcode_id": 34, "title": "Find First and Last Position of Element in Sorted Array", "title_cn": "在排序数组中查找元素的第一个和最后一个位置", "difficulty": "Medium", "category": "二分查找"},
    {"leetcode_id": 33, "title": "Search in Rotated Sorted Array", "title_cn": "搜索旋转排序数组", "difficulty": "Medium", "category": "二分查找"},
    {"leetcode_id": 153, "title": "Find Minimum in Rotated Sorted Array", "title_cn": "寻找旋转排序数组中的最小值", "difficulty": "Medium", "category": "二分查找"},
    {"leetcode_id": 4, "title": "Median of Two Sorted Arrays", "title_cn": "寻找两个正序数组的中位数", "difficulty": "Hard", "category": "二分查找"},
    
    # ========== 栈 ==========
    {"leetcode_id": 20, "title": "Valid Parentheses", "title_cn": "有效的括号", "difficulty": "Easy", "category": "栈"},
    {"leetcode_id": 155, "title": "Min Stack", "title_cn": "最小栈", "difficulty": "Medium", "category": "栈"},
    {"leetcode_id": 394, "title": "Decode String", "title_cn": "字符串解码", "difficulty": "Medium", "category": "栈"},
    {"leetcode_id": 739, "title": "Daily Temperatures", "title_cn": "每日温度", "difficulty": "Medium", "category": "栈"},
    {"leetcode_id": 84, "title": "Largest Rectangle in Histogram", "title_cn": "柱状图中最大的矩形", "difficulty": "Hard", "category": "栈"},
    
    # ========== 堆 ==========
    {"leetcode_id": 215, "title": "Kth Largest Element in an Array", "title_cn": "数组中的第K个最大元素", "difficulty": "Medium", "category": "堆"},
    {"leetcode_id": 347, "title": "Top K Frequent Elements", "title_cn": "前 K 个高频元素", "difficulty": "Medium", "category": "堆"},
    {"leetcode_id": 295, "title": "Find Median from Data Stream", "title_cn": "数据流的中位数", "difficulty": "Hard", "category": "堆"},
    
    # ========== 贪心算法 ==========
    {"leetcode_id": 121, "title": "Best Time to Buy and Sell Stock", "title_cn": "买卖股票的最佳时机", "difficulty": "Easy", "category": "贪心算法"},
    {"leetcode_id": 55, "title": "Jump Game", "title_cn": "跳跃游戏", "difficulty": "Medium", "category": "贪心算法"},
    {"leetcode_id": 45, "title": "Jump Game II", "title_cn": "跳跃游戏 II", "difficulty": "Medium", "category": "贪心算法"},
    {"leetcode_id": 763, "title": "Partition Labels", "title_cn": "划分字母区间", "difficulty": "Medium", "category": "贪心算法"},
    
    # ========== 动态规划 ==========
    {"leetcode_id": 70, "title": "Climbing Stairs", "title_cn": "爬楼梯", "difficulty": "Easy", "category": "动态规划"},
    {"leetcode_id": 118, "title": "Pascal's Triangle", "title_cn": "杨辉三角", "difficulty": "Easy", "category": "动态规划"},
    {"leetcode_id": 198, "title": "House Robber", "title_cn": "打家劫舍", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 279, "title": "Perfect Squares", "title_cn": "完全平方数", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 322, "title": "Coin Change", "title_cn": "零钱兑换", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 139, "title": "Word Break", "title_cn": "单词拆分", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 300, "title": "Longest Increasing Subsequence", "title_cn": "最长递增子序列", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 152, "title": "Maximum Product Subarray", "title_cn": "乘积最大子数组", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 416, "title": "Partition Equal Subset Sum", "title_cn": "分割等和子集", "difficulty": "Medium", "category": "动态规划"},
    {"leetcode_id": 32, "title": "Longest Valid Parentheses", "title_cn": "最长有效括号", "difficulty": "Hard", "category": "动态规划"},
    
    # ========== 多维动态规划 ==========
    {"leetcode_id": 62, "title": "Unique Paths", "title_cn": "不同路径", "difficulty": "Medium", "category": "多维动态规划"},
    {"leetcode_id": 64, "title": "Minimum Path Sum", "title_cn": "最小路径和", "difficulty": "Medium", "category": "多维动态规划"},
    {"leetcode_id": 5, "title": "Longest Palindromic Substring", "title_cn": "最长回文子串", "difficulty": "Medium", "category": "多维动态规划"},
    {"leetcode_id": 1143, "title": "Longest Common Subsequence", "title_cn": "最长公共子序列", "difficulty": "Medium", "category": "多维动态规划"},
    {"leetcode_id": 72, "title": "Edit Distance", "title_cn": "编辑距离", "difficulty": "Medium", "category": "多维动态规划"},
    
    # ========== 技巧 ==========
    {"leetcode_id": 136, "title": "Single Number", "title_cn": "只出现一次的数字", "difficulty": "Easy", "category": "技巧"},
    {"leetcode_id": 169, "title": "Majority Element", "title_cn": "多数元素", "difficulty": "Easy", "category": "技巧"},
    {"leetcode_id": 75, "title": "Sort Colors", "title_cn": "颜色分类", "difficulty": "Medium", "category": "技巧"},
    {"leetcode_id": 31, "title": "Next Permutation", "title_cn": "下一个排列", "difficulty": "Medium", "category": "技巧"},
    {"leetcode_id": 287, "title": "Find the Duplicate Number", "title_cn": "寻找重复数", "difficulty": "Medium", "category": "技巧"},
]

# 预置标签
DEFAULT_TAGS = [
    {"name": "数组", "color": "#409EFF"},
    {"name": "链表", "color": "#67C23A"},
    {"name": "哈希表", "color": "#E6A23C"},
    {"name": "字符串", "color": "#F56C6C"},
    {"name": "双指针", "color": "#909399"},
    {"name": "滑动窗口", "color": "#9B59B6"},
    {"name": "栈", "color": "#3498DB"},
    {"name": "队列", "color": "#1ABC9C"},
    {"name": "堆", "color": "#E74C3C"},
    {"name": "二叉树", "color": "#2ECC71"},
    {"name": "二分查找", "color": "#F39C12"},
    {"name": "回溯", "color": "#8E44AD"},
    {"name": "贪心算法", "color": "#16A085"},
    {"name": "动态规划", "color": "#C0392B"},
    {"name": "图论", "color": "#2980B9"},
    {"name": "DFS", "color": "#27AE60"},
    {"name": "BFS", "color": "#D35400"},
    {"name": "位运算", "color": "#7F8C8D"},
    {"name": "数学", "color": "#BDC3C7"},
    {"name": "排序", "color": "#34495E"},
]


def get_leetcode_url(leetcode_id: int, title: str) -> str:
    """生成 LeetCode 链接"""
    slug = title.lower().replace(" ", "-")
    return f"https://leetcode.cn/problems/{slug}/"
