def 随机生成(种子=None, 数量=1000):
    import random
    import time
    
    if 种子 is None:
        种子 = int(time.time() * 1000) % (2**32 - 1)  # 以当前时间的毫秒数作为种子
    
    random.seed(种子)
    
    随机_号码 = [f"{random.randint(0, 999):03d}" for _ in range(数量)]
    return 随机_号码


def 排列三号码(start_draw_num):  # start_draw_num 是期数    
    import pymysql
    db_config = {
        'host': '111.59.242.140',
        'port': 9033,
        'user': 'root',
        'password': 'Honghong998.',
        'database': 'lottery'
    }

    query = """
    SELECT lotteryDrawResult
    FROM pl3
    WHERE id >= (
        SELECT id FROM pl3 WHERE lotteryDrawNum = %s
    )
    ORDER BY id ASC;
    """

    try:
        with pymysql.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (start_draw_num,))
                results = cursor.fetchall()
                # 直接返回字符串格式
                号码列表 = [row[0] for row in results]
                return 号码列表
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return []

# # 调用函数并输出数据
# start_draw_num = 5001  # 这里填写你要从哪个 lotteryDrawNum 开始查询
# data = 排列三号码(start_draw_num)
# for record in data:
#     print(record)