# 배포전 구현사항
csv를 파싱해서 pickle로 만드는 로직 함수화해서 어플리케이션 실행전에 실행시킨다.
.env 파일 관리한다.
# 1차 구현 기능
1. 자연어로 질의해서 필터 설정하기
- 오늘 프로토타입 완성하기
2. 자연어로 데이터프레임에 대해 질의하고, 모델이 응답하기
- 오늘 프로토타입 완성하기

## 2차 구현 기능
3. 자연어로 시각화 명령하기
- 시각화는 나중에
4. 예시로 보여줄 유용한 통계 인사이트 발굴해서 삽입하기.

5. 필터시 활용할 스페셜 필터 구현하기
- 프롬프트 엔지니어링으로 모델이 처리할 수 있게 해본다.
- Top10s
- Lowests
- 테마별
- 설날, 명절, 주말, 연휴, 여름, 봄, 가을, 겨울
- 크리스마스, 불꽃놀이, 

6. 연산을 줄이기 위해 리샘플링된 데이터프레임을 따로 추출해서 저장해놓기
- freq를 반영해서 freq별로 따로 데이터프레임을 미리 추출해놓고, 활용해보기
- 일단위
- 월단위
- 분기단위
- 연단위