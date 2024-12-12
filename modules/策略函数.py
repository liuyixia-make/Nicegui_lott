默认策略代码 = '''def 策略函数(历史数据):
    # 生成所有可能的三位数组合（000-999）
    所有可能 = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                号码 = f"{i}{j}{k}"
                所有可能.append(号码)
    
    # 只返回前500个组合
    return 所有可能[:500]
'''