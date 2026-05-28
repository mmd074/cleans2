import requests
import random

def get_flag_emoji(code):
    """تبدیل کد کشور به ایموجی پرچم"""
    if len(code) != 2 or not code.isalpha():
        return code

    base = ord("🇦") - ord("A")

    return (
        chr(base + ord(code[0].upper())) +
        chr(base + ord(code[1].upper()))
    )

# منابع مختلف
urls = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
    # سورس‌های بیشتر اضافه کن
    # "https://example.com/list1.txt",
    # "https://example.com/list2.txt",
]

all_lines = []

# گرفتن همه لیست‌ها
for url in urls:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        lines = response.text.strip().split("\n")

        all_lines.extend(lines)

        print(f"Loaded {len(lines)} lines from {url}")

    except Exception as e:
        print(f"Failed to load {url}")
        print(e)

# حذف موارد تکراری
all_lines = list(set(all_lines))

valid_nodes = []

for line in all_lines:

    parts = [p.strip() for p in line.split(",")]

    if len(parts) >= 4:

        ip = parts[0]
        port = parts[1]
        name = parts[2]
        dc = parts[3]

        # پرچم کشور
        country_code = name[:2].upper()

        # اسم سرور
        server_name = name[2:] if len(name) > 2 else name

        display_name = f"{get_flag_emoji(country_code)}{server_name}"

        node = f"{ip}:{port}#{display_name}_{dc}"

        valid_nodes.append(node)

# حذف نودهای تکراری
valid_nodes = list(set(valid_nodes))

# شافل کامل برای رندوم واقعی
random.shuffle(valid_nodes)

# -------------------------
# فایل 150 تایی
# -------------------------

small_nodes = valid_nodes[:min(150, len(valid_nodes))]

with open("nodes.txt", "w", encoding="utf-8") as f:

    for node in small_nodes:
        f.write(node + "\n")

# -------------------------
# فایل 5000 تایی
# -------------------------

big_nodes = valid_nodes[:min(5000, len(valid_nodes))]

with open("nodes_5000.txt", "w", encoding="utf-8") as f:

    for node in big_nodes:
        f.write(node + "\n")

print("===================================")
print(f"Total unique nodes: {len(valid_nodes)}")
print(f"Saved 150 nodes -> nodes.txt")
print(f"Saved 5000 nodes -> nodes_5000.txt")
print("Done!")
