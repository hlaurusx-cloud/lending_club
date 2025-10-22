import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

# Streamlit 페이지 설정
st.set_page_config(layout="wide", page_title="지능형 신용 평가 모형")

# 로드될 데이터프레임의 목표 변수 컬럼명 (실제 데이터에 맞게 수정 필수)
TARGET_COLUMN = 'loan_status_is_bad' 

# =================================================================================
# 1. 모델 실행 및 평가 로직 함수 (Top-Level Function)
# =================================================================================
@st.cache_data
def run_model_analysis(data, C_param):
    st.text("데이터 분할 및 모델 훈련 중...")

    # 경고: 이 코드는 업로드된 데이터가 이미 전처리(인코딩/스케일링) 완료되었다고 가정합니다.
    # X, Y 분리 및 결측치 처리
    X = data.drop(TARGET_COLUMN, axis=1, errors='ignore').fillna(0)
    Y = data[TARGET_COLUMN]

    # 훈련/테스트 데이터 분할 (80:20)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y
    )

    # 로지스틱 회귀 모델 학습
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

# =================================================================================
# 2. 결과 시각화 및 출력 함수들 (Top-Level Functions)
# =================================================================================
def display_metrics(acc, prec, rec):
    st.header("✅ 최종 모형 평가 지표")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("정확도 (Accuracy)", f"{acc:.4f}")
    col2.metric("정밀도 (Precision)", f"{prec:.4f}")
    col3.metric("재현율 (Recall)", f"{rec:.4f}")
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
    
    coefficients = model.coef_[0]
    coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})
    
    coef_df['Abs_Coefficient'] = np.abs(coef_df['Coefficient'])
    coef_df = coef_df.sort_values(by='Abs_Coefficient', ascending=False)
    
    st.dataframe(coef_df[['Feature', 'Coefficient']].head(10).style.format({'Coefficient': "{:.4f}"}))
    st.caption("계수의 절댓값이 클수록 예측에 미치는 영향이 큽니다. 양수 계수는 부실 가능성 증가를 의미합니다.")


# =================================================================================
# 3. 메인 Streamlit 함수 (Top-Level Function)
# =================================================================================
def main():
    st.title("💳 지능형 신용 평가 모형 (로지스틱 회귀)")
    st.markdown("본 페이지는 **Lending Club** 데이터를 이용해 구축된 로지스틱 회귀 모형의 분석 결과 및 성능을 시각화합니다.")
    st.markdown("---")

    # --- 사이드바 (입력 변수) ---
    st.sidebar.header("⚙️ 분석 설정 및 데이터 로드")
    
    uploaded_file = st.sidebar.file_uploader("균형 데이터셋 CSV 파일 업로드", type=["csv"])
    model_choice = st.sidebar.selectbox(
        "사용할 예측 모형", 
        ('로지스틱 회귀 (Logistic Regression)', '신경망 (Neural Network) - 예정')
    )
    C_param = st.sidebar.slider("로지스틱 회귀: 규제 강도 C", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    
    run_button = st.sidebar.button('🚀 모형 학습 및 평가 시작')

    
    # --- 메인 콘텐츠 (결과 출력) ---
    if uploaded_file is not None:
        try:
            # 파일 로드 (인코딩 문제는 try-except로 처리)
            try:
                data = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                data = pd.read_csv(uploaded_file, encoding='cp949')

            st.subheader("✅ 데이터 현황 (건전 15,000 / 부실 15,000)")
            st.dataframe(data.head())
            st.write(f"총 샘플링된 데이터 수: {len(data)} 행")
            st.markdown("---")
            
            # 실행 버튼 클릭 시 모델 분석 시작
            if run_button:
                # 훈련 및 평가 함수 호출
                with st.spinner('모델 훈련 및 평가 중...'):
                    acc, prec, rec, cm, model = run_model_analysis(data, C_param)

                # 결과 출력
                display_metrics(acc, prec, rec)
                display_confusion_matrix(cm)
                display_model_interpretation(model, data.drop(TARGET_COLUMN, axis=1, errors='ignore').columns)

        except KeyError:
            st.error(f"오류: 데이터에 목표 변수 '{TARGET_COLUMN}' 컬럼이 없습니다. 컬럼명을 확인해주세요.")
        except Exception as e:
            st.error(f"데이터 처리 중 예상치 못한 오류 발생: {e}")
            st.info("파일이 One-Hot Encoding 및 필요한 전처리된 상태인지 확인해주세요.")
            
    else:
        st.info("👈 분석을 시작하려면 CSV 파일을 사이드바에 업로드하고 '모형 학습 시작' 버튼을 눌러주세요.")


# =================================================================================
# 4. 스크립트 실행 시작 지점 (Top-Level Block)
# =================================================================================
if __name__ == '__main__':
    main()
