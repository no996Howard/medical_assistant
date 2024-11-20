import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 目标网址（中药材列表页）
base_url = "http://www.zhongyoo.com/name/"

# 设置保存路径
save_dir = "pictures"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 创建一个txt文件，用于储存中药材信息
txt_file = "herb_description.txt"
with open(txt_file, "w", encoding="utf-8") as f:
    f.write("中药材数据\n\n")  # 文件标题

# 创建一个zip文件来存储图片
zip_filename = "herb_images.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:

    # 发送请求获取页面内容
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # 提取所有中药材名称和详情页链接
        links = soup.find_all("a", class_="title")  # 根据HTML的实际 class 名调整
        for link in links:
            name = link.text.strip()  # 提取中药材名称
            detail_url = urljoin(base_url, link["href"])  # 构造详情页完整URL

            # 访问详情页
            detail_response = requests.get(detail_url)
            if detail_response.status_code == 200:
                detail_soup = BeautifulSoup(detail_response.content, "html.parser")

                # 提取图片URL
                img_tag = detail_soup.find("img")  # 找到图片的 <img> 标签（调整选择器）
                img_url = urljoin(detail_url, img_tag["src"]) if img_tag else None

                # 提取描述信息（假设描述存放在多个 <p> 标签中）
                description_tags = detail_soup.find_all("p")  # 找到所有 <p> 标签
                description = "\n".join([ "<p>" + tag.get_text().replace('\n', '<br>').strip() + "</p>" for tag in description_tags]) if description_tags else "<p>暂无描述信息</p>"



                
                # 下载图片并保存到本地
                if img_url:
                    img_name = f"{name}.jpg".replace("/", "-")  # 防止非法字符
                    img_path = os.path.join(save_dir, img_name)
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        with open(img_path, "wb") as img_file:
                            img_file.write(img_response.content)
                        # 将图片添加到zip包中
                        zipf.write(img_path, arcname=img_name)
                        print(f"图片下载成功：{name} -> {img_name}")
                    else:
                        print(f"图片下载失败：{img_url}")
                else:
                    print(f"未找到图片：{name}")

                # 将药材信息写入txt文件
                with open(txt_file, "a", encoding="utf-8") as f:
                    f.write(f'if herb_choice == "{name}":\n')
                    f.write(f'    st.markdown("{name},{description}")\n')
                    f.write(f'    st.image("D:\medical_assistant\pictures\{name}.jpg")\n\n')

            else:
                print(f"详情页请求失败：{detail_url}")
    else:
        print(f"请求失败，状态码：{response.status_code}")

print("爬取完成，所有中药材信息已保存！")
