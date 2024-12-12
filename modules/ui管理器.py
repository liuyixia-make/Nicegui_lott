# modules/ui管理器.py

from nicegui import ui
from modules.数据函数 import 随机生成, 排列三号码
from modules.庄函数 import Pick3_庄模板
from modules.策略函数 import 默认策略代码
import sys
import io
import random
import time
from tqdm import tqdm

class UI管理器:
    def __init__(self):
        import io
        import sys
        self.数据 = []  # 存储生成的数据
        self.显示状态 = True  # 控制数据显示区域的显示状态
        self.当前策略 = 默认策略代码
        self.组件 = {}  # 存储UI组件引用
        self.偏差列表 = []
        self.进度条 = None  # 初始化进度条属性

        # 添加新的数据结构
        self.统计数据 = {
            '下注数量': [],  # 每期下注数量
            '是否中奖': [],  # 每期是否中奖
            '偏差合集': [],  # 每轮测试的偏差值
            '购买比例合集': [],  # 每轮测试的购买比例
            '连对统计': {},  # 动态字典，存储连对统计
            '连错统计': {}   # 动态字典，存储连错统计
        }
  
    
    def 初始化组件引用(self, **kwargs):
        """初始化所有UI组件的引用"""
        self.组件 = kwargs
        self.单次测试状态 = kwargs.get('单次测试状态')
        

         #运行结果区清除按钮
    def 清除结果(self):
        """清除运行结果区的内容"""
        self.组件['运行结果区'].value = ''
        ui.notify('已清除结果', type='info')
    
    def 清除批量测试(self):
        """清除批量测试信息区的内容"""
        self.组件['批量测试信息区'].value = ''
        ui.notify('已清除批量测试信息', type='info')

    
    def 更新状态显示(self):
        """更新状态标签显示"""
        if len(self.组件['显示区域'].value.strip()) > 0:
            self.组件['历史数据状态'].text = '已录入'
            self.组件['历史数据状态'].classes('text-green-500', remove='text-red-500')
        else:
            self.组件['历史数据状态'].text = '未录入'
            self.组件['历史数据状态'].classes('text-red-500', remove='text-green-500')
        
        if self.组件['策略代码'].value == 默认策略代码:
            self.组件['策略函数状态'].text = '默认策略'
            self.组件['策略函数状态'].classes('text-blue-500', remove='text-green-500 text-red-500')
        elif self.组件['策略代码'].value.strip():
            self.组件['策略函数状态'].text = '自定义策略'
            self.组件['策略函数状态'].classes('text-green-500', remove='text-blue-500 text-red-500')
        else:
            self.组件['策略函数状态'].text = '未输入'
            self.组件['策略函数状态'].classes('text-red-500', remove='text-green-500 text-blue-500')

    def 更新显示(self):
        """更新界面显示状态"""
        当前选项 = self.组件['选项'].value
        self.组件['随机生成区域'].set_visibility(当前选项 == '随机生成')
        self.组件['排列三区域'].set_visibility(当前选项 == '排列三')
        self.组件['手动输入区域'].set_visibility(当前选项 == '手动输入')
    
    def 随机生成处理(self):
        """处理随机生成按钮点击事件"""
        try:
            种子值 = None if self.组件['种子'].value is None else int(self.组件['种子'].value)
            数量值 = int(self.组件['数量'].value) if self.组件['数量'].value else 1000
            
            结果 = 随机生成(种子=种子值, 数量=数量值)
            self.数据.clear()
            self.数据.extend(结果)
            self.组件['显示区域'].value = str(self.数据)  # 直接显示列表
            self.更新状态显示()
            ui.notify('随机数据生成成功', type='positive')
            
        except Exception as e:
            ui.notify(f'生成失败：{str(e)}', type='negative')

    def 排列三处理(self):
        """处理排列三按钮点击事件"""
        try:
            结果 = 排列三号码(self.组件['期数'].value)
            self.数据.clear()
            self.数据.extend(结果)
            self.组件['显示区域'].value = str(self.数据)  # 直接显示列表
            self.更新状态显示()
        except Exception as e:
            ui.notify(f'获取失败：{str(e)}', type='negative')

    def 手动输入处理(self):
        """处理手动输入按钮点击事件"""
        try:
            输入文本 = self.组件['手动输入'].value
            if ',' in 输入文本:
                新数据 = [x.strip() for x in 输入文本.split(',')]
            else:
                新数据 = [输入文本.strip()]
            
            for num in 新数据:
                if not (len(num) == 3 and num.isdigit()):
                    raise ValueError("每个数字必须是3位数")
                
            if len(self.数据) == 0:
                self.数据.extend(新数据)
            else:
                self.数据.extend(新数据)
            
            self.组件['显示区域'].value = str(self.数据)  # 直接显示列表
            self.组件['手动输入'].value = ''
            self.更新状态显示()
        except Exception:
            ui.notify('数据格式错误，请检查输入（需要输入3位数）', type='warning')
    
    def 清空数据(self):
        """清空数据并重置显示"""
        self.数据.clear()
        self.组件['显示区域'].value = ""
        self.更新状态显示()
    
    def 切换显示(self):
        """切换数据显示区域的显示/隐藏状态"""
        self.显示状态 = not self.显示状态
        self.组件['显示区域'].set_visibility(self.显示状态)
        self.组件['显示切换按钮'].text = '隐藏数据' if self.显示状态 else '显示数据'
    
    def 更新策略(self):
        """更新策略函数"""
        self.当前策略 = self.组件['策略代码'].value
        ui.notify('策略函数已更新')
        self.更新状态显示()
    
    def 恢复默认策略(self):
        """恢复默认策略"""
        self.组件['策略代码'].value = 默认策略代码
        self.更新状态显示()
    

    def 获取策略函数(local_dict):
        """从local_dict中获取第一个函数对象"""
        for value in local_dict.values():
            if callable(value) and value.__class__.__name__ == 'function':
                return value
        raise ValueError("未找到任何函数定义")
    
    def 执行庄策略(self):
        """执行庄策略"""
        try:
            if not self.组件['显示区域'].value.strip():
                ui.notify('请先输入历史数据', type='warning')
                return

            原始文本 = self.组件['显示区域'].value.strip()
            清理文本 = 原始文本.strip('[]')
            历史数据 = [x.strip().strip("'\"") for x in 清理文本.split(',') if x.strip().strip("'\"")]
            
            庄实例 = Pick3_庄模板()
            
            # 处理策略代码的缩进
            策略代码行 = self.当前策略.strip().split('\n')
            正确缩进代码 = []
            for i, 行 in enumerate(策略代码行):
                if i == 0:  # 函数定义行
                    正确缩进代码.append(行)
                else:  # 函数体需要缩进
                    if 行.strip():  # 如果不是空行
                        正确缩进代码.append('    ' + 行)  # 添加4个空格的缩进
                    else:
                        正确缩进代码.append(行)
            
            处理后的代码 = '\n'.join(正确缩进代码)
            
            local_dict = {}
            # 在执行前打印处理后的代码，方便调试
            print("执行的代码：")
            print(处理后的代码)
            exec(处理后的代码, globals(), local_dict)
            
            # 获取第一个函数对象
            for value in local_dict.values():
                if callable(value) and value.__class__.__name__ == 'function':
                    用户函数 = value
                    break
            else:
                raise ValueError("未找到任何函数定义")
            
            庄实例.执行预测(历史数据, 用户函数)
            
            output = io.StringIO()
            sys.stdout = output
            庄实例.显示结果()
            sys.stdout = sys.__stdout__
            结果文本 = output.getvalue()
            
            self.组件['运行结果区'].value = 结果文本
            ui.notify('策略执行成功', type='positive')
            
        except Exception as e:
            ui.notify(f'执行失败：{str(e)}', type='negative')
    
    
    













    # async def 批量测试(self):
    #     """执行批量测试"""
    #     try:
    #         # 初始化统计数据
    #         self.统计数据 = {
    #             '偏差合集': [],
    #             '购买比例合集': [],
    #             '连对统计': {},
    #             '连错统计': {}
    #         }
            
    #         生成数量 = int(self.组件['生成数量'].value)
    #         测试次数 = int(self.组件['测试次数'].value)

    #         if 生成数量 <= 0 or 测试次数 <= 0:
    #             ui.notify('生成数量和测试次数必须大于0', type='warning')
    #             return

    #         总结果 = []
            
    #         # 在开始前先显示初始信息
    #         self.组件['批量测试信息区'].value = f"开始执行批量测试...\n当前进度：0/{测试次数}"
    #         await ui.run_javascript('setTimeout(() => {}, 0)')
            
    #         for 当前测试序号 in range(测试次数):
    #             # 更新进度信息
    #             self.组件['批量测试信息区'].value = f"正在执行批量测试...\n当前进度：{当前测试序号 + 1}/{测试次数}"
    #             await ui.run_javascript('setTimeout(() => {}, 0)')
                
    #             # 使用时间戳和随机数组合作为种子
    #             current_seed = int(time.time() * 1000000) + random.randint(1, 1000000) + 当前测试序号
    #             random.seed(current_seed)
    #             历史数据 = [f"{random.randint(0, 999):03d}" for _ in range(生成数量)]
                
    #             庄实例 = Pick3_庄模板()
                
    #             # 执行策略函数
    #             local_dict = {}
    #             exec(self.当前策略, globals(), local_dict)
    #             用户函数 = list(local_dict.values())[0]
                
    #             庄实例.执行预测(历史数据, 用户函数)
                
    #             # 捕获输出
    #             output = io.StringIO()
    #             sys.stdout = output
    #             庄实例.显示结果()
    #             sys.stdout = sys.__stdout__
    #             结果文本 = output.getvalue()
                
    #             # 添加测试序号
    #             总结果.append(f"第{当前测试序号 + 1}次测试结果:\n{结果文本}\n{'=' * 50}\n")
                
    #             # 从结果文本中提取数据
    #             lines = 结果文本.split('\n')
    #             表格模式 = False
    #             连对行 = None
    #             连错行 = None
                
    #             中奖次数 = 0
    #             平均下注数 = 0.0
                
    #             for line in lines:
    #                 if '中奖次数:' in line:
    #                     try:
    #                         中奖次数 = int(line.split('(')[0].split(':')[1].strip())
    #                     except ValueError:
    #                         print("无法解析中奖次数:", line)
    #                 elif '平均下注数:' in line:
    #                     try:
    #                         平均下注数 = float(line.split(':')[1].strip())
    #                     except ValueError:
    #                         print("无法解析平均下注数:", line)
    #                 elif '统计表格:' in line:
    #                     表格模式 = True
    #                 elif 表格模式 and '连对' in line:
    #                     连对行 = line
    #                 elif 表格模式 and '连错' in line:
    #                     连错行 = line
                
    #             # 处理连对数据
    #             if 连对行:
    #                 parts = 连对行.split()
    #                 for i in range(1, len(parts)):
    #                     if parts[i].isdigit():
    #                         连对长度 = i + 1  # 因为表格从2次开始
    #                         次数 = int(parts[i])
    #                         if 连对长度 not in self.统计数据['连对统计']:
    #                             self.统计数据['连对统计'][连对长度] = 0
    #                         self.统计数据['连对统计'][连对长度] += 次数
                
    #             # 处理连错数据
    #             if 连错行:
    #                 parts = 连错行.split()
    #                 for i in range(1, len(parts)):
    #                     if parts[i].isdigit():
    #                         连错长度 = i + 1  # 因为表格从2次开始
    #                         次数 = int(parts[i])
    #                         if 连错长度 not in self.统计数据['连错统计']:
    #                             self.统计数据['连错统计'][连错长度] = 0
    #                         self.统计数据['连错统计'][连错长度] += 次数
                
    #             # 偏差计算
    #             try:
    #                 偏差值 = ((中奖次数 / 1000) - (平均下注数 / 1000)) / 生成数量
    #                 self.统计数据['偏差合集'].append(偏差值)
    #                 self.统计数据['购买比例合集'].append(平均下注数 / 生成数量)
    #             except ZeroDivisionError:
    #                 print("计算偏差时发生除零错误")
                
    #         # 计算最终统计结果
    #         if self.统计数据['偏差合集']:
    #             最终偏差 = sum(self.统计数据['偏差合集']) / len(self.统计数据['偏差合集'])
    #             平均购买比例 = sum(self.统计数据['购买比例合集']) / len(self.统计数据['购买比例合集'])
                
    #             统计信息 = f"""统计结果:
    #     实验次数: {len(self.统计数据['偏差合集'])}/{测试次数}
    #     平均偏差: {最终偏差:.4f}
    #     平均购买比例: {平均购买比例:.4f}

    #     连对统计:
    #     {'\n'.join(f'{k}连对在所有测试中共出现: {v}次' for k, v in sorted(self.统计数据['连对统计'].items()))}

    #     连错统计:
    #     {'\n'.join(f'{k}连错在所有测试中共出现: {v}次' for k, v in sorted(self.统计数据['连错统计'].items()))}
    #     {'=' * 50}\n"""
    #         else:
    #             统计信息 = "没有有效的测试数据可以统计\n" + ('=' * 50) + "\n"

    #         # 显示结果
    #         self.组件['批量测试信息区'].value = 统计信息 + '\n'.join(总结果)
    #         ui.notify('批量测试完成', type='positive')
            
    #     except Exception as e:
    #         ui.notify(f'批量测试失败：{str(e)}', type='negative')
    #         print(f"错误详情：{str(e)}")



    async def 批量测试(self):
        """执行批量测试"""
        try:
            # 初始化统计数据
            self.统计数据 = {
                '偏差合集': [],
                '购买比例合集': [],
                '连对统计': {},
                '连错统计': {}
            }
            
            生成数量 = int(self.组件['生成数量'].value)
            测试次数 = int(self.组件['测试次数'].value)

            if 生成数量 <= 0 or 测试次数 <= 0:
                ui.notify('生成数量和测试次数必须大于0', type='warning')
                return

            总结果 = []
            
            # 在开始前先显示初始信息
            self.组件['批量测试信息区'].value = f"开始执行批量测试...\n当前进度：0/{测试次数}"
            await ui.run_javascript('setTimeout(() => {}, 0)')
            
            for 当前测试序号 in range(测试次数):
                # 更新进度信息
                self.组件['批量测试信息区'].value = f"正在执行批量测试...\n当前进度：{当前测试序号 + 1}/{测试次数}"
                await ui.run_javascript('setTimeout(() => {}, 0)')
                
                # 使用时间戳和随机数组合作为种子
                current_seed = int(time.time() * 1000000) + random.randint(1, 1000000) + 当前测试序号
                random.seed(current_seed)
                历史数据 = [f"{random.randint(0, 999):03d}" for _ in range(生成数量)]
                
                庄实例 = Pick3_庄模板()
                
                # 执行策略函数
                local_dict = {}
                exec(self.当前策略, globals(), local_dict)
                用户函数 = list(local_dict.values())[0]
                
                庄实例.执行预测(历史数据, 用户函数)
                
                # 捕获输出
                output = io.StringIO()
                sys.stdout = output
                庄实例.显示结果()
                sys.stdout = sys.__stdout__
                结果文本 = output.getvalue()
                
                # 添加测试序号
                分隔线 = "=" * 50
                总结果.append(f"第{当前测试序号 + 1}次测试结果:\n{结果文本}\n{分隔线}\n")
                
                # 从结果文本中提取数据
                lines = 结果文本.split('\n')
                表格模式 = False
                连对行 = None
                连错行 = None
                
                中奖次数 = 0
                平均下注数 = 0.0
                
                for line in lines:
                    if '中奖次数:' in line:
                        try:
                            中奖次数 = int(line.split('(')[0].split(':')[1].strip())
                        except ValueError:
                            print("无法解析中奖次数:", line)
                    elif '平均下注数:' in line:
                        try:
                            平均下注数 = float(line.split(':')[1].strip())
                        except ValueError:
                            print("无法解析平均下注数:", line)
                    elif '统计表格:' in line:
                        表格模式 = True
                    elif 表格模式 and '连对' in line:
                        连对行 = line
                    elif 表格模式 and '连错' in line:
                        连错行 = line
                
                # 处理连对数据
                if 连对行:
                    parts = 连对行.split()
                    for i in range(1, len(parts)):
                        if parts[i].isdigit():
                            连对长度 = i + 1  # 因为表格从2次开始
                            次数 = int(parts[i])
                            if 连对长度 not in self.统计数据['连对统计']:
                                self.统计数据['连对统计'][连对长度] = 0
                            self.统计数据['连对统计'][连对长度] += 次数
                
                # 处理连错数据
                if 连错行:
                    parts = 连错行.split()
                    for i in range(1, len(parts)):
                        if parts[i].isdigit():
                            连错长度 = i + 1  # 因为表格从2次开始
                            次数 = int(parts[i])
                            if 连错长度 not in self.统计数据['连错统计']:
                                self.统计数据['连错统计'][连错长度] = 0
                            self.统计数据['连错统计'][连错长度] += 次数
                
                # 偏差计算
                try:
                    偏差值 = ((中奖次数 / 1000) - (平均下注数 / 1000)) / 生成数量
                    self.统计数据['偏差合集'].append(偏差值)
                    self.统计数据['购买比例合集'].append(平均下注数 / 生成数量)
                except ZeroDivisionError:
                    print("计算偏差时发生除零错误")
                
            # 计算最终统计结果
            if self.统计数据['偏差合集']:
                最终偏差 = sum(self.统计数据['偏差合集']) / len(self.统计数据['偏差合集'])
                平均购买比例 = sum(self.统计数据['购买比例合集']) / len(self.统计数据['购买比例合集'])
                分隔线 = "=" * 50
                
                连对统计文本 = '\n'.join(f'{k}连对在所有测试中共出现: {v}次' for k, v in sorted(self.统计数据['连对统计'].items()))
                连错统计文本 = '\n'.join(f'{k}连错在所有测试中共出现: {v}次' for k, v in sorted(self.统计数据['连错统计'].items()))
                
                统计信息 = f"""统计结果:
        实验次数: {len(self.统计数据['偏差合集'])}/{测试次数}
        平均偏差: {最终偏差:.4f}
        平均购买比例: {平均购买比例:.4f}

        连对统计:
        {连对统计文本}

        连错统计:
        {连错统计文本}
        {分隔线}\n"""
            else:
                分隔线 = "=" * 50
                统计信息 = f"没有有效的测试数据可以统计\n{分隔线}\n"

            # 显示结果
            self.组件['批量测试信息区'].value = 统计信息 + '\n'.join(总结果)
            ui.notify('批量测试完成', type='positive')
            
        except Exception as e:
            ui.notify(f'批量测试失败：{str(e)}', type='negative')
            print(f"错误详情：{str(e)}")