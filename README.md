# medical_assistant
# 中医药助手项目

## 项目简介
本项目旨在通过现代技术与中医药知识的结合，打造一个有趣、互动的学习平台。用户可以通过应用了解中药材的知识，识别植物，并学习药食同源的烹饪方法。

---

## 功能特点
### 药材学习
- 提供详细的中药材列表，包括药用功效和图片。
- 通过互动游戏测试对药材的辨识能力。

### AI 中药顾问
- 模拟与虚拟“李时珍”的对话，解答药材相关问题。
- 利用自然语言处理技术生成友好的回答。
- 提供文字转语音功能，增强用户体验。

### 植物识别
- 支持上传植物图片，利用 AI 模型进行识别。
- 提供植物名称、描述及相关信息。

### 药食同源菜谱
- 提供将中药材融入日常饮食的菜谱。
- 每道菜谱配有详细做法和图片，方便用户参考。

### 友好交互界面
- 简洁易用的界面，支持侧边栏和自定义背景。
- 鼓励通过游戏和视觉化手段进行学习。

---

### 目录结构
```bash
.
├── medical_assistant.py       # 主应用文件
├── crawler.py                 # 爬虫脚本，用于获取药材数据
├── pictures/                  # 存放药材图片的目录
├── herb_description.txt       # 保存药材描述的文本文件
├── requirements.txt           # Python 依赖库列表

```

## 安装与运行

### 环境需求
- **Python 版本**：3.8 或更高
- **依赖库**：
  - `streamlit`
  - `requests`
  - `BeautifulSoup4`
  - `pyttsx4`
  - `zhipuai`
  - `base64`
  - `zipfile`

### 安装步骤
#### 克隆代码库
```bash
git clone https://github.com/your-repo/Traditional-Medicine-Assistant.git
cd Traditional-Medicine-Assistant](https://github.com/no996Howard/medical_assistant.git
```

### 准备资源
- 下载药材图片并保存到 `pictures` 目录。
- 确保在 `medical_assistant.py` 中正确配置 AI 服务和植物识别的 API 密钥。

## 使用说明
### 药材学习
- 在侧边栏选择“小郎中学药材”。
- 浏览中药材信息，参与互动测试。

### AI 中药顾问
- 选择“小郎中拜大师”，与虚拟李时珍进行交流。
- 输入问题后等待 AI 的回答，支持语音播放。

### 植物识别
- 选择“小郎中认植物”，上传图片进行植物识别。

### 药食同源菜谱
- 选择“小郎中练小手”，查看药材相关菜谱，并尝试制作。

## 开发注意事项
### API 配置
- 确保已正确配置 Zhipu AI 和百度植物识别的 API 密钥。

### 数据来源
- 爬虫脚本从指定网站（zhongyoo.com）获取中药材数据和图片。

## 未来改进
- 扩展药材数据库，增加详细描述。
- 支持多语言界面。
- 集成更高级的图片识别模型。

## 项目贡献者
- no996Howard -
- 智谱清言 - AI 模型集成支持
- 百度开源植物识别大模型 - "https://cloud.baidu.com/doc/IMAGERECOGNITION/s/Mk3bcxe9i"

如需更多信息或支持，请联系 hexy@mail.nwpu.edu.cn 
