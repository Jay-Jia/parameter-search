'''
Descripttion: python实现的超参搜索算法，支持随机搜索、爬山法搜索、模拟退火算法以及遗传算法
version: v1.0
Author: xibeijia
Date: 2020-11-19 12:10:43
LastEditors: xibeijia
LastEditTime: 2020-12-28 11:11:31
'''

import random
import math
import mmcv

class SearchParam:
    '''
    param {dict} param_info,自定义的参数搜索域
    param {callable} cost_func,自定义的代价函数
    param {str} mode,选择支持的超参搜索算法，可选random, hillclimb, annealing和genetic
    param {bool} reverse,表示代价函数的返回值按照升序还是降序排列
    param {str} num_type,参数搜索为整型还是浮点型，可选值为int和float
    '''
    def __init__(self, param_info: dict, cost_func: callable, mode: str, reverse: bool, num_type: str):
        self.mode = mode
        print('\033[1;37;40m\t=====> choose {} algorithm\033[0m'.format(self.mode))
        self.param_info = param_info
        self.method = []
        self.cost = cost_func
        self.reverse = reverse
        self.num_type = num_type
        # 随机初始化值
        self.all_vec = list(self.param_info.keys())
        print('total key: {}'.format(self.all_vec))
    
    '''
    name: random
    msg: 随机搜索算法
    param {int} maxiter 最大循环次数
    return {list} 
    '''
    def random(self, maxiter: int) -> list:
        best_cost = float("inf")
        for i in range(maxiter):
            if self.num_type == 'float':
                vec = [round(random.uniform(self.param_info[i]['min'], self.param_info[i]['max']), 2) for i in self.all_vec]
            elif self.num_type == 'int':
                vec = [random.randint(self.param_info[i]['min'], self.param_info[i]['max']) for i in self.all_vec] 
            now_cost, overkill, escape = self.cost(vec)
            if now_cost < best_cost:
                print('======> update the lowest cost and vec!!!')
                best_cost = now_cost
                self.vec = vec
            print('current overkill is: {:.4f}, escape is: {:.4f}'.format(overkill, escape))
            print('current vec is {}'.format(vec))
            print('current iter {}, cost is: {:.4f}, and the lowest cost is {:.4f}'.format(i, now_cost, best_cost))
            print()
        print('the lowest cost is {:.4f}, and best params are {}'.format(best_cost, self.vec))
        return self.vec

    def hillclimb(self, step: float) -> list:
        # 随机产生一个序列作为初始种子
        if self.num_type == 'float':
            vec = [round(random.uniform(self.param_info[i]['min'], self.param_info[i]['max']), 2) for i in self.all_vec]
        elif self.num_type == 'int':
            vec = [random.randint(self.param_info[i]['min'], self.param_info[i]['max']) for i in self.all_vec]
        best_cost = float("inf")
        while 1:
            neighbor = []
            # 循环改变解的每一个值产生一个临近解的列表
            for i in range(len(self.all_vec)):
                # 下列判断是为了将某一位加减step后不超出范围
                if vec[i] > self.param_info[self.all_vec[i]]['min']:
                    newneighbor = vec[0:i] + [vec[i] - step] + vec[i + 1:]
                    neighbor.append(newneighbor)
                if vec[i] < self.param_info[self.all_vec[i]]['max']:
                    newneighbor = vec[0:i] + [vec[i] + step] + vec[i + 1:]
                    neighbor.append(newneighbor)
 
            # 对所有的临近解计算代价，排序，得到代价最小的解
            neighbor_cost = sorted(
                [(s, self.cost(s)) for s in neighbor], key=lambda x: x[1][0])
 
            # 如果新的最小代价 > 原种子代价，则跳出循环
            cost, overkill, escape = self.cost(vec)
            if neighbor_cost[0][1][0] > cost:
                break
 
            # 新的代价更小的临近解作为新的种子
            vec = neighbor_cost[0][0]
            best_cost = neighbor_cost[0][1][0]
            print("current vec: {}, and current cost: {}".format(vec, neighbor_cost[0][1][0]))
            print('current overkill is {}, and escape is {}'.format(overkill, escape))
        # 输出
        print('best params are {}'.format(vec))
        print("爬山法得到的解的最小代价是 {}".format(best_cost))
        return vec

    '''
    name: annealingoptimize
    msg: 模拟退火算法
    param {*} self
    param {float} T, 温度，温度越高，搜索的时间越长，解更优。
    param {float} cool, 温度冷却系数, 温度越来越低，算法越来越不能接受差的解
    param {float} step, 参数调整步长
    return {list}
    '''
    def annealingoptimize(self, T: float, cool: float, step: float)-> list:
        if self.num_type == 'float':
            self.vec = [round(random.uniform(self.param_info[i]['min'], self.param_info[i]['max']), 2) for i in self.all_vec]
        elif self.num_type == 'int':
            self.vec = [random.randint(self.param_info[i]['min'], self.param_info[i]['max']) for i in self.all_vec]
        print('init value: {}'.format(self.vec))
        # 循环
        while T > 0.1:
            # 选择一个索引值
            i = random.randint(0, len(self.vec) - 1)
            # 选择一个改变索引值的方向
            # 控制步长为step
            c = random.choice([step, -step])
            # c = random.uniform(-step, step)
            # c = random.choice([-1,1]) * random.randint(1,10)/100
            # 构造新的解
            vec_clone = self.vec[:]
            vec_clone[i] += c
            # 判断越界情况
            if vec_clone[i] < self.param_info[self.all_vec[i]]['min']:
                vec_clone[i] = self.param_info[self.all_vec[i]]['min']
            if vec_clone[i] > self.param_info[self.all_vec[i]]['max']:
                vec_clone[i] = self.param_info[self.all_vec[i]]['max']
 
            # 计算当前成本和新的成本
            cost1, overkill, escape = self.cost(self.vec)
            cost2, overkill2, escape2 = self.cost(vec_clone)

            if self.reverse:
                flag = cost2 > cost1
            else:
                flag = cost1 > cost2
 
            # 判断新的解是否优于原始解 或者 算法将以一定概率接受较差的解
            if flag or random.random() < math.exp(-(cost2 - cost1) / T):
                print('cost1is : {:.4f}'.format(cost1))
                print('cost2 is : {:.4f}'.format(cost2))
                if flag:
                    print('accept by cost!')
                else:
                    print('accept by random!')
                self.vec = vec_clone
 
            T = T * cool  # 温度冷却
            print('param: {}, cost: {}, overkill: {:.4f}, escape: {:.4f}'.format(vec_clone[:], cost2, overkill2, escape2))
        # self.printsolution(vec)
        print('best params: {}'.format(self.vec))
        best_cost1, best_overkill, best_escape = self.cost(self.vec)
        print("lowest cost{}".format(best_cost1))
        print('overkill: {}, escape: {}'.format(best_overkill, best_escape))
        return self.vec

    
    '''
    name: geneticoptimize
    msg: 遗传算法
    param {int} popsize 种群大小
    param {float} step 参数步长
    param {float} mutprob 变异概率0-1
    param {float} elite 最优比例0-1
    param {int} maxiter 最大迭代系数
    return {list}
    '''
    def geneticoptimize(self, popsize: int, step: float, mutprob: float, crossprob: float, elite: float, maxiter: int) -> list:

        # 构造初始种群
        pop = []
        for i in range(popsize):
            vec = [random.randrange(self.param_info[i]['min'] * 100, self.param_info[i]['max']* 100, 5)/100 \
                for i in self.all_vec]
            pop.append(vec)
        # print(pop)
        # 变异操作的函数
        def mutate(vec):
            i = random.randint(0, len(self.all_vec) - 1)
            step = random.uniform(-0.5, 0.5)
            vec[i] += step
            # 判断越界情况
            if vec[i] < self.param_info[self.all_vec[i]]['min']:
                vec[i] = self.param_info[self.all_vec[i]]['min']
            if vec[i] > self.param_info[self.all_vec[i]]['max']:
                vec[i] = self.param_info[self.all_vec[i]]['max']
            return vec
    
        # 交叉操作的函数（单点交叉）
        def crossover(r1, r2):
            i = random.randint(0, len(self.all_vec) - 1)
            return r1[0:i] + r2[i:]

        # 针对代价函数可能返回多个值进行的处理
        def util(i):
            return i[0]
        
        # 多进程加速
        cpu_count = multiprocessing.cpu_count()
        print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    
        # 每一代中有多少胜出者
        topelite = int(elite * popsize)
        print('each epoch has {} successors'.format(topelite))
        
        # 主循环
        for i in range(maxiter):
            print('iter: {} begin...'.format(i))
            #默认多进程数目为cpu核心数目的80%
            score = mmcv.utils.track_parallel_progress(self.cost, pop, cpu_count * 0.8)
            scores = [(cost, v) for (cost, v) in zip(score, pop)]
            
            print('iter {}, scores is calculated...'.format(i))
            scores.sort(key=util)
            print('参数: {}: 代价: {}'.format(scores[0][1], scores[0][0]))
            # print(scores)
            # 解按照代价由小到大的排序
            ranked = [v for (s, v) in scores]
            # 优质解遗传到下一代
            pop = ranked[0: topelite]
            print('iter {}, start to mutprob or cross...'.format(i))
            # 如果当前种群数量小于既定数量，则添加变异和交叉遗传
            while len(pop) < popsize:
                # 随机数小于 mutprob 则变异，否则交叉
                if random.random() < mutprob:  # mutprob控制交叉和变异的比例
                    # 选择一个个体
                    c = random.randint(0, topelite)
                    # 变异
                    pop.append(mutate(ranked[c]))
                if random.random() < crossprob:
                    # 随机选择两个个体进行交叉
                    c1 = random.randint(0, topelite)
                    c2 = random.randint(0, topelite)
                    pop.append(crossover(ranked[c1], ranked[c2]))
            # 输出当前种群中代价最小的解
            
        print(scores[0][1])
        print("遗传算法求得的最小代价：{}".format(scores[0][0]))
        return scores[0][1]


def cost_func(vec):
    return sum(vec) / len(vec)
    
if __name__ == "__main__":
    
    init = SearchParam(allinfo, cost_func, 'genetic', False, 'float')
    # init.annealingoptimize(1000.0, 0.98, 0.01)
    init.geneticoptimize(100, 0.1, 0.2, 0.5, 0.1, 100)
    # init.random(100)
    # init.hillclimb(0.1)
