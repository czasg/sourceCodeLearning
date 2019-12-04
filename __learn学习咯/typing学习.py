# -*- coding: utf-8 -*-
import typing
from typing import List, Dict

# 类型别名
vector_list = List[str]
vector_dict = Dict[str, str]
def test1(default: None = None) -> None: ...
def test2(default: vector_list = None) -> None: ...
def test3(default: vector_dict = None) -> None: ...





if __name__ == '__main__':
    # test1(None)
    # test2(['123', '456'])
    test3({'123': '123'})
