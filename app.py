import random
import pandas as pd
import streamlit as st

# 2. 리스트 선언: 고등학교 목록, 고등학교 우선순위 가중치 리스트 정의
ALL_HIGHSCHOOLS = [
    "세종과학고",
    "한성과학고",
    "경기북과학고",
    "하나고",
    "하남고",
    "미사고",
    "신장고",
    "미사강변고",
    "남한고",
    "하남경영고",
]
WEIGHTS = [30, 25, 20, 15, 10]  # 1순위(30%) ~ 5순위(10%) 확률


# 중학교 내신별 가능한 고등학교를 if-elif-else로 구성
def get_available_schools(grade):
    if grade >= 200:
        return ALL_HIGHSCHOOLS[0:]
    elif grade >= 199.5:
        return ALL_HIGHSCHOOLS[1:]
    elif grade >= 198:
        return ALL_HIGHSCHOOLS[2:]
    elif grade >= 195:
        return ALL_HIGHSCHOOLS[3:]
    elif grade >= 190:
        return ALL_HIGHSCHOOLS[4:]
    elif grade >= 180:
        return ALL_HIGHSCHOOLS[5:]
    elif grade >= 170:
        return ALL_HIGHSCHOOLS[6:]
    elif grade >= 160:
        return ALL_HIGHSCHOOLS[7:]
    elif grade >= 140:
        return ALL_HIGHSCHOOLS[8:]
    elif grade >= 100:
        return ALL_HIGHSCHOOLS[9:]
    else:
        return []


# 성적과 원하는 고등학교 1~5순위를 입력받아 뽑을 고등학교 5개 선정
def check_rist(grade, wanted_hughschool):
    available = get_available_schools(grade)
    selected_5 = []
    for school in wanted_hughschool:
        if school in available and len(selected_5) < 5:
            selected_5.append(school)
    return selected_5


# 4. 버튼 클릭 시 실행되는 추첨 함수
def pick_highschool(grade, available_schools, wanted_highschool):
    # 지원 가능한 학교가 5개 이상일 때는 중복 선택 방지
    if len(available_schools) >= 5 and len(set(wanted_highschool)) < 5:
        st.error(
            "⚠️ 1순위부터 5순위까지 중복되지 않게 서로 다른 고등학교 5개를 선택해주세요."
        )
        return

    # check_rist 함수를 통해 최종 후보 5개 학교 확정
    candidates = check_rist(grade, wanted_highschool)

    # 확률에 따라 최종 고등학교 1개 추첨
    picked_school = random.choices(candidates, weights=WEIGHTS, k=1)[0]

    # 결과 출력 화면(예시): 중학교 내신 | 추첨된 고등학교
    result_df = pd.DataFrame(
        [{"중학교 내신": f"{grade:.2f}", "추첨된 고등학교": picked_school}]
    )

    st.subheader("🎉 최종 추첨 결과")
    st.dataframe(result_df, hide_index=True, use_container_width=True)


# --- 1. 시작: 사용자가 앱에 접속 ---
st.title("🏫 고등학교 진학 확률 추첨 시스템")

# 3. 입력받기: grade로 성적 입력
grade = st.number_input(
    "중학교 내신 성적을 입력하세요 (0 ~ 200점, 소수점 입력 가능):",
    min_value=0.0,
    max_value=200.0,
    value=192.42,
    step=0.01,
    format="%.2f",
)

# 5. 조건 판단: 성적이 100 미만이라면 경고 메시지 출력
if grade < 100:
    st.warning("가능한 학교가 없습니다, 다른 지역에서 찾아가세요")
else:
    available_schools = get_available_schools(grade)

    # 6. 반복 출력: for 구문을 이용해 가능한 고등학교 리스트를 테이블 생성용 데이터로 변환
    school_table_data = []
    for idx, school in enumerate(available_schools, start=1):
        school_table_data.append({"번호": idx, "지원 가능한 고등학교": school})

    st.subheader("📋 지원 가능한 고등학교 선택목록")
    st.dataframe(
        pd.DataFrame(school_table_data),
        hide_index=True,
        use_container_width=True,
    )

    if len(available_schools) < 5:
        st.caption(
            "※ 지원 가능한 학교가 5개 미만인 경우, 원하는 학교를 중복 배치하여 1~5순위를 채울 수 있습니다."
        )

    # 3. 입력받기: wanted_highschool로 성적에서 가능한 고등학교들 중 5개 입력받음
    st.subheader("🎯 희망 고등학교 우선순위 입력 (1~5순위)")
    wanted_highschool = []
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            choice = st.selectbox(
                f"{i+1}순위 ({WEIGHTS[i]}%)",
                options=available_schools,
                index=min(i, len(available_schools) - 1),
                key=f"rank_{i}",
            )
            wanted_highschool.append(choice)

    # 4. 버튼 클릭 시 'pick_highschool()' 함수 실행
    if st.button("🎲 최종 고등학교 추첨하기", use_container_width=True):
        pick_highschool(grade, available_schools, wanted_highschool)
