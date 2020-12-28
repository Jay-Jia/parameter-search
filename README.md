<!--
 * @Descripttion: 
 * @version: 
 * @Author: xibeijia
 * @Date: 2020-12-28 10:55:51
 * @LastEditors: xibeijia
 * @LastEditTime: 2020-12-28 11:34:55
-->
# 参数搜索算法 Parameter search algorithm

# 1. 支持的搜索算法 Supported search algorithms
- [x] `随机搜索 random search`
- [x] `爬山搜索算法 hillclimb`
- [x] `模拟退火算法 annealing optimize`
- [x] `遗传算法 genetic optimize`

# 2. Requirements
- mmcv

# 3. Usage
- 只需要定义一系列需要搜索的参数，且定义参数的搜索范围，选择化需要使用的搜索算法，定义好代价函数，喝杯茶等待结果吧～
- Just define a series of parameters that need to be searched, define the search range of the parameters, select the search algorithm to be used, define the cost function, and wait for the result with a cup of tea~

# 4. Demo
- 具体使用案例已经定义在``hyperParamSearch.py``中
```bash
python3 hyperParamSearch.py
```
