"""
        - y, d : 0 ~ 9까지의 숫자 
        파일 관련
        - file_to_ignore_reg: 무시할 파일 
        - file_evid_reg: 증거로 분류할 파일 

        준비서면 내용 관련        
        - split_reg: 문장을 끊는 기준
        - year_reg, month_reg: 준비서면 내용에서 날짜인지 여부 기준 
        - evid_reg: 준비서면 내용에서 증거인지 판단할 근거 

        useless_token: 무시할 문장
        
        r" "형태로 되어 있는 것은 정규표현식으로 넣어야 함. 
        나머지는 [
                [[('같은 자리에 올 한 글자 리스트')], 
                ['A', 'B', 'C', 'D'], 
                [], 
                []
                ]
                형식
"""

# 숫자
y = [str(i) for i in range(10)]
d = [str(i) for i in range(10)]

# 무시할 파일 
file_to_ignore_reg =[
        [['위'], ['임']],
        [['참'], ['고'], ['자'], ['료']],
        [['위'], ['임'], ['장']],
        [['첨'], ['부']],
        [['보'], ['정'], ['권'], ['고']],
        [['수'], ['행'], ['자'],],
        [['집'], ['행'], ['정'],['지']],        
] 

# 증거로 분류할 파일 
file_evid_reg = [
        [['갑','을'], d], 
        [['소'], ['갑','을'], d],
]

# 문장을 끊는 기준
split_reg = r'(다\.)|(까\.)|(\)\.)|\!|\?|(\]\.)'

# 준비서면 내용에서 날짜인지 여부 기준
year_reg = r'(\d{4}(?=\.))|(\d{4}(?=년))|(\d{4}(?=-))'
month_reg = r'월|\.|-'

# 준비서면 내용에서 증거인지 판단할 근거 
evid_reg = [
        [['갑', '을'], [' '], ['제'], y, y, y],
        [['갑', '을'], [' '], ['제'], y, y],
        [['갑', '을'], [' '], ['제'], y],
        [['갑', '을'], [' '], y, y, y],
        [['갑', '을'], [' '], y, y],
        [['갑', '을'], [' '], y],
        [['갑', '을'], ['제'], y, y, y],
        [['갑', '을'], ['제'], y, y],
        [['갑', '을'], ['제'], y],
        [['갑', '을'], y, y, y],
        [['갑', '을'], y, y],
        [['갑', '을'], y],
        [['갑', '을'], ['가','나','다'], [' '], ['제'], y, y, y],
        [['갑', '을'], ['가','나','다'], [' '], ['제'], y, y],
        [['갑', '을'], ['가','나','다'], [' '], ['제'], y],
        [['갑', '을'], ['가','나','다'], [' '], y, y, y],
        [['갑', '을'], ['가','나','다'], [' '], y, y],
        [['갑', '을'], ['가','나','다'], [' '], y],
        [['갑', '을'], ['가','나','다'], ['제'], y, y, y],
        [['갑', '을'], ['가','나','다'], ['제'], y, y],
        [['갑', '을'], ['가','나','다'], ['제'], y],
        [['갑', '을'], ['가','나','다'], y, y, y],
        [['갑', '을'], ['가','나','다'], y, y],
        [['갑', '을'], ['가','나','다'], y],

        ]

# 무시할 문장 
useless_token = ["<제정", "<개정", "<신설" "대법원", "서울고", "서울중", \
        "입증방", "입 증", "소 장", "준비서", "준 비", "답변서", "답 변"]

ignore_date_3_chars = ['법 (', '령 (', '칙 (', '례 ('] # 글자 3개 앞부터, 가령 "법 (1997. 3. 13. 개정)" 이면 1997. 3. 13. 앞에 "법 (" 세 글자니까 무시함
ignore_date_2_chars = ['법(', '법원', '령(', '칙(', '례('] # 글자 2개 앞부터,
ignore_date_w_space = ['법원', '개정', '제정', '판소', ] # 글자 3개 앞부터 2개 앞까지