

class Pick3_庄模板:
    def __init__(self, 启用资金=False) -> None:
        #  self.投注结果 [中W,不中L，没买-]
        self.投注结果 = []
        #   统计
        self.中次数结果统计 = {}   
        self.不中次数结果统计 = {} 
        self.不买次数结果统计 = {} 

        # 仅买入统计
        self.仅买入结果 = []  # 新增：只记录W和L
        self.仅买入中次数统计 = {}   
        self.仅买入不中次数统计 = {} 

        

        # 资金管理开关和相关属性
        self.启用资金 = 启用资金
        if 启用资金:
            self.初始资金 = 10000
            self.当前资金 = self.初始资金
            self.单注金额 = 1 
            self.满注 = 1000
            self.赔率 = 0.97     
            self.资金曲线 = [self.初始资金]
            self.倍数 = 1  # 添加倍数属性


    def 动作(self, 类型, 投注集合=None):
        """
        记录投注结果和更新资金（如果启用）
        类型: 'W'(中), 'L'(不中), '-'(不买)
        """
        if 类型 in ['W', 'L', '-']:
            self.投注结果.append(类型)
            # 只记录买入的结果
            if 类型 in ['W', 'L']:
                self.仅买入结果.append(类型)
            
            # 如果启用资金管理，在这里统一处理资金
            if self.启用资金 and 投注集合 is not None:
                购买注数 = len(投注集合)
                
                if 类型 == '-':
                    self.资金曲线.append(self.当前资金)
                elif 类型 == 'W':
                    奖金 = (self.单注金额 * self.满注) * self.赔率 * self.倍数
                    投注成本 = 购买注数 * self.单注金额 * self.倍数
                    self.当前资金 = self.当前资金 + 奖金 - 投注成本
                    self.资金曲线.append(self.当前资金)
                else:  # 类型 == 'L'
                    投注成本 = 购买注数 * self.单注金额 * self.倍数
                    self.当前资金 -= 投注成本
                    self.资金曲线.append(self.当前资金)

    def 执行预测(self, 历史数据):
        """
        遍历历史数据进行预测和记录
        """
        for i in range(len(历史数据)):
            当前号码 = 历史数据[i]
            前期数据 = 历史数据[:i]
            预测结果 = self.预测(前期数据)
            
            if not 预测结果:
                self.动作('-', 预测结果)
            elif 当前号码 in 预测结果:
                self.动作('W', 预测结果)
            else:
                self.动作('L', 预测结果)

    def 统计(self):
        # 统计完整结果（包含不买）
        if self.投注结果:
            当前符号 = self.投注结果[0]
            连续次数 = 1
            
            for i in range(1, len(self.投注结果)):
                if self.投注结果[i] == 当前符号:
                    连续次数 += 1
                else:
                    if 当前符号 == 'W':
                        self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
                    elif 当前符号 == 'L':
                        self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
                    elif 当前符号 == '-':
                        self.不买次数结果统计[连续次数] = self.不买次数结果统计.get(连续次数, 0) + 1
                    
                    当前符号 = self.投注结果[i]
                    连续次数 = 1
            
            # 处理最后一个连续序列
            if 当前符号 == 'W':
                self.中次数结果统计[连续次数] = self.中次数结果统计.get(连续次数, 0) + 1
            elif 当前符号 == 'L':
                self.不中次数结果统计[连续次数] = self.不中次数结果统计.get(连续次数, 0) + 1
            elif 当前符号 == '-':
                self.不买次数结果统计[连续次数] = self.不买次数结果统计.get(连续次数, 0) + 1

        # 统计仅买入结果
        if self.仅买入结果:
            当前符号 = self.仅买入结果[0]
            连续次数 = 1
            
            for i in range(1, len(self.仅买入结果)):
                if self.仅买入结果[i] == 当前符号:
                    连续次数 += 1
                else:
                    if 当前符号 == 'W':
                        self.仅买入中次数统计[连续次数] = self.仅买入中次数统计.get(连续次数, 0) + 1
                    elif 当前符号 == 'L':
                        self.仅买入不中次数统计[连续次数] = self.仅买入不中次数统计.get(连续次数, 0) + 1
                    
                    当前符号 = self.仅买入结果[i]
                    连续次数 = 1
            
            # 处理最后一个连续序列
            if 当前符号 == 'W':
                self.仅买入中次数统计[连续次数] = self.仅买入中次数统计.get(连续次数, 0) + 1
            elif 当前符号 == 'L':
                self.仅买入不中次数统计[连续次数] = self.仅买入不中次数统计.get(连续次数, 0) + 1


    def 显示结果(self, 包含不买=True):
        if 包含不买:
            print("投注记录:", self.投注结果)
            print("\n连续中奖统计:", self.中次数结果统计)
            print("连续不中统计:", self.不中次数结果统计)
            print("连续不买统计:", self.不买次数结果统计)
        else:
            print("投注记录(仅买入):", self.仅买入结果)
            print("\n连续中奖统计:", self.仅买入中次数统计)
            print("连续不中统计:", self.仅买入不中次数统计)
        
        if self.启用资金:
            print(f"\n初始资金: {self.初始资金:.2f}元")
            print(f"当前资金: {self.当前资金:.2f}元")
            收益率 = (self.当前资金 - self.初始资金) / self.初始资金 * 100
            print(f"收益率: {收益率:.2f}%")
            # 删除所有 matplotlib 相关代码，资金曲线的显示将在 main.py 中通过 plotly 实现
            




