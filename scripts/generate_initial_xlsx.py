import openpyxl
from openpyxl import Workbook

# Seed data from the HTML file
questions = [
    (1, 'image-choice', '辨認動物', '<p><strong>圖中是甚麼種類的動物？</strong></p><p>請選擇正確的分類：</p>', '鳥類', '哺乳類', '魚類', '昆蟲', 'B', '', 'https://i.pinimg.com/736x/08/30/45/0830457efcb9967453099414443272a8.jpg'),
    (2, 'text-choice', '光合作用', '<p>植物的哪個部分通常進行光合作用？</p>', '根', '莖', '葉', '花', 'C', '', ''),
    (3, 'short-answer', '水的蒸發', '<p>一杯水放在桌上，三天後水位變低了。水去哪裡了？請寫出你的想法。</p>', '', '', '', '', '', '', ''),
    (4, 'text-choice', '重力', '<p>下面哪一種力會把物體往地面拉？</p>', '磁力', '摩擦力', '重力', '彈力', 'C', '', ''),
    (5, 'text-choice', '魚類呼吸', '<p>魚類用什麼呼吸？</p>', '肺', '皮膚', '', '氣管', 'C', '', ''),
    (6, 'text-choice', '自然資源', '<p>下列哪一個是「自然資源」？</p>', '塑膠', '玻璃', '陽光', '鋼鐵', 'C', '', ''),
    (7, 'text-choice', '太陽軌跡', '<p>一天中，太陽在天空中的位置怎樣變化？</p>', '從東邊升起，西邊落下', '從西邊升起，東邊落下', '一直停在頭頂', '從北邊移到南邊', 'A', '', ''),
    (8, 'fill-blank', '水的三態', '<p>水的三態分為固體、______ 和氣體。</p>', '', '', '', '', '液態', '液態|液體', ''),
    (9, 'text-choice', '昆蟲', '<p>下列哪一種動物是「昆蟲」？</p>', '蜘蛛', '蜜蜂', '蜈蚣', '牛', 'B', '', ''),
    (10, 'text-choice', '雨衣材料', '<p>哪一種材料最適合用來做雨衣？</p>', '棉布', '塑膠', '紙', '木頭', 'B', '', ''),
    (11, 'short-answer', '月亮發光', '<p>月亮會發光嗎？請簡單說明。</p>', '', '', '', '', '', '', ''),
    (12, 'text-choice', '心臟', '<p>人體中負責傳送血液的器官是？</p>', '胃', '心臟', '肝臟', '肺', 'B', '', ''),
    (13, 'text-choice', '冰塊融化', '<p>冰塊放在室溫環境下會變成什麼？</p>', '水蒸氣', '水', '冰', '霜', 'B', '', ''),
    (14, 'text-choice', '草食動物', '<p>下列哪一項是草食性動物？</p>', '獅子', '馬', '老虎', '狼', 'B', '', ''),
    (15, 'text-choice', '颱風', '<p>在澳門，熱帶氣旋又被稱作甚麼？</p>', '暴雨', '下雪', '颱風', '起霧', 'C', '', ''),
    (16, 'fill-blank', '植物生長條件', '<p>一棵樹的生長需要哪些條件？寫出兩個。</p>', '', '', '', '', '陽光', '陽光|水', ''),
    (17, 'text-choice', '導電體', '<p>哪一個是導電體？</p>', '橡皮擦', '鐵釘', '塑膠尺', '玻璃杯', 'B', '', ''),
    (18, 'text-choice', '燃燒需要', '<p>蠟燭燃燒時，需要哪一種氣體？</p>', '二氧化碳', '氧氣', '氮氣', '氫氣', 'B', '', ''),
    (19, 'text-choice', '影子', '<p>什麼是「影子」形成的原因？</p>', '光線被物體擋住', '物體自身發光', '光線直接穿過物體', '物體會變黑', 'A', '', ''),
    (20, 'short-answer', '保護色', '<p>寫出一種具有「保護色」的動物。</p>', '', '', '', '', '', '', ''),
    (21, 'text-choice', '水星', '<p>下面哪一個行星離太陽最近？</p>', '地球', '金星', '水星', '火星', 'C', '', ''),
    (22, 'text-choice', '仙人掌', '<p>為甚麼仙人掌的葉子是尖刺狀？</p>', '減少營養流失', '增加吸引空氣中水分的機會', '減少水分流失', '怕太陽曬', 'C', '', ''),
]

wb = Workbook()
ws = wb.active
ws.title = '題庫'

# Header
headers = ['ID', '題型', '標題', '題目內容', '選項A', '選項B', '選項C', '選項D', '正確答案', '多組答案(|分隔)', '圖片網址']
ws.append(headers)

# Data
for q in questions:
    ws.append(q)

# Column widths
ws.column_dimensions['A'].width = 5
ws.column_dimensions['B'].width = 16
ws.column_dimensions['C'].width = 24
ws.column_dimensions['D'].width = 50
ws.column_dimensions['E'].width = 16
ws.column_dimensions['F'].width = 16
ws.column_dimensions['G'].width = 16
ws.column_dimensions['H'].width = 16
ws.column_dimensions['I'].width = 16
ws.column_dimensions['J'].width = 24
ws.column_dimensions['K'].width = 40

wb.save('questions.xlsx')
print('Successfully created questions.xlsx with %d questions' % len(questions))
