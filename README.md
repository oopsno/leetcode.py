# codewars.py

[![Travis](https://img.shields.io/travis/oopsno/leetcode.py.svg?style=flat-square)]()
[![Code Climate](https://img.shields.io/codeclimate/maintainability/oopsno/leetcode.py.svg?style=flat-square)]()
[![Coveralls github](https://img.shields.io/coveralls/oopsno/leetcode.py/master.svg?style=flat-square)]()

## 简介

这是一个用 [Python][Python] 刷 [CodeWars][LeetCode] 的仓库

> 反正刷了也找不到工作啊喵...

## 依赖

+ (必须) Python 3.6+
+ (可选) Coverage.py 4.0+

## 使用

要检查是不是写对了

```shell
python test/soltions.py
```

要检查覆盖率

```shell
coverage run test/solutions.py && coverage report
```

## 结构

### leetcode

目前 `leetcode` 模块仅实现了类似于 [Catch2][Catch2] 的 DSL 到标准库中的 [`unittest`][PyUT] 的转译器

### solutions

放答案的地方

### test
#### soltions

- 加载 `solutions` 中的所有题解的单元测试，并逐一运行
- 当且仅当全部测试通过时，解释器以返回值0结束

[LeetCode]: https://www.leetcode.com
[Python]: https://www.python.org
[Catch2]: https://github.com/catchorg/Catch2 
[CWTF]: https://github.com/Codewars/codewars.com/wiki/Codewars-Python-Test-Framework
[PyUT]: https://docs.python.org/3/library/unittest.html
