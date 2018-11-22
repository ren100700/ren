class Stack:

    def __init__(self, max_size):
        self.max_size = max_size
        self.top = None

    def push(self, item):
        if self.size() != self.max_size:
            node = Node(item)
            node.next_node = self.top
            self.top = node

    def pop(self):
        if self.top is None:
            return None
        else:
            tmp = self.top.value
            self.top = self.top.next_node
            return tmp

    def index(self, item):
        top = self.top
        index = self.size() - 1
        while top:
            if top.value == item:
                return index
            index -= 1
            top = top.next_node
        return None

    def empty(self):
        self.top = None

    def full(self):
        for i in range(self.max_size):
            self.push(i)

    def size(self):
        top = self.top
        count = 0
        while top:
            count += 1
            top = top.next_node
        return count

    def get(self, index):
        top = self.top
        num = self.size()
        for i in range(num):
            if index == num-1-i:
                return top.value
            top = top.next_node


class Query:

    def __init__(self):
        self.right = None

    def push(self, item):
        right = self.right
        if right:
            while right.next_node:
                right = right.next_node
            right.next_node = Node(item)
        else:
            self.right = Node(item)

    def pop(self):
        if self.right is None:
            return None
        else:
            right = self.right
            self.right = right.next_node
            return right

    def size(self):
        count = 0
        right = self.right
        while right:
            count += 1
            right = right.next_node
        return count


class Node:

    def __init__(self, value):
        self.value = value
        self.next_node = None


#链表
class LinkedList:

    def __init__(self):
        self.head = None

    def append(self, value):
        if self.head:
            head = self.head
            while head.next_node:
                head = head.next_node
            head.next_node = Node(value)
        else:
            self.head = Node(value)

    def insert(self, value, index):
        head = self.head
        if index <= 0:
            self.head = Node(value)
            self.head.next_node = head
        elif index >= self.size():
            if head:
                while head.next_node:
                    head = head.next_node
                head.next_node = Node(value)
            else:
                self.append(value)
        else:
            next_node = head.next_node
            for i in range(index - 1):
                head = head.next_node
                next_node = next_node.next_node
            head.next_node = Node(value)
            head.next_node.next_node = next_node

    def delete(self, index):
        head = self.head
        if head:
            if index == 0:
                self.head = head.next_node
            if 0 < index < self.size() - 1:
                next_node = head.next_node
                for i in range(index - 1):
                    head = head.next_node
                    next_node = next_node.next_node
                head.next_node = next_node.next_node
            if index == self.size() - 1:
                while head.next_node.next_node:
                    head = head.next_node
                head.next_node = None

    def size(self):
        count = 0
        head = self.head
        while head:
            count += 1
            head = head.next_node
        return count

    def remove(self, value):
        head = self.head
        if head:
            if head.value == value:
                self.head = head.next_node
            else:
                while head.next_node:
                    if head.next_node.value == value:
                        head.next_node = head.next_node.next_node
                        break
                    head = head.next_node

    def index(self, value):
        head = self.head
        index = 0
        index_list = []
        while head:
            if head.value == value:
                index_list.append(index)
            index += 1
            head = head.next_node
        return index_list

    def __repr__(self):
        str_link = ''
        head = self.head
        if head:
            while True:
                str_link += str(head.value)
                if head.next_node:
                    head = head.next_node
                    str_link += '→'
                else:
                    break
            return str_link
        else:
            return 'There is nothing'


if __name__ == "__main__":
    pass