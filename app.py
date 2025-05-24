import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import datetime
from db import insert_log, get_logs_by_user_date
from db_projects import get_projects_for_user, add_project_for_user, create_user_projects_table

# 初始化用户项目表
create_user_projects_table()

# --- 登录认证 ---
with open("auth_config.yaml", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"], config["cookie"]["name"], config["cookie"]["key"], config["cookie"]["expiry_days"]
)

name, authentication_status, username = authenticator.login("登录", location="main")

if authentication_status is False:
    st.error("用户名或密码错误")
elif authentication_status is None:
    st.warning("请输入用户名和密码")
elif authentication_status:

    st.title(f"👷‍♂️ LindoAI 日志记录 - {name}")
    authenticator.logout("退出登录", "sidebar")

    st.sidebar.header("🗓 日期选择")
    today = datetime.date.today()
    date = st.sidebar.date_input("选择日期", today)

    st.subheader("➕ 添加日志记录")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        start_time = st.time_input("开始时间", datetime.time(8, 0))
    with col2:
        end_time = st.time_input("结束时间", datetime.time(9, 0))
    with col3:
        user_projects = get_projects_for_user(username)
        selected_project = st.selectbox("选择项目", user_projects)
        new_project = st.text_input("或新建项目名称")
        if st.button("➕ 添加新项目") and new_project:
            add_project_for_user(username, new_project.strip())
            st.success("项目已添加，请重新选择")
            st.experimental_rerun()

    content = st.text_area("内容描述", "")

    if st.button("📥 添加记录"):
        if content.strip() and start_time < end_time and (selected_project or new_project):
            project_used = new_project.strip() if new_project else selected_project
            insert_log(str(date), start_time.strftime("%H:%M"), end_time.strftime("%H:%M"), content.strip(), project_used, username)
            st.success("记录已添加！")
        else:
            st.error("请输入完整内容，且时间段合法")

    st.subheader("📋 今日记录")

    logs = get_logs_by_user_date(username, str(date))
    if not logs:
        st.info("暂无记录")
    else:
        for start, end, content, project in logs:
            st.markdown(f"- 🕒 {start} - {end}（{project}）：{content}")