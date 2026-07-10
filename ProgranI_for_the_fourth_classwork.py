import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

orders = pd.DataFrame({
    'order_id': [f'O{number}' for number in range(1001, 1019)],
    'region': ['华东','华北','华南','华东','西南','华北','华南','华东','西南','华北','华东','华南','西南','华东','华北','华南','华东','西南'],
    'product': ['机械键盘','无线鼠标','显示器','扩展坞','机械键盘','显示器','无线鼠标','显示器','扩展坞','机械键盘','无线鼠标','扩展坞','显示器','机械键盘','扩展坞','显示器','无线鼠标','机械键盘'],
    'category': ['外设','外设','显示设备','配件','外设','显示设备','外设','显示设备','配件','外设','外设','配件','显示设备','外设','配件','显示设备','外设','外设'],
    'quantity': [2,3,1,4,5,2,6,1,3,2,8,2,1,3,5,2,4,6],
    'unit_price': [289,129,1299,399,289,1299,129,1299,399,289,129,399,1299,289,399,1299,129,289],
    'member_level': ['金卡','普通','银卡','金卡','银卡','普通','金卡','银卡','普通','金卡','银卡','金卡','普通','银卡','金卡','金卡','普通','银卡'],
    'coupon_rate': [0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.08,0.00,0.10],
    'salesperson': ['小林','小周','小陈','小林','小赵','小周','小陈','小林','小赵','小周','小林','小陈','小赵','小林','小周','小陈','小林','小赵']
})
# 1. 行数、列数、列名
print("1. 数据规模：")
print(f"行数：{orders.shape[0]}，列数：{orders.shape[1]}")
print(f"所有列名：{orders.columns.tolist()}\n")

# 2. 单列与多列取值及类型
region_series = orders['region']
three_cols_df = orders[['order_id', 'product', 'quantity']]
print("2. 数据类型：")
print(f"region单列类型：{type(region_series)}")
print(f"三列数据类型：{type(three_cols_df)}\n")

# 3. iloc 取第4~8行、前4列（行索引从0开始，第4行对应索引3，第8行对应索引7，左闭右开）
print("3. iloc切片结果：")
print(orders.iloc[3:8, :4])
print()

# 4. loc 筛选华东订单
print("4. 华东地区订单：")
east_china_orders = orders.loc[orders['region'] == '华东', ['order_id', 'product', 'member_level']]
print(east_china_orders)
# 基于原表生成新表，不修改原始orders
analysis = orders.assign(
    # 商品总金额
    gross_amount = orders['quantity'] * orders['unit_price'],
    # 会员折扣：金卡10%，银卡5%，普通0%
    member_discount = np.where(orders['member_level'] == '金卡', 0.10,
                              np.where(orders['member_level'] == '银卡', 0.05, 0.00)),
    # 优惠后应付金额
    payable_amount = lambda df: df['gross_amount'] * (1 - df['member_discount']) * (1 - df['coupon_rate']),
    # 运费：满1000免运费，否则20元
    shipping_fee = lambda df: np.where(df['payable_amount'] >= 1000, 0, 20),
    # 最终实付金额
    final_amount = lambda df: df['payable_amount'] + df['shipping_fee']
).round(2)  # 金额统一保留两位小数

# 展示前8行核心结算字段
print(analysis[['order_id', 'gross_amount', 'member_discount', 'payable_amount', 'shipping_fee', 'final_amount']].head(8))
# 分别定义3个布尔条件
mask_region = analysis['region'].isin(['华东', '华南'])  # 地区为华东或华南
mask_amount = analysis['final_amount'] >= 700           # 最终金额≥700
mask_quality = (analysis['quantity'] >= 2) | (analysis['member_level'] == '金卡')  # 数量≥2 或 金卡会员

# 组合条件
final_mask = mask_region & mask_amount & mask_quality

# 筛选指定列并按金额降序
key_orders = (
    analysis.loc[final_mask, ['order_id', 'region', 'product', 'quantity', 'member_level', 'final_amount']]
    .sort_values('final_amount', ascending=False)
    .reset_index(drop=True)
)

print("重点跟进订单：")
print(key_orders)
def add_order_level(df):
    # 不修改原表，先复制再操作
    result_df = df.copy()
    # 嵌套np.where实现三级分类
    result_df['order_level'] = np.where(result_df['final_amount'] >= 2000, '战略订单',
                                       np.where(result_df['final_amount'] >= 1000, '重点订单', '普通订单'))
    return result_df

# 通过pipe调用函数
leveled_orders = analysis.pipe(add_order_level)

# 统计各等级订单数量
level_count = leveled_orders['order_level'].value_counts()
print("各等级订单数量：")
print(level_count)
region_report = (
    analysis                     # 从analysis出发
    .pipe(add_order_level)       # 1. 添加订单等级
    .query('final_amount >= 500')# 2. 筛选金额≥500的订单
    .groupby(['region', 'order_level'])  # 3. 按地区+订单等级分组
    .agg(                        # 4. 多指标聚合
        order_count = ('order_id', 'count'),
        quantity_sum = ('quantity', 'sum'),
        revenue_sum = ('final_amount', 'sum'),
        revenue_mean = ('final_amount', 'mean')
    )
    .sort_values('revenue_sum', ascending=False)  # 5. 按营收合计降序
    .reset_index()               # 重置索引便于查看
)

print("地区经营汇总报表：")
print(region_report.round(2))
# 1. 计算每位销售的总成交金额，找出最高者
sales_revenue = analysis.groupby('salesperson')['final_amount'].sum().sort_values(ascending=False)
top_salesperson = sales_revenue.index[0]
total_revenue = sales_revenue.iloc[0]

# 2. 筛选该销售数据，计算各地区成交金额，找出核心地区
top_sales_data = analysis[analysis['salesperson'] == top_salesperson]
region_revenue = top_sales_data.groupby('region')['final_amount'].sum().sort_values(ascending=False)
core_region = region_revenue.index[0]
core_region_revenue = region_revenue.iloc[0]

# 3. 计算地区贡献率
contribution_ratio = core_region_revenue / total_revenue

# 整理输出结果
diagnose_result = pd.Series({
    '销售人员': top_salesperson,
    '核心地区': core_region,
    '总成交金额': round(total_revenue, 2),
    '核心地区金额': round(core_region_revenue, 2),
    '地区贡献率': f"{contribution_ratio:.2%}"
})

print("销售经营诊断结果：")
print(diagnose_result)
