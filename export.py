import os
from db import get_logs_by_user_date
from db_meta import get_meta_for_user

def export_markdown(username, date, output_dir="log"):
    logs = get_logs_by_user_date(username, date)
    location, weather, temperature = get_meta_for_user(username, date)

    lines = []
    lines.append(f"# 🗓️ {date} 工程日志\n")
    lines.append(f"- 用户：{username}")
    lines.append(f"- 地点：{location or '-'}")
    lines.append(f"- 天气：{weather or '-'}，{temperature or '-'}℃\n")
    lines.append("---\n")
    lines.append("## ⏱ 日志记录\n")

    if not logs:
        lines.append("_暂无记录_\n")
    else:
        for start, end, content, project in logs:
            lines.append(f"- {start} - {end}（{project}）：{content}")

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"log-{date}-{username}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filepath