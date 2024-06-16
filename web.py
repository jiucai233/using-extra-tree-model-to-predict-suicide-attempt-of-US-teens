import streamlit as st
import gdown
import joblib
import os
import time
from pathlib import Path

# Google Drive 文件的共享链接
file_id = '1VlAbUQIRaG_3MvFD1Jp5bBul_9KPa6wV'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'model.pkl'

# 使用 st.cache_resource 缓存模型加载
@st.cache_resource
def download_and_load_model(url, output):
    # 下载文件
    if not os.path.exists(output):
        gdown.download(url, output, quiet=True)
    
    # 确保文件已完整下载
    if os.path.exists(output):
        try:
            model = joblib.load(output)
            return model
        except Exception as e:
            st.error(f"Failed to load the model: {e}")
            return None
    else:
        st.error("Failed to download the file")
        return None

# 加载模型
model = download_and_load_model(url, output)

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

footerText = """
<style>
#MainMenu {
visibility:hidden ;
}

footer {
visibility : hidden ;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
"""

st.markdown(str(footerText), unsafe_allow_html=True)

def prediction(X_test):
    if model:
        try:
            result = model.predict_proba([X_test])
            return result[0][1]
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None
    else:
        return None

def set_bmi(BMI):
    if BMI < 18.5:
        return 1
    elif BMI < 23:
        return 2
    elif BMI < 25:
        return 3
    else:
        return 4

def input_values():
    Age = st.radio('Age(year)', (14, 15, 16, 17, 18), horizontal=True)
    grade = st.radio('Grade(school)', (9, 10, 11, 12), horizontal=True)
    sex = st.radio('Sex', ('Male', 'Female'), horizontal=True)
    SEXDict = {'Male': 1, 'Female': 2}
    sex = SEXDict[sex]

    height = st.number_input('Height (cm)', min_value=0, max_value=1000, value=130)
    weight = st.number_input('Weight (kg)', min_value=0, max_value=1000, value=50)
    bmiv = weight / ((height / 100) ** 2)
    bmi_2 = set_bmi(bmiv)
    bmiDict = {1: 'Underweight', 2: 'Normal', 3: 'Overweight', 4: 'Obese'}
    st.write('BMI: ', bmiDict[bmi_2], round(bmiv, 2))

    smoking = st.radio('Smoking status', ('No', 'Yes'), horizontal=True)
    smokingDict = {'No': 0, 'Yes': 1}
    smoking = smokingDict[smoking]

    alcoholic_consumption = st.radio('Alcohol consumption Status', ('No', 'Yes'), horizontal=True)
    alcoholic_consumptionDict = {'No': 0, 'Yes': 1}
    alcoholic_consumption = alcoholic_consumptionDict[alcoholic_consumption]

    stress = st.radio('Stress status', ('Low to moderate', 'High to severe'), horizontal=True)
    stressDict = {'Low to moderate': 1, 'High to severe': 2}
    stress = stressDict[stress]

    depression = st.radio('Depression status', ('Low to moderate', 'High to severe'), horizontal=True)
    depressionDict = {'Low to moderate': 1, 'High to severe': 2}
    depression = depressionDict[depression]

    suicide_thinking = st.radio('Suicidal thought', ('Low to moderate', 'High to severe'), horizontal=True)
    suicide_thinkingDict = {'Low to moderate': 0, 'High to severe': 1}
    suicide_thinking = suicide_thinkingDict[suicide_thinking]

    use_drug = st.radio('Drug addiction', ('Never', 'Have been used'), horizontal=True)
    use_drugDict = {'Never': 0, 'Have been used': 1}
    use_drug = use_drugDict[use_drug]

    race_options = ('white', 'black', 'asian', 'hispanic', 'other')
    selected_races = st.multiselect('Please choose your race (you can have multiple choices if you are mixed blooded)', race_options)

    white = 1 if 'white' in selected_races else 0
    black = 1 if 'black' in selected_races else 0
    asian = 1 if 'asian' in selected_races else 0
    hispanic = 1 if 'hispanic' in selected_races else 0
    other = 1 if 'other' in selected_races else 0

    X_test = [Age, grade, sex, bmi_2, smoking, alcoholic_consumption, stress, depression, suicide_thinking, use_drug, white, black, asian, hispanic, other]

    result = prediction(X_test)

    return result

def main():
    result = input_values()

    with st.sidebar:
        st.markdown(f'# Probability for suicidal attempt')

        if result is not None:
            if result * 100 < 50:
                danger_level = 'Barely'
                st.markdown(f'# {result * 100:.2f} %')
            elif result * 100 < 75:
                danger_level = 'Moderately'
                st.markdown(f'# {result * 100:.2f} %')
            elif result * 100 < 90:
                danger_level = 'Considerably'
                st.markdown(f'# {result * 100:.2f} %')
            else:
                danger_level = 'Extremely'
                st.markdown(f'# {result * 100:.2f} %')

            st.markdown(f'## {danger_level}')
        else:
            st.markdown(f'# Prediction failed')

    now = time.localtime()
    print(time.strftime('%Y-%m-%d %H:%M:%S', now))

if __name__ == '__main__':
    main()
