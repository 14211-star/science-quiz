import openpyxl
import json
import sys
from pathlib import Path

def parse_xlsx():
    xlsx_path = Path('questions.xlsx')
    json_path = Path('questions.json')
    
    if not xlsx_path.exists():
        print("Error: questions.xlsx not found")
        sys.exit(1)
    
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active
    
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append(row)
    
    if len(rows) < 2:
        print("Error: XLSX has no data rows")
        sys.exit(1)
    
    questions = []
    for i in range(1, len(rows)):
        row = rows[i]
        if row[0] is None or row[0] == '':
            continue
        
        q = {
            'id': int(row[0]) if row[0] else (100 + i),
            'type': str(row[1]).strip() if row[1] else 'text-choice',
            'title': str(row[2]).strip() if row[2] else '',
            'content': str(row[3]).strip() if row[3] else '',
            'correctAnswer': {'q': ''},
            'multiAnswers': None,
            'image': None
        }
        
        # Parse options (columns E-H, indices 4-7)
        opt_labels = 'ABCDEFGH'
        opts = []
        for j in range(4, 8):
            val = str(row[j]).strip() if row[j] else ''
            if val:
                label = opt_labels[len(opts)]
                opts.append({
                    'label': label,
                    'value': label,
                    'text': val,
                    'image': ''
                })
        if opts:
            q['options'] = opts
        
        # Parse correct answer (column I, index 8)
        if row[8]:
            q['correctAnswer'] = {'q': str(row[8]).strip()}
        
        # Parse multi-answers (column J, index 9)
        if row[9]:
            multi = str(row[9]).strip()
            if multi:
                q['multiAnswers'] = {
                    'q': [s.strip() for s in multi.split('|') if s.strip()]
                }
        
        # Parse image URL (column K, index 10)
        if row[10]:
            img = str(row[10]).strip()
            if img:
                q['image'] = img
        
        questions.append(q)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully parsed {len(questions)} questions to questions.json")

if __name__ == '__main__':
    parse_xlsx()
