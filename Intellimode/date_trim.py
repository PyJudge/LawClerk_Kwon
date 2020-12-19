#%%
import pandas as pd

def delete_duplicate(table):
    date_dict = dict()
    for row in table : 
        if row[0] not in date_dict.keys():
            date_dict[row[0]] = []
        rest_row_ = row[1:] # 나머지 데이터 
        date_dict[row[0]].append(rest_row_) # nested list 

    result = []
    for date in date_dict.keys():
        sents_ = date_dict[date]
        for i, sent_1 in enumerate(sents_): 
            for j in range(i+1, len(sents_) ): 
                sent_2 = sents_[j]
                s1_ = sent_1[3].replace(" ", "")
                s2_ = sent_2[3].replace(" ", "")
                if s1_ == s2_:
                    if sents_[j][3][0:2] != "중복":
                        sents_[j][3] = "중복: {}-{}면".format(*sent_1[1:3]) # 뒷 문장을 중복으로 날림
                    else : 
                        sents_[j][3] +=  ", {}-{}면".format(*sent_1[1:3])
        result.append([[date, *sent_data] for sent_data in sents_])

    # 3중 괄호 > 2중 괄호
    res = []
    for rrr in result:
        for rr in rrr:
            res.append(rr)
    return res


#%%
# CODE FOR TESTING, test data with some duplicate
table = """20180300	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	126	500-706 광주 광역시 북구 첨단과기로 333 GJTP 사업화1동 201호TEL(062)FAX(062)품 목NO품 명사 양수량단위단가(원)금액(원)비고1SP44-33-195LIB 21700380대2,580,000 980,400,000 * 배터리설치 썬그린에너지. 상차운반도착 인셀.공급가액부가세총 합 계IC-QP-701-01B(1)견 적 서 견 적 서 번 호 : IC - ES - 1803-100 인 셀 ㈜ INCELL CO., LTD.2018-03-10썬그린에너지 귀하 대 표 이 사 정 창 권 973-5993~4* 배터리실 온도 23±5℃, 습도 50%±10정도아래와 같이 견적합니다.
20180300	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	452	500-706 광주 광역시 북구 첨단과기로 333 GJTP 사업화1동 201호TEL(062)FAX(062)품 목NO품 명사 양수량단위단가(원)금액(원)비고1SP44-33-195LIB 21700380대2,580,000 980,400,000 * 배터리설치 썬그린에너지. 상차운반도착 인셀.공급가액부가세총 합 계IC-QP-701-01B(1)견 적 서 견 적 서 번 호 : IC - ES - 1803-100 인 셀 ㈜ INCELL CO., LTD.2018-03-10썬그린에너지 귀하 대 표 이 사 정 창 권 973-5993~4* 배터리실 온도 23±5℃, 습도 50%±10정도아래와 같이 견적합니다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	23	(단, 배터리 수급이 원활하지 않을 경우 설치 기간이 연장될 수 있다) 4. ESS 납품 및 설치공사 세부내역 품명제조사사양단위수량비교 삼성 셀 리튬이온배터리삼성SDI 인셀(주) 3,114kWh식1공인기관의 시험성적서품질보증서 제출 2018. 5. 이후 정식 출고된 정품제품, 출고 증명서 제출 PCS㈜피앤이솔루션1,000kWh식1공인기관의 시험성적서품질보증서 제출 EMS㈜C&GRIDEMS H/W, S/W식 1 정품S/W EPC썬그린에너지(주)건축, 전기공사식1ESS설치 마감 5. 계약금액 및 대금지급 방법 구분금액합계금액(부가세포함)비고계약총액1,50,000,000원1,650,000,000원배터리, PCS, 설치, 대관업무 제비용계약금10%150,000,000원165,000,000원계약이행보증증권발행 3일 이내 선급금 % - 원 -원금융대출 금액의 잔금 8. 품질기준 (무상A/S기간) 1) 에너지저장장치 설치공사 완료(준공) 후 하자가 발생한 경우 “갑”은 “을”에게 그 내용을 즉시 통보하여야 하며, “갑”의 통보를 받은 “을”은 즉시 이를 이행 완료하여야 한다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	24	나. 에너지 저장장치의 품명을 특정함 (계약의 가장 중요한 부분) 이 사건 도급계약서 표지 부분 및 제12조(특약사항) 제5항에서 규정 하였듯, 원고와 피고1. 회사는 이 사건 도급공사에 있어서 에너지 저장장치의 종류로, ‘삼성 SDI 리튬이온셀 21700(품질보증서 제출 2018. 5.월 이후 정식 출고된 정품제품)’으로 설치할 것을 계약의 가장 중요한 내용으로 포함 시켰고, 이를 별도 특약사항으로 정하면서까지 확인 하였습니다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	24	5) 설치 제품은 삼성 SDI 리튬이온셀 21700(품질보증서 제출 2018. 5.월 이후 정식 출고된 정품제품)으로 하되, 출고 증명서를 갑에게 제출 하여야 한다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	76	2. 이 사건 도급계약의 변경 가. 배터리용량 증설에 관한 원고와 피고 썬그린에너지㈜의 합의 및 이에 따른 배터리 제품의 교체 1) 원고는 피고 썬그린에너지㈜와 이 사건 도급계약의 체결하고 총 공사대금 1,500,000,000원 중 일부인 금 1,349,999,996원을 지급한 직후, 2018. 5.경 피고
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	83	- 8 - 라. ESS고압연계 시설공사 설계도면 및 건축설계도면에 따른 시공 1) 원고는 피고 썬그린에너지㈜가 설계도면과 다르게 변경설치를 하였다고 주장하나, 앞서 살펴본 바와 같이 원고와 피고 썬그린에너지㈜는 설치공사 이전인 2018. 5.경 배터리용량을 증설하여 ㈜인셀 삼성SDI 18650모델로 설치하고, 500kwh PCS 2개를 설치하기로 합의하였으며,이후 피고 썬그린에너지㈜는 ESS고압연계 시설공사의 설계도면 및 건축설계도면에 따라 ㈜인셀 삼성SDI 18650배터리를 설치하고 500kwh PCS 2개를 설치하였습니다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	98	5) 설치 제품은 삼성 SDI 리튬이온셀 21700(품질보증서 제출 2018. 5.월 이후 정식 출고된 정품제품)으로 하되, 출고 증명서를 갑에게 제출 하여야 한다.
20180500	005	/Users/wonmyeongkwon/Downloads/전주지방법원_2019가합3393	127	5) 설치 제품은 삼성 SDI 리튬이온셀 21700(품질보증서 제출 2018. 5.월 이후 정식 출고된 정품제품)으로 하되, 출고 증명서를 갑에게 제출 하여야 한다."""

