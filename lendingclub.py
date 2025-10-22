import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit 페이지 설정
st.set_page_config(layout="wide", page_title="지능형 신용 평가 모형")

# 로드될 데이터프레임과 컬럼명 (실제 데이터에 맞게 수정 필요)
TARGET_COLUMN = 'loan_status_is_bad'  # 부실 여부를 나타내는 최종 이진 컬럼명 (0 또는 1)
def main():
    st.title("💳 지능형 신용 평가 모형 (로지스틱 회귀)")
    st.markdown("본 페이지는 Lending Club 데이터를 이용해 구축된 **로지스틱 회귀 모형**의 분석 결과 및 성능을 시각화합니다.")
    st.markdown("---")

    # =================================================================================
    # 1. 사이드바 (입력 변수)
    # =================================================================================
    st.sidebar.header("⚙️ 분석 설정 및 데이터 로드")
    
    # 1-1. 데이터 업로드 위젯
    uploaded_file = st.sidebar.file_uploader("균형 데이터셋 CSV 파일 업로드", type=["csv"])
    
    # 1-2. 모형 선택 위젯 (향후 신경망 확장을 대비)
    model_choice = st.sidebar.selectbox(
        "사용할 예측 모형", 
        ('로지스틱 회귀 (Logistic Regression)', '신경망 (Neural Network) - 예정')
    )
    
    # 1-3. 로지스틱 회귀 하이퍼파라미터 (C 값)
    C_param = st.sidebar.slider("로지스틱 회귀: 규제 강도 C", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    # 1-4. 실행 버튼
    run_button = st.sidebar.button('🚀 모형 학습 및 평가 시작')

    
    # =================================================================================
    # 2. 메인 콘텐츠 (결과 출력)
    # =================================================================================

    if uploaded_file is not None:
        try:
            # 파일 로드 및 전처리 (실제 데이터에 맞게 인코딩 수정 필요)
            data = pd.read_csv(uploaded_file, encoding='utf-8')
            
            st.subheader("✅ 데이터 현황 (건전 15,000 / 부실 15,000)")
            st.dataframe(data.head())
            st.write(f"총 샘플링된 데이터 수: {len(data)} 행")
            st.markdown("---")
            
            if run_button:
                # 데이터 분할 및 모델 학습 로직
                acc, prec, rec, cm, model = run_model_analysis(data, C_param)

                # 2-1. 평가 지표 출력
                display_metrics(acc, prec, rec)
                
                # 2-2. 혼동 행렬 시각화
                display_confusion_matrix(cm)
                
                # 2-3. 모형 해석 (특성 중요도)
                display_model_interpretation(model, data.drop(TARGET_COLUMN, axis=1).columns)

        except Exception as e:
            st.error(f"데이터 처리 중 오류 발생: {e}")
            st.info("파일이 15000/15000 샘플링된 CSV 형식이며, 인코딩이 맞는지 확인해주세요.")
            
    else:
        st.info("👈 분석을 시작하려면 CSV 파일을 사이드바에 업로드하고 '모형 학습 시작' 버튼을 눌러주세요.")
        @st.cache_data  # 데이터프레임과 모형 학습 결과 캐싱
def run_model_analysis(data, C_param):
    # 경고: 이 로직은 동료 학생의 결과에 없는 3대 지표를 계산하는 부분입니다.
    # 특성 선택, 스케일링, 인코딩 로직이 이전에 완료된 '균형 데이터'를 가정합니다.
    
    st.text("데이터 분할 및 모델 훈련 중...")

    # X, Y 분리 (업로드된 데이터가 이미 One-Hot Encoding 된 상태라고 가정)
    X = data.drop(TARGET_COLUMN, axis=1).fillna(0) # 결측치는 임시로 0 처리 (실제 과제에서는 더 복잡한 처리 필요)
    Y = data[TARGET_COLUMN]

    # 훈련/테스트 데이터 분할 (80:20)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

    # 로지스틱 회귀 모델 학습 (C_param 사용)
    model_lr = LogisticRegression(C=C_param, random_state=42, solver='liblinear', max_iter=1000)
    model_lr.fit(X_train, Y_train)

    # 예측 및 평가
    Y_pred = model_lr.predict(X_test)

    cm = confusion_matrix(Y_test, Y_pred)
    acc = accuracy_score(Y_test, Y_pred)
    prec = precision_score(Y_test, Y_pred)
    rec = recall_score(Y_test, Y_pred)

    st.success("모형 학습 및 평가 완료!")
    return acc, prec, rec, cm, model_lr
    def display_metrics(acc, prec, rec):
    st.header("✅ 최종 모형 평가 지표")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("정확도 (Accuracy)", f"{acc:.4f}", help="전체 예측 중 올바른 예측 비율")
    col2.metric("정밀도 (Precision)", f"{prec:.4f}", help="부실 예측 중 실제 부실 비율 (대출 심사 중요 지표)")
    col3.metric("재현율 (Recall)", f"{rec:.4f}", help="실제 부실 고객을 모형이 잡아낸 비율 (리스크 관리 중요 지표)")
    st.markdown("---")

def display_confusion_matrix(cm):
    st.subheader("📊 혼동 행렬 (Confusion Matrix)")
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, 
                xticklabels=['예측 건전 (0)', '예측 부실 (1)'], 
                yticklabels=['실제 건전 (0)', '실제 부실 (1)'],
                cbar=False)
    ax.set_ylabel('실제 값 (True Label)')
    ax.set_xlabel('예측 값 (Predicted Label)')
    
    st.pyplot(fig)
    st.markdown("---")

def display_model_interpretation(model, feature_names):
    st.subheader("🔎 모형 해석: 특성별 영향력 (계수)")
    
    # 계수 추출
    coefficients = model.coef_[0]
    coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})
    
    # 계수 절댓값 기준 정렬 (영향력 큰 순)
    coef_df['Abs_Coefficient'] = np.abs(coef_df['Coefficient'])
    coef_df = coef_df.sort_values(by='Abs_Coefficient', ascending=False)
    
    st.dataframe(coef_df[['Feature', 'Coefficient']].head(10).style.format({'Coefficient': "{:.4f}"}))
    st.caption("계수의 절댓값이 클수록 예측에 미치는 영향이 큽니다.")
    if __name__ == '__main__':
    main()
