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
        self.中次数概率统计 = {}  # 连续中奖次数统计
        self.不中次数概率统计 = {}  # 连续不中次数统计
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
        self.概率期望 = 0.0

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
                # 删除 if 连续次数 >= 2 的判断，改为：
                if 当前符号 == 'W':
                    self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
                    self.连对统计[连续次数] = self.连对统计.get(连续次数, 0) + 1
                elif 当前符号 == 'L':
                    self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
                    self.连错统计[连续次数] = self.连错统计.get(连续次数, 0) + 1
                当前符号 = 实际购买结果[i]
                连续次数 = 1
        
        # 处理最后一组连续结果
        if 当前符号 == 'W':
            self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
            self.连对统计[连续次数] = self.连对统计.get(连续次数, 0) + 1
        elif 当前符号 == 'L':
            self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
            self.连错统计[连续次数] = self.连错统计.get(连续次数, 0) + 1
        
        # 查找最长连续次数
        self.最长连对 = max(self.中次数结果统计.keys(), default=0)
        self.最长连错 = max(self.不中次数结果统计.keys(), default=0)

        # 概率期望
        self.概率期望 = round(self.中奖率 - self.平均下注率, 3) # 结果四舍五入到小数点后两位。
        # 处理概率 ↓
        # 在统计方法末尾修改计算概率的代码
        总中奖次数 = sum(self.中次数结果统计.values())
        总不中次数 = sum(self.不中次数结果统计.values())
        
        # 计算中奖概率（转换为小数形式）
        self.中次数概率统计.clear()
        for 次数, 频次 in self.中次数结果统计.items():
            概率 = round(频次 / 总中奖次数, 3) if 总中奖次数 > 0 else 0  # 直接使用小数，保留3位
            self.中次数概率统计[次数] = 概率
        
        # 计算不中概率（转换为小数形式）
        self.不中次数概率统计.clear()
        for 次数, 频次 in self.不中次数结果统计.items():
            概率 = round(频次 / 总不中次数, 3) if 总不中次数 > 0 else 0  # 直接使用小数，保留3位
            self.不中次数概率统计[次数] = 概率


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
    
    def 生成对比表格(self):
        # 获取实际统计中的最大次数
        最大次数 = max(
            max(self.中次数结果统计.keys(), default=0),
            max(self.不中次数结果统计.keys(), default=0)
        )
        
        # 使用平均下注率作为单次中奖概率
        单次中奖概率 = self.平均下注率
        单次不中概率 = 1 - self.平均下注率  # 单次不中概率是平均下注率的补数
        
        # 计算理论概率
        中奖理论概率 = {}
        不中理论概率 = {}
        
        # 计算连对的理论概率
        中奖总和 = sum((单次中奖概率 ** n) * (1 - 单次中奖概率) for n in range(1, 最大次数 + 1))
        for n in range(1, 最大次数 + 1):
            中奖理论概率[n] = (单次中奖概率 ** n) * (1 - 单次中奖概率) / 中奖总和
        
        # 计算连错的理论概率
        不中总和 = sum((单次不中概率 ** n) * (1 - 单次不中概率) for n in range(1, 最大次数 + 1))
        for n in range(1, 最大次数 + 1):
            不中理论概率[n] = (单次不中概率 ** n) * (1 - 单次不中概率) / 不中总和
        
        # 创建对比数据
        data = {
            '连对实际概率': [self.中次数概率统计.get(i, 0) for i in range(1, 最大次数 + 1)],
            '连对理论概率': [中奖理论概率.get(i, 0) for i in range(1, 最大次数 + 1)],
            '连对差异': [self.中次数概率统计.get(i, 0) - 中奖理论概率.get(i, 0) for i in range(1, 最大次数 + 1)],
            '连错实际概率': [self.不中次数概率统计.get(i, 0) for i in range(1, 最大次数 + 1)],
            '连错理论概率': [不中理论概率.get(i, 0) for i in range(1, 最大次数 + 1)],
            '连错差异': [self.不中次数概率统计.get(i, 0) - 不中理论概率.get(i, 0) for i in range(1, 最大次数 + 1)]
        }
        
        # 创建DataFrame并设置显示格式
        df = pd.DataFrame(data).T
        df.columns = [f'{i}次' for i in range(1, 最大次数 + 1)]
        print(f"\n单次中奖概率: {单次中奖概率:.3f}")
        print(f"单次不中概率: {单次不中概率:.3f}")
        print("\n概率对比表格:")
        pd.set_option('display.unicode.east_asian_width', True)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.float_format', '{:.3f}'.format)  # 设置浮点数格式为三位小数
        
        # 打印表格
        print(df.to_string(justify='center'))

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
        # print(f"平均下注率: {self.平均下注率}")
        # print(f"参与率: {self.参与率}")
        print(f"概率期望=（中奖率 - 平均下注率 ）: {self.概率期望}")
        self.生成对比表格()


        # # 找出最大次数并创建统计表格
        # 最大次数 = max(
        #     max(self.中次数结果统计.keys(), default=0),
        #     max(self.不中次数结果统计.keys(), default=0)
        # )

        # # 创建数据字典
        # data = {
        #     '连对次数': [self.连对统计.get(i, 0) for i in range(1, 最大次数 + 1)],
        #     '连对概率': [self.中次数概率统计.get(i, 0) for i in range(1, 最大次数 + 1)],
        #     '连错次数': [self.连错统计.get(i, 0) for i in range(1, 最大次数 + 1)],
        #     '连错概率': [self.不中次数概率统计.get(i, 0) for i in range(1, 最大次数 + 1)]
        # }

        # # 创建DataFrame并打印带表格线的表格
        # df = pd.DataFrame(data).T
        # df.columns = [f'{i}次' for i in range(1, 最大次数 + 1)]
        # print("\n统计表格:")
        # pd.set_option('display.unicode.east_asian_width', True)
        # pd.set_option('display.colheader_justify', 'center')
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)
        # pd.set_option('display.float_format', '{:.3f}'.format)  # 设置浮点数格式为三位小数

        # # 打印表格
        # print(df.to_string(justify='center'))

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