table = table.replace("\n", "\t")
result = []

row = []
for i, cell in enumerate(table.split('\t')):
    row.append(cell)
    if i % 5 == 4:
        result.append(row)
        row = []

table = result
#%% Prototype code

date_dict = dict()
for row in table : 
    if row[0] not in date_dict.keys():
        date_dict[row[0]] = []
    rest_row_ = row[1:5] # 나머지 데이터 
    date_dict[row[0]].append(rest_row_) # nested list 

result = []
for date in date_dict.keys():
    sents_ = date_dict[date]
    for i, sent_1 in enumerate(sents_): 
        for j in range(i+1, len(sents_) ): 
            sent_2 = sents_[j]
            s1_ = sent_1[3].replace(" ", "")
            s2_ = sent_2[3].replace(" ", "")
            if s1_ == s2_:
                if sents_[j][3][0:2] != "중복":
                    sents_[j][3] = "중복: {}-{}면".format(*sent_1[1:3]) # 뒷 문장을 중복으로 날림
                else : 
                    sents_[j][3] +=  ", {}-{}면".format(*sent_1[1:3])
    result.append([[date, *sent_data] for sent_data in sents_])

# 3중 괄호 > 2중 괄호
res = []
for rrr in result:
    for rr in rrr:
        res.append(rr)
res
# %%
# make them to a func 

# %%
