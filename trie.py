# -*- coding: utf-8 -*-
from collections import defaultdict
from collections.abc import Set
import re

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
        results = set()
        element = []
        
        def _search(m, node, i, current_skip_steps, min_skip_steps, max_skip_steps):
            element.append(m)
            #print(current_skip_steps, max_skip_steps, ''.join(element), i, len(term))
            if current_skip_steps < max_skip_steps and max_skip_steps != -1:
                for k, child in node._children.items():
                    _search(k, child, i, current_skip_steps+1, min_skip_steps, max_skip_steps)
                    if current_skip_steps >= min_skip_steps:
                        _search(k, child, i+1, -1, -1, -1)
            elif current_skip_steps == -1 and max_skip_steps == -1:
                if i == len(term):
                    if node._end:
                        results.add(''.join(element))
                elif term[i] == '?':
                    for k,child in node._children.items():
                        _search(k, child, i+1, -1, -1, -1)
                elif term[i] == '*':
                    _search('', node, i+1, -1, -1, -1)
                    for k,child in node._children.items():
                        _search(k, child, i, -1, -1, -1)
                elif len(re.findall('\[W:0-([1-9]*)\]', term[i])) > 0:
                    max_s = re.findall('\[W:0-([1-9]*)\]', term[i])[0]
                    _search('', node, i+1, -1, -1, -1)
                    for k,child in node._children.items():
                        _search(k, child, i, 1, 0, int(max_s))
                elif term[i] in node._children:
                    _search(term[i], node._children[term[i]], i+1, -1, -1, -1)
                elif node._end:
                    if element[-1] == term[i]:
                        results.add(''.join(element))
            element.pop()
        _search('', self, 0, -1, -1, -1)

        return results
    """    
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
    """

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

def print_tree(node, indent=0):
    if node:
        ind = '' + '\t' * indent
        for k,children in node._children.items():
            label = "'%s' : " % k
            print (ind + label + '{')
            print_tree(children, indent+1)
            print (ind + ' '*len(label) + '}')  

def test():
    root = TrieNode()
    root.add("aba*")
    root.add("abb")
    root.add("abc")
    root.add("abd")
    root.add("")
    root.add("中华人民")


    root.add("鱼")
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
    print (root.search_1(['我','[W:0-3]','狗']))
    print (root.search_1(['[W:0-3]','大','鱼']))
    print (root.search_1(['我','爱','吃','[W:0-2]', '鱼']))
    print (root.search_1(['[W:0-2]', '鱼']))
    print (root.search_1(['我','爱','吃','[W:0-2]', '狗']))
    print (root.search_1(['[W:0-2]', '狗']))
    
    #print_tree(root)

if __name__ == "__main__":
    test()
