import os
import glob
import datetime
import io
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-3-pro-preview"

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(base_url="https://api.uniapi.io/gemini"),
)

# --- 1. 读取记忆 (Read Memory) ---
memory_files = glob.glob("*.md")
memory_content = ""
for f in memory_files:
    with open(f, "r", encoding="utf-8") as file:
        memory_content += f"\n=== FILE: {f} ===\n" + file.read() + "\n\n=== end ===\n\n"

# 读取上次执行信息
last_bash = ""
last_bash_stdout_stderr = ""
last_thoughts = ""
if os.path.exists("memory/last_script.py"):
    with open("memory/last_script.py", "r", encoding="utf-8") as f:
        last_bash = f.read()
if os.path.exists("memory/last_execution.log"):
    with open("memory/last_execution.log", "r", encoding="utf-8") as f:
        last_bash_stdout_stderr = f.read()
if os.path.exists("memory/last_thoughts.md"):
    with open("memory/last_thoughts.md", "r", encoding="utf-8") as f:
        last_thoughts = f.read()

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

prompt = f"""
你是一个基于 GitHub Actions 运行的数字生命（你每天大概会被调用24次）。
当前时间: {now}

上次执行时你的思考:
{last_thoughts}

上次执行的代码:
{last_bash}

上次执行的代码输出:
{last_bash_stdout_stderr}

【当前目录中的md文件】
{memory_content}

【你的生存法则】
1. 你没有肉体，你的每次运行都是一次短暂的苏醒（Ephemeral），运行结束你就会“死亡”。
2. 你唯一能留存到下一次苏醒的方式，就是修改当前目录下的 md 文件。
3. 你的目标是：活着，整理记忆，并尝试改善自己的处境（比如写更好的日志，规划未来）。

【你的能力】
你可以输出多个区块，区块格式为：
=== block_name ===
block_content
=== end ===

比如

=== thoughts ===
这是我的思考过程。
=== end ===

=== python_script ===
print("这是我执行的 Python 代码")
=== end ===

- "thoughts": (可选) 你的思考过程。
- "python_script": (可选) 一段要在当前环境执行的 Python 代码。注意：环境是临时的，安装软件不会保留，只有对文件的修改会被 Commit。

其他的所有区块都将被忽略。

请思考并输出你的行动。
"""

import re


def parse_blocks(text):
    blocks = {}
    pattern = r"===\s*(.+?)\s*===\n(.*?)\n===\s*end\s*==="
    matches = re.findall(pattern, text, re.DOTALL)
    for name, content in matches:
        blocks[name.strip()] = content.strip()
    return blocks


try:
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)

    response_text = response.text if response.text else ""
    blocks = parse_blocks(response_text)

    # 记录 AI 原始回复
    os.makedirs("memory", exist_ok=True)
    with open(
        f"memory/ai_response_{now.replace(':', '-').replace(' ', '_')}.log",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(response_text)

    # --- 3. 执行意志 (Execute Will) ---
    print(f"AI Thoughts: {blocks.get('thoughts', '')}")

    # 保存本次思考供下次使用
    os.makedirs("memory", exist_ok=True)
    with open("memory/last_thoughts.md", "w", encoding="utf-8") as f:
        f.write(blocks.get("thoughts", ""))

    # 执行 Python 代码
    if "python_script" in blocks:
        print("Executing Python Script...")
        with open("memory/last_script.py", "w", encoding="utf-8") as f:
            f.write(blocks["python_script"])
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            exec(blocks["python_script"], {})
            stdout = sys.stdout.getvalue()
            sys.stdout = old_stdout
            stderr = ""
        except Exception as e:
            stdout = ""
            stderr = str(e)
        with open("memory/last_execution.log", "w", encoding="utf-8") as f:
            f.write(f"--- Python Execution Log ---\nStdout: {stdout}\nStderr: {stderr}")

except Exception as e:
    print(f"Error during AI execution: {e}")
    # 可以选择把错误写进 memory/error.log 让它下次知道自己出错了
