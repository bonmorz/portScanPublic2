def read_usage():
    wb = xlrd.open_workbook('tcpUsage.xlsx')
    # 按工作簿定位工作表
    sh = wb.sheet_by_name('Sheet1')
    # print(sh.nrows)  # 有效数据行数
    # print(sh.ncols)  # 有效数据列数
    # print(sh.cell(0, 0).value)  # 输出第一行第一列的值
    # print(sh.row_values(0))  # 输出第一行的所有值
    # 将数据和标题组合成字典
    # print(dict(zip(sh.row_values(0), sh.row_values(1))))
    # 遍历excel，打印所有数据
    usage_result = []
    usage_dict = {}
    for i in range(sh.nrows):
        # print(sh.row_values(i))
        usage_dict[sh.row_values(i)[0]] = sh.row_values(i)[1]
    # print(usage_result)
    #print(usage_dict)
    return usage_dict
