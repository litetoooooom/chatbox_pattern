# -*- coding: utf-8 -*-
from collections import defaultdict
from collections.abc import Set

class TrieNode(Set):
    def __init__(self, iterable=()):
        self._children = defaultdict(TrieNode)
        self._end = False
        self._len = 0
        for element in iterable:
            self.add(element)

    def add(self, element):
        node = self
        for s in element:
            node = node._children[s]
        if not node._end:
            node._end = True
            node._len += 1
            node = self
            for s in element:
                node._len += 1
                node = node._children[s]

    def __contains__(self, element):
        node = self
        for k in element:
            if k not in node._children:
                return False
            node = node._children[k]
        return node._end
    
    def search_1(self, term):
        print ("Start: ", ''.join(term))
        results = set()
        element = []
        def _search(m, node, i, current_skip_steps, max_skip_steps):
            element.append(m)
            print(current_skip_steps, max_skip_steps, ''.join(element), i, len(term))
            if current_skip_steps <= max_skip_steps and max_skip_steps != -1:
                #if node._end:
                #    results.add(''.join(element))
                for k, child in node._children.items():
                    _search(k, child, i, current_skip_steps+1, max_skip_steps)
                    if i+current_skip_steps <= len(term):
                        _search(k, child, i+current_skip_steps, -1, -1)
            elif max_skip_steps != -1:
                pass
            else:
                if i == len(term):
                    if node._end:
                        results.add(''.join(element))
                elif term[i] == '?':
                    for k,child in node._children.items():
                        _search(k, child, i+1, -1, -1)
                elif term[i] == '*':
                    _search('', node, i+1, -1, -1)
                    for k,child in node._children.items():
                        _search(k, child, i, -1, -1)
                elif term[i] == '[W:0-2]':
                    for k,child in node._children.items():
                        _search(k, child, i, 1, 2)
                        _search(k, child, i+1, -1, -1)
                elif term[i] in node._children:
                    _search(term[i], node._children[term[i]], i+1, -1, -1)
                    
            element.pop()
        _search('', self, 0, -1, -1)

        return results
    
    def search_2(self, term):
        def _add(indexes, i):
            while i < len(term) and term[i] == '*':
                indexes.add(i)
                i += 1
            indexes.add(i)
        
        indexes = set()
        _add(indexes, 0)
        if self._end and len(term) in indexes:
            yield ''
        
        indexes_stack = [indexes]
        element = ['']
        iter_stack = [iter(self._children.items())]
        while iter_stack:
            for k, node in iter_stack[-1]:
                new_indexes = set()
                for i in indexes_stack[-1]:
                    if i >= len(term):
                        continue
                    elif term[i] == '*':
                        _add(new_indexes, i)
                    elif term[i] == '?' or term[i] == k:
                        _add(new_indexes, i + 1)
                if new_indexes:
                    element.append(k)
                    if node._end and len(term) in new_indexes:
                        yield ''.join(element)
                    indexes_stack.append(new_indexes)
                    iter_stack.append(iter(node._children.items()))
                    break
            else:
                element.pop()
                indexes_stack.pop()
                iter_stack.pop()

    def __iter__(self):
        element = ['']
        stack = [iter([('', self)])]
        while stack:
            for k,node in stack[-1]:
                element.append(k)
                if node._end:
                    yield ''.join(element)
                stack.append(iter(node._children.items()))
                break
            else:
                element.pop()
                stack.pop()

    def __len__(self):
        return self._len


root = TrieNode()
root.add("aba*")
root.add("abb")
root.add("abc")
root.add("abd")
root.add("")
root.add("中华人民")


root.add("我鱼")
root.add("我爱鱼")
root.add("我爱吃鱼")
root.add("我爱吃大鱼")
root.add("我爱吃大小鱼")
root.add("我爱吃大小黄鱼")
root.add("我狗")
root.add("我爱狗")
root.add("我爱吃狗")
root.add("我爱吃大狗")
root.add("我爱吃大小狗")
root.add("我爱吃大小黄狗")
#print (root.search_1(['我','[W:0-2]','鱼']))
#print (root.search_1(['[W:0-2]','大','鱼']))
def print_all(node):
    ks = []
    for k,d in node._children.items():
        ks.append(k)
    print(' '.join(ks))
    for k,d in node._children.items():
        print_all (d)
print_all(root)

