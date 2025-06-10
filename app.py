import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import datetime
from streamlit.components.v1 import html
from db.db_core import init_db
from db.db_logs import insert_log, get_logs_by_user_date, delete_log
from db.db_projects import (
    create_user_projects_table,
    get_projects_for_user,
    add_project_for_user,
    delete_project_for_user,
)
from db.db_phrases import get_top_phrases_for_user
from db.db_meta import create_meta_table, save_meta, get_meta_for_user
from io import StringIO
def generate_markdown_for_logs(logs, date, username):
    location, recorder, weather, temperature = get_meta_for_user(username, str(date))

    lines = []
    lines.append(f"# 📅 {date} 工程日志")
    lines.append(f"- 记录人：{recorder or username}")
    lines.append(f"- 地点：{location or '-'}")
    lines.append(f"- 天气：{weather or '-'}，{temperature or '-'}℃")
    lines.append("\n---\n\n## ⏱ 日志记录")

    if not logs:
        lines.append("_暂无记录_")
    else:
        for start, end, content, project in logs:
            lines.append(f"- {start} - {end}（{project}）：{content}")

    return "\n".join(lines)



# 初始化数据库
init_db()
create_meta_table()
create_user_projects_table()

# --- 登录认证 ---
with open("auth_config.yaml", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

name, authentication_status, username = authenticator.login("登录", location="main")

if authentication_status is False:
    st.error("用户名或密码错误")
elif authentication_status is None:
    st.warning("请输入用户名和密码")
elif authentication_status:

    st.sidebar.title(f"🦄👷‍♂️ LindoAI 日志记录- {name}")
    authenticator.logout("退出登录", "sidebar")

    # 侧边栏：基础信息
    st.sidebar.header("🗓 日期选择")
    today = datetime.date.today()
    date = st.sidebar.date_input("选择日期", today)

    st.sidebar.markdown("### 📌 基础信息")
    location, weather, temperature = get_meta_for_user(username, str(date))
    new_location = st.sidebar.text_input("地点", value=location)
    new_weather = st.sidebar.selectbox(
        "天气", ["", "晴", "阴", "大雨", "中雨", "小雨", "雪", "多云"],
        index=["", "晴", "阴", "大雨", "中雨", "小雨", "雪", "多云"].index(weather if weather else "")
    )
    new_temp = st.sidebar.text_input("温度 ℃", value=temperature)
    recorder_name = st.sidebar.text_input("记录人", value=username)

    if st.sidebar.button("💾 保存基础信息"):
        save_meta(recorder_name, str(date), new_location, new_weather, new_temp)
        st.sidebar.success("已保存！")

 
    left_col, right_col = st.columns([1, 3])

    with left_col:
        start_time = st.time_input("开始时间", datetime.time(8, 0))
        end_time = st.time_input("结束时间", datetime.time(9, 0))
        user_projects = get_projects_for_user(username)
        selected_project = st.selectbox("选择项目", user_projects)

        with st.expander("📁 我的项目管理", expanded=False):
            if user_projects:
                proj_to_delete = st.selectbox("选择要删除的项目", user_projects, key="delete-project")
                if st.button("🗑 删除该项目"):
                    delete_project_for_user(username, proj_to_delete)
                    st.success(f"已删除项目：{proj_to_delete}")
                    st.rerun()
            else:
                st.info("你还没有项目")
        
        new_project = st.text_input("或新建项目名称")
        if st.button("➕ 添加新项目"):
            if new_project.strip():
                add_project_for_user(username, new_project.strip())
                st.success("项目已添加，请重新选择")
                st.rerun()

    with right_col:
    
    
        st.subheader("📋 今日记录")

        logs = get_logs_by_user_date(username, str(date))
        # ⬇️ 生成 Markdown 内容并提供下载
        md_text = generate_markdown_for_logs(logs, str(date), username)
        md_filename = f"log-{date}.md"

        st.download_button(
            label="📄 导出 Markdown",
            data=md_text,
            file_name=md_filename,
            mime="text/markdown"
        )

        if not logs:
            st.info("暂无记录")
        else:
            MAX_VISIBLE = 4

            for i, (start, end, content, project) in enumerate(logs[:MAX_VISIBLE]):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div style='
                            padding: 10px 14px;
                            margin-bottom: 8px;
                            background-color: #1e1e1e;
                            color: #f8f9fa;
                            font-size: 14px;
                            font-family: "Segoe UI", sans-serif;
                            border-radius: 6px;
                            border: 1px solid #333;
                        '>
                            🕒 <strong>{start} - {end}</strong> （{project}）：{content}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col2:
                    if st.button("🗑", key=f"del-log-{i}"):
                        delete_log(username, str(date), start, end, project, content)
                        st.rerun()

            if len(logs) > MAX_VISIBLE:
                with st.expander("📂 查看更多记录"):
                    for i, (start, end, content, project) in enumerate(logs[MAX_VISIBLE:], start=MAX_VISIBLE):
                        col1, col2 = st.columns([10, 1])
                        with col1:
                            st.markdown(
                                f"""
                                <div style='
                                    padding: 10px 14px;
                                    margin-bottom: 8px;
                                    background-color: #1e1e1e;
                                    color: #f8f9fa;
                                    font-size: 14px;
                                    font-family: "Segoe UI", sans-serif;
                                    border-radius: 6px;
                                    border: 1px solid #333;
                                '>
                                    🕒 <strong>{start} - {end}</strong> （{project}）：{content}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        with col2:
                            if st.button("🗑", key=f"del-log-{i}"):
                                delete_log(username, str(date), start, end, project, content)
                                st.rerun()

            # 内容输入框 + 添加按钮
        common_phrases = get_top_phrases_for_user(username)
        if common_phrases:
            with st.expander("💡 常用内容快速选择"):
                cols = st.columns(len(common_phrases))
                for i, phrase in enumerate(common_phrases):
                    with cols[i]:
                        if st.button(phrase, key=f"phrase-{i}"):
                            st.session_state["content_input"] = phrase

        col_content, col_btn = st.columns([5, 1])

        with col_content:
            content = st.text_area("内容描述", value=st.session_state.get("content_input", ""))

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)  # 空行让按钮垂直居中
            if st.button("📥 添加记录"):
                project_used = new_project.strip() if new_project else selected_project
                if content.strip() and start_time < end_time and project_used:
                    insert_log(str(date), start_time.strftime("%H:%M"), end_time.strftime("%H:%M"),
                            content.strip(), project_used, username)
                    st.success("记录已添加！")
                    st.rerun()
                else:
                    st.error("请输入完整内容，且时间段合法")



