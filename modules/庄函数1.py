import pandas as pd
import random  # 需要添加random导入
from tabulate import tabulate

class Pick3_庄模板:
    def __init__(self):
        self.投注结果 = []  # 存储每期投注结果
        self.预测数量列表 = []  # 存储每期预测的号码数量
        self.平均预测数量 = 0  # 存储每期预测的号码数量
        self.中次数结果统计 = {}  # 连续中奖次数统计
        self.不中次数结果统计 = {}  # 连续不中次数统计
        self.总次数 = 0


        self.最长连对 = 0
        self.最长连错 = 0
        self.中奖率 = 0.0  # 浮点数
        self.参与率 = 0.0  # 浮点数
        # 需要观察的数据
        # 新增连对和连错统计属性 数据格式：字典的键是连续次数（如 2 次、3 次等），值是对应连续次数出现的次数
        self.总次数 = 0

        self.中奖次数 = 0
        self.不中次数 = 0
        self.不买次数 = 0
        self.中奖率 = 0.0  # 浮点数
        self.实际购买次数 = 0  
        self.参与率 = 0.0 
        self.平均下注数 = 0  
        self.平均下注率 = 0.0 
        self.连对统计 = {}  # 连对次数统计  
        self.连错统计 = {}  # 连错次数统计

    def 动作(self, 结果, 预测集合):
        self.投注结果.append(结果)
        self.预测数量列表.append(len(预测集合) if 预测集合 else 0)
        if 结果 != '-':
            self.实际购买次数 += 1

        # 更新统计信息
        self.总次数 = len(self.投注结果)
        self.中奖次数 = self.投注结果.count('W')
        self.不中次数 = self.投注结果.count('L')
        self.不买次数 = self.投注结果.count('-')
        self.平均下注数 = self.计算预测平均数()
        
        # 计算中奖率和参与率（以浮点数显示）
        self.参与率 = (self.实际购买次数 / self.总次数) if self.总次数 > 0 else 0.0
        self.中奖率 = (self.中奖次数 / self.实际购买次数) if self.实际购买次数 > 0 else 0.0


        # 计算下注率（以浮点数显示）
        self.平均下注率 = self.平均下注数 / 1000 if self.总次数 > 0 else 0.0

    def 执行预测(self, 历史数据, 策略函数):
        if not 历史数据:
            return
            
        for i in range(len(历史数据)):
            当前号码 = 历史数据[i]
            前期数据 = [] if i == 0 else 历史数据[:i]
            
            预测结果 = 策略函数(前期数据)
            if not 预测结果:
                self.动作('-', set())
            elif 当前号码 in 预测结果:
                self.动作('W', 预测结果)
            else:
                self.动作('L', 预测结果)
                
        self.统计()

    def 统计(self):
        实际购买结果 = [结果 for 结果 in self.投注结果 if 结果 != '-']
        
        if not 实际购买结果:
            return
            
        # 连对和连错统计
        当前符号 = 实际购买结果[0]
        连续次数 = 1
        
        # 清空连对和连错统计
        self.连对统计 = {}
        self.连错统计 = {}
        
        for i in range(1, len(实际购买结果)):
            if 实际购买结果[i] == 当前符号:  # 如果与前一个相同
                连续次数 += 1
            else:  # 如果与前一个不同
                if 连续次数 >= 2:  # 只统计2次及以上的
                    if 当前符号 == 'W':
                        self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
                        self.连对统计[连续次数] = self.连对统计.get(连续次数, 0) + 1
                    elif 当前符号 == 'L':
                        self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
                        self.连错统计[连续次数] = self.连错统计.get(连续次数, 0) + 1
                当前符号 = 实际购买结果[i]
                连续次数 = 1
        
        # 处理最后一组连续结果
        if 连续次数 >= 2:
            if 当前符号 == 'W':
                self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
                self.连对统计[连续次数] = self.连对统计.get(连续次数, 0) + 1
            elif 当前符号 == 'L':
                self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
                self.连错统计[连续次数] = self.连错统计.get(连续次数, 0) + 1
        
        # 查找最长连续次数
        self.最长连对 = max(self.中次数结果统计.keys(), default=0)
        self.最长连错 = max(self.不中次数结果统计.keys(), default=0)

    def 计算预测平均数(self):
        # 只统计预测集合非空且实际进行投注的情况
        有效预测数量 = [
            self.预测数量列表[i] 
            for i in range(len(self.投注结果)) 
            if self.投注结果[i] != '-' and self.预测数量列表[i] > 0
        ]
        
        if not 有效预测数量:
            return 0
        return int(sum(有效预测数量) / len(有效预测数量))
    
    def 显示结果(self):
        # 打印详细统计
        print(f"详细统计:")
        print(f"总期数: {self.总次数}")
        print(f"实际购买次数: {self.实际购买次数}({self.参与率})") 
        print(f"平均下注数: {self.平均下注数}({self.平均下注率})")
        print(f"中奖次数: {self.中奖次数} ({self.中奖率})")
        print(f"不中次数: {self.不中次数} ({(self.不中次数/self.实际购买次数 if self.实际购买次数 > 0 else 0)})")
        print(f"不买次数: {self.不买次数} ({(self.不买次数/self.总次数 if self.总次数 > 0 else 0)})")
        print(f"连错次数统计: {self.连错统计}")
        print(f"连对次数统计: {self.连对统计}")
        print(f"平均下注率: {self.平均下注率}")
        print(f"参与率: {self.参与率}")



        # 找出最大次数并创建统计表格
        最大次数 = max(
            max(self.中次数结果统计.keys(), default=0),
            max(self.不中次数结果统计.keys(), default=0)
        )
        
        # 创建数据字典
        data = {
            '连对': [self.连对统计.get(i, 0) for i in range(2, 最大次数 + 1)],
            '连错': [self.连错统计.get(i, 0) for i in range(2, 最大次数 + 1)]
        }
        
        # 创建DataFrame并打印带表格线的表格
        df = pd.DataFrame(data).T
        df.columns = [f'{i}次' for i in range(2, 最大次数 + 1)]
        print("\n统计表格:")
        pd.set_option('display.unicode.east_asian_width', True)  # 处理中文对齐
        pd.set_option('display.colheader_justify', 'center')    # 列标题居中
        pd.set_option('display.max_columns', None)              # 显示所有列
        pd.set_option('display.width', None)                    # 不限制宽度
        
        # 打印表格
        print(df.to_string(justify='center'))

    def 获取统计结果(self):
        """返回统计结果字典"""
        return {
            '投注记录': self.投注结果,
            '中奖次数': self.中奖次数,
            '不中次数': self.不中次数,
            '不买次数': self.不买次数,
            '总次数': self.总次数,
            '实际购买次数': self.实际购买次数,
            '平均下注数': round(self.平均下注数, 2),
            '中奖率': round(self.中奖率, 4),  # 调整为浮点数
            '参与率': round(self.参与率, 4),  # 调整为浮点数
            '最长连对': self.最长连对,
            '最长连错': self.最长连错,
            '中次数结果统计': self.中次数结果统计,
            '不中次数结果统计': self.不中次数结果统计,
            '连对统计': self.连对统计,  # 返回连对统计
            '连错统计': self.连错统计   # 返回连错统计
        }