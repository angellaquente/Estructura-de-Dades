class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    visitados = set() 
    actual = head
    while actual is not None: 
        if actual in visitados: 
            return True
        visitados.add(actual)
        actual = actual.next
    return False

