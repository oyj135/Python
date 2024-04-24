"""
[模块使用]:
    DrissionPage
    csv
    time
"""
import time

# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入csv模块
import csv

# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '酒店',
    '评论',
    '价格',
    '城市',
    '区域',
    '地址',
    '距离',
    '纬度',
    '经度',
    '评分',
    '评价',
    '环境',
    '卫生',
    '服务',
    '设施',
    '标签',
])
csv_writer.writeheader()

# 打开浏览器
dp = ChromiumPage()
# 监听数据包
dp.listen.start('json/HotelSearch')
# 访问网站
dp.get('https://hotels.ctrip.com/hotels/list?countryId=1&city=2&checkin=2024/05/01&checkout=2024/05/06&optionId=2&optionType=City&directSearch=0&display=%E4%B8%8A%E6%B5%B7&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&')

# for循环下滑页面
for page in range(1, 15):
    print(f'正在采集第{page}页的数据内容')
    if page > 4:
        # 元素定位 -> 通过css选择器定位元素
        next_page = dp.ele('css:.btn-box span')
        # 判断是否出现点击按钮
        if next_page.text == '搜索更多酒店':
            # 点击搜索更多酒店
            next_page.click()
            dp.wait.load_start(2)
            next_page = dp.ele('css:.btn-box span')
    # 等待数据包加载
    resp = dp.listen.wait()
    # 获取响应内容
    json_data = resp.response.body
    # 解析数据，提取酒店信息所在列表
    hotelList = json_data['Response']['hotelList']['list']
    # for循环遍历，提取列表里面的元素
    for index in hotelList:
        """ 提取具体数据内容，保存到字典里面 """
        dit = {
            '酒店': index['base']['hotelName'],
            '评论': index['comment'].get('content'),
            '价格': index['money']['price'],
            '城市': index['position']['cityName'],
            '区域': index['position']['area'],
            '地址': index['position']['address'],
            '距离': index['position']['poi'],
            '纬度': index['position']['lat'],
            '经度': index['position']['lng'],
            '评分': index['score']['number'],
            '评价': index['score']['desc'],
            '环境': index['score']['subScore'][0]['number'],
            '卫生': index['score']['subScore'][1]['number'],
            '服务': index['score']['subScore'][2]['number'],
            '设施': index['score']['subScore'][3]['number'],
            '标签': ' '.join(index['base']['tags']),
        }
        # 写入数据
        csv_writer.writerow(dit)
        print(dit)
    # 下滑页面到底部
    dp.scroll.to_bottom()
