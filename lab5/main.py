import streamlit as st
import pandas as pd
import glob
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path, 'lab5', 'data')
    files = glob.glob(os.path.join(path, "*.csv"))
    
    if not files:
        st.error(f"Файли не знайдені")
        return pd.DataFrame()
    
    all_data = []
    replace_map = {
        1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21,
        11: 9, 12: 13, 13: 14, 14: 15, 15: 16, 16: 25, 17: 17, 18: 18, 19: 6,
        20: 1, 21: 2, 22: 7, 23: 5, 24: 10, 25: 11
    }
    
    for file in files:
        try:
            file_name = os.path.basename(file)
            orig_id = int(file_name.split('_')[2])
            df_temp = pd.read_csv(file, header=1, names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
            
            df_temp['Year'] = df_temp['Year'].astype(str).str.replace(r'<[^>]*>', '', regex=True).str.strip()
            df_temp = df_temp[df_temp['Year'].str.isnumeric()] 
            df_temp['Year'] = df_temp['Year'].astype(int)
            
            df_temp['Area'] = orig_id
            df_temp['Area'] = df_temp['Area'].replace(replace_map)
            all_data.append(df_temp)
        except Exception as e:
            continue
            
    if not all_data:
        return pd.DataFrame()
        
    full_df = pd.concat(all_data, ignore_index=True)
    return full_df[full_df['VHI'] != -1]

st.set_page_config(layout="wide")
df = load_data()

area_names = {
    1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська",
    6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська", 9: "Київська", 10: "Кіровоградська",
    11: "Луганська", 12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська",
    16: "Рівненська", 17: "Сумська", 18: "Тернопільська", 19: "Харківська", 20: "Херсонська",
    21: "Хмельницька", 22: "Черкаська", 23: "Чернівецька", 24: "Чернігівська", 25: "м. Київ"
}

col1, col2 = st.columns([1, 3])

with col1:
    st.header("Фільтри")
    
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0

    def reset_filters():
        st.session_state.reset_counter += 1

    index_choice = st.selectbox("Оберіть часовий ряд", ["VCI", "TCI", "VHI"], key=f"index_{st.session_state.reset_counter}")
    
    region_choice = st.selectbox("Оберіть область", 
                                 options=list(area_names.keys()), 
                                 format_func=lambda x: area_names[x],
                                 key=f"region_{st.session_state.reset_counter}")
    
    week_range = st.slider("Інтервал тижнів", 1, 52, (1, 52), key=f"weeks_{st.session_state.reset_counter}")
    
    year_range = st.slider("Інтервал років", 
                           int(df['Year'].min()), int(df['Year'].max()), 
                           (int(df['Year'].min()), int(df['Year'].max())), 
                           key=f"years_{st.session_state.reset_counter}")
    
    st.button("Скинути фільтри", on_click=reset_filters)
    
    st.subheader("Сортування")
    sort_asc = st.checkbox("За зростанням", key=f"asc_{st.session_state.reset_counter}")
    sort_desc = st.checkbox("За спаданням", key=f"desc_{st.session_state.reset_counter}")

filtered_df = df[(df['Area'] == region_choice) & 
                 (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
                 (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])]

if sort_asc and not sort_desc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=True)
elif sort_desc and not sort_asc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=False)
elif sort_asc and sort_desc:
    st.sidebar.warning("Оберіть лише один тип сортування")

with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння областей"])
    
    with tab1:
        st.dataframe(filtered_df)
        
    with tab2:
        st.line_chart(filtered_df.set_index('Year')[index_choice])
        
    with tab3:
        comp_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
                     (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])]
        pivot_df = comp_df.pivot_table(index='Year', columns='Area', values=index_choice, aggfunc='mean')
        pivot_df.columns = [area_names.get(c, c) for c in pivot_df.columns]
        st.line_chart(pivot_df)