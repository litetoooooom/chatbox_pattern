# chatbox_pattern
trie 树实现自动问答匹配pattern，在给定query下，在所有数据中查询

目前提供的查询功能有：
1. 提供'?', 表示通配一个字符
2. 提供'*', 表示通配所有字符
3. 提供[W:0-3]: 表示通配0-3个匹配字，其中3是可修改，

```python    
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
    ```
结果输出：

{'我爱吃大狗', '我狗', '我爱吃狗', '我爱狗'}
{'我爱吃大鱼'}
{'我爱吃鱼', '我爱吃大鱼', '我爱吃大小鱼'}
{'我鱼', '鱼', '我爱鱼'}
{'我爱吃大狗', '我爱吃大小狗', '我爱吃狗'}
{'我狗', '我爱狗'}
