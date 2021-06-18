from django.shortcuts import render
import os
import openpyxl
import pprint
from django.http import HttpResponse

def index(request):
    """
      Excel output from template
    """
    # Excelのテンプレートファイルの読み込み
    wb = openpyxl.load_workbook('C:\ExcelTemplate\workSheet.xlsx')

    sheet = wb['sheet1']
    sheet['C2'] = 'XXX'
    sheet['E2'] = 'new'
    sheet['A1'] = 'こんにちは'

# Excelを返すためにcontent_typeに「application/vnd.ms-excel」をセットします。

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'yes.xlsx'

    # データの書き込みを行なったExcelファイルを保存する
    wb.save(response)

    # 生成したHttpResponseをreturnする
    return response