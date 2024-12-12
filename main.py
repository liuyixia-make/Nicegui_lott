from nicegui import ui, app
import os
from modules.ui管理器 import UI管理器
from assets.styles import *
from modules.策略函数 import 默认策略代码

# 配置静态文件目录
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
app.add_static_files('/static', static_dir)

@ui.page('/')
def main():
    ui管理 = UI管理器()
    
    # ====================== 界面布局 ======================
    with ui.column().classes(MAIN_CONTAINER):
        # 主要内容区域
        with ui.splitter().classes(MAIN_CONTENT).style('width: 100%; min-height: 100vh;') as splitter:
            # 左面板
            with splitter.before:
                with ui.column().classes(GAP_2 + ' ' + W_FULL).style('min-width: 100%; width: 100%; min-height: 100px; resize: vertical;'):
                    # ------- 左上部分（数据获取区域）-------
                    with ui.card().classes(CARD_BASIC):
                        with ui.row().classes(W_FULL + ' justify-between items-center'):
                            ui.label('数据获取').classes(CARD_TITLE)
                        ui.separator()
                        
                        选项 = ui.radio(options=['随机生成', '排列三', '手动输入'], 
                                    value='随机生成', 
                                    on_change=lambda: ui管理.更新显示()).props('inline').classes(W_FULL)
                        
                        # 随机生成区域
                        随机生成区域 = ui.element('div').classes(W_FULL)
                        with 随机生成区域:
                            with ui.row().classes(GAP_4):
                                种子 = ui.number('随机种子').classes(NUMBER_FIELD)
                                数量 = ui.number('生成次数', value=1000).classes(NUMBER_FIELD)
                            ui.button('确定生成', on_click=lambda: ui管理.随机生成处理()).classes(MT_2)

                        # 排列三区域
                        排列三区域 = ui.element('div').classes(W_FULL)
                        with 排列三区域:
                            期数 = ui.input('期数', value='4001').classes(NUMBER_FIELD)
                            ui.button('确定获取', on_click=lambda: ui管理.排列三处理()).classes(MT_2)

                        # 手动输入区域
                        手动输入区域 = ui.element('div').classes(W_FULL)
                        with 手动输入区域:
                            with ui.row().classes(INPUT_GROUP):
                                手动输入 = ui.input('输入数据', placeholder='输入三位数，多个用逗号分隔'
                                ).props('outlined').classes(INPUT_FIELD)
                                ui.button('确定', on_click=lambda: ui管理.手动输入处理())

                        # 数据显示部分
                        ui.separator()
                        with ui.row().classes('w-full items-center justify-between'):
                            ui.label('数据显示:')
                            with ui.row().classes('gap-2'):
                                显示切换按钮 = ui.button('隐藏数据', on_click=lambda: ui管理.切换显示())
                                ui.button('清空数据', on_click=lambda: ui管理.清空数据()).props('outline')
                        显示区域 = ui.textarea('').style('width: 100%; min-height: 100px; resize: vertical;').props('readonly outlined')

                    # ------- 左中部分（策略函数编辑）-------
                    with ui.card().classes(CARD_BASIC):
                        ui.label('策略函数编辑').classes(CARD_TITLE)
                        策略代码 = ui.textarea(value=默认策略代码, placeholder='输入自定义策略函数'
                        ).style('width: 100%; min-height: 100px; resize: vertical;').props('outlined')
                        
                        with ui.row():
                            ui.button('确认策略', on_click=lambda: ui管理.更新策略())
                            ui.button('恢复默认', on_click=lambda: ui管理.恢复默认策略())

            # 右面板
            with splitter.after:
                with ui.column().classes(W_FULL).style('min-width: 100%; width: 100%; min-height: 100px; resize: vertical;'):
                    
                    # 状态显示卡片
                    with ui.card().classes(CARD_BASIC):
                        ui.label('运行状态').classes(CARD_TITLE)
                        
                        with ui.row().classes('items-center gap-2 w-full'):  # 添加w-full确保行占满宽度
                            with ui.row().classes('items-center gap-2'):
                                ui.label('历史数据: ')
                                历史数据状态 = ui.label('未录入').classes('text-red-500')
                                ui.label('策略函数: ')
                                策略函数状态 = ui.label('默认策略').classes('text-blue-500')
                            with ui.row().classes('ml-auto'):  # 使用ml-auto将按钮推到右边
                                ui.button('执行策略', on_click=lambda: ui管理.执行庄策略())
                        
                        ui.separator()
                        
                       # 添加批量测试控件
                        with ui.row().classes('items-center gap-2 w-full'):  # 添加w-full确保行占满宽度
                            with ui.row().classes('items-center gap-2'):
                                生成数量 = ui.number('生成数量', value=1000).classes(NUMBER_FIELD)
                                测试次数 = ui.number('测试次数', value=10).classes(NUMBER_FIELD)
                            with ui.row().classes('ml-auto'):  # 使用ml-auto将按钮推到右边
                                ui.button('批量测试', on_click=lambda: ui管理.批量测试())


                    
                    # 运行结果卡片
                    with ui.card().classes(CARD_BASIC + ' textarea-container'):
                        with ui.row().classes('w-full items-center'):  # 标题和按钮在同一行
                            ui.label('运行结果').classes(CARD_TITLE)
                            with ui.row():  # 使用ml-auto将按钮推到右边
                                ui.button('清除数据', on_click=lambda: ui管理.清除结果())
                        运行结果区 = ui.textarea(value='在这里显示运行结果...').props('readonly outlined width="100%"')

                    # 批量测试信息
                    with ui.card().classes(CARD_BASIC + ' textarea-container'):
                        with ui.row().classes('w-full items-center'):  # 标题和按钮在同一行
                            ui.label('批量测试信息').classes(CARD_TITLE)
                            with ui.row():  # 使用ml-auto将按钮推到右边
                                ui.button('清除批量数据', on_click=lambda: ui管理.清除批量测试())
                        批量测试信息区 = ui.textarea(value='在这里显示运行结果...\n执行批量测试时会显示当前执行到第几次测试').props('readonly outlined width="100%"')

    # 初始化UI管理器的组件引用
    ui管理.初始化组件引用(
        选项=选项,
        种子=种子,
        数量=数量,
        期数=期数,
        手动输入=手动输入,
        显示区域=显示区域,
        显示切换按钮=显示切换按钮,
        策略代码=策略代码,
        历史数据状态=历史数据状态,
        策略函数状态=策略函数状态,
        运行结果区=运行结果区,
        批量测试信息区=批量测试信息区,
        随机生成区域=随机生成区域,
        排列三区域=排列三区域,
        手动输入区域=手动输入区域,
        生成数量=生成数量,
        测试次数=测试次数,
    )

    # ====================== 初始化 ======================
    ui管理.更新显示()
    ui管理.更新状态显示()
    splitter.set_value(20)

    # 添加静态资源
    ui.add_head_html('''
        <link rel="stylesheet" href="/static/css/styles.css">
        <script src="/static/js/scripts.js"></script>
    ''')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        reload=True,
        port=8080,
        show=False,
        reconnect_timeout=10
    )