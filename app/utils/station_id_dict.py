id_list = [95,  96,  97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107,
           108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
           121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
           134, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
           213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225,
           226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
           239, 240, 241, 242, 243, 302, 303, 304, 305, 306, 307, 308, 309,
           310, 311, 312, 313, 314, 315, 316, 317, 402, 403, 404, 405, 406,
           407, 408, 409, 410, 411, 412, 413, 414]

name_list = ['다대포해수욕장', '다대포항', '낫개', '신장림', '장림', '동매', '신평', '하단', '당리', '사하', '괴정', '대티', '서대신', '동대신', '토성', '자갈치', '남포', '중앙', '부산역', '초량', '부산진', '좌천', '범일', '범내골', '1서면', '부전', '양정', '시청', '1연산', '교대', '1동래', '명륜', '온천장', '부산대', '장전', '구서', '두실', '남산', '범어사', '노포', '장산', '중동', '해운대', '동백', '벡스코', '센텀시티', '민락', '수영', '광안', '금련산', '남천', '경성대부경대', '대연', '못골', '지게골', '문현',
             '국제금융센터', '전포', '2서면', '부암', '가야', '동의대', '개금', '냉정', '주례', '감전', '사상', '덕포', '모덕', '모라', '구남', '구명', '2덕천', '수정', '화명', '율리', '동원', '금곡', '호포', '증산', '부산대양산', '남양산', '양산', '망미', '배산', '물만골', '3연산', '거제', '종합운동장', '사직', '미남', '만덕', '남산정', '숙등', '3덕천', '구포', '강서구청', '체육공원', '대저', '4동래', '수안', '낙민', '충렬사', '명장', '서동', '금사', '반여농산물', '석대', '영산대', '윗반송', '고촌', '안평']
station_id_dict = {}

for key, value in zip(id_list, name_list):
    station_id_dict[key] = value
