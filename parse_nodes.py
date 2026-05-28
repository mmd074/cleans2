import requests
import random

def get_flag_emoji(code):
    """تبدیل کد ۲ حرفی کشور به ایموجی پرچم"""
    if len(code) != 2 or not code.isalpha():
        return code
    
    base = ord("🇦") - ord("A")
    return (
        chr(base + ord(code[0].upper())) +
        chr(base + ord(code[1].upper()))
    )

# چند منبع
urls = [
    "https://github.com/clubgratis/Proxy/raw/refs/heads/main/all.txt",
    "https://raw.githubusercontent.com/xsm-syn/Nautica/refs/heads/main/proxyip.txt",
    # مثال:
    # "https://example.com/list1.txt",
    # "https://example.com/list2.txt",
]

all_lines = []

# گرفتن همه لیست‌ها
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        lines = response.text.strip().split("\n")
        all_lines.extend(lines)

        print(f"Loaded {len(lines)} lines from: {url}")

    except Exception as e:
        print(f"Failed to load {url}")
        print(e)

# حذف آیتم‌های تکراری
all_lines = list(set(all_lines))

valid_nodes = []

for line in all_lines:
    parts = [p.strip() for p in line.split(",")]

    if len(parts) >= 4:
        ip = parts[0]
        port = parts[1]
        name = parts[2]
        dc = parts[3]

        country_code = name[:2].upper()
        server_name = name[2:] if len(name) > 2 else name

        display_name = f"{get_flag_emoji(country_code)}{server_name}"

        valid_nodes.append(
            f"{ip}:{port}#{display_name}_{dc}"
        )

# انتخاب رندوم
num_to_select = min(150, len(valid_nodes))
random_nodes = random.sample(valid_nodes, num_to_select)

# ذخیره
with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in random_nodes:
        f.write(node + "\n")

print(
    f"Done! {len(valid_nodes)} total unique nodes, "
    f"{len(random_nodes)} random selected."
)
