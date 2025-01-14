class Node {
  constructor(val, child) {
    this.val = val;
    this.child = child;
  }
}
// Refactored the Node class:
// 1. Corrected the spelling of the constructor from 'ctructor' to 'constructor'.
// 2. Modified the constructor to accept 'val' and 'child' as parameters for initialization.
// 3. Initialized 'this.val' and 'this.child' with the provided 'val' and 'child' values, respectively.
// 4. Removed the redundant 'this.val = this.val' and the assignment 'this.child = v' where 'v' was undefined.