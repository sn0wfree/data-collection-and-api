# -*- encoding:utf-8 -*-
class Node():
    '创建节点'

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList():
    '创建列表'

    def __init__(self):
        '初始化列表'
        self.head = None

        self.tail = None

    def append(self, data):
        '右添加节点'
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = self.head
        else:
            self.tail.next = node
            self.tail = node

    def is_empty(self):
        return self.head is None

    def view(self):
        '查看列表'

        node = self.head
        if self.is_empty:
            link_str = 'empty'

        else:
            link_str = ''
            while 1:
                if node.next is not None:
                    link_str += str(node.data) + '-->'
                else:
                    link_str += str(node.data)
                node = node.next
        print 'The Linklist is:' + link_str

    def length(self, rtrn=True, printitout=False):
        '列表长度'
        node = self.head
        if node is not None:
            count = 1
            while node.next is not None:
                count += 1
                node = node.next
        else:
            count = 0
        if printitout:
            print 'The length of linklist are %d' % count
        if rtrn:
            return count

    def delete_node(self, index):
        '删除节点'
        if index + 1 > self.length():
            raise IndexError('index out of bounds')
        num = 0
        node = self.head
        while True:
            if num == index - 1:
                break
            node = node.next
            num += 1
        tmp_node = node.next
        node.next = node.next.next
        return tmp_node.data

    def find_node(self, index):
        '查看具体节点'
        if index + 1 > self.length():
            raise IndexError('index out of bounds')
        num = 0
        node = self.head
        while True:
            if num == index:
                break
            node = node.next
            num += 1
        return node.data

if __name__ == '__main__':
    pass
