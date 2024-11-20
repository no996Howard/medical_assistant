import streamlit as st
import random
import zhipuai as zp
import pyttsx4 as pyttsx4
import requests
import base64

# 初始化会话状态
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
if 'output_data' not in st.session_state:
    st.session_state['output_data'] = []

# API密钥
zp.api_key = "5c4b3cc18b174a36c0e55e8d2c5a2a9a.fdgOoSvK7xsLpcKo"

# 李时珍图片
def display_li_shizhen_image():
    st.image('li_shizhen.png')

# 文字转语音
def text_to_speech(text):
    engine = pyttsx4.init()
    id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\SPEECH\\Voices\\Tokens\\TTS_MS_ZH-CN_KANGKANG_11.0"
    engine.setProperty('voice', id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()

# 主页面函数
def page2():
    st.title("小郎中拜师: 与师交流")
    st.write("在这里我们将从师于李时珍喔，大朋友小朋友如果有什么疑惑敬请询问喔，李老先生将会给予你满意的答复喔！")

    display_li_shizhen_image()

    # 用户输入
    user_input = st.text_input("输入你想问的药材：", st.session_state['user_input'])

    # 如果用户输入了内容，则调用模型API
    if user_input and user_input != st.session_state['user_input']:
        st.session_state['user_input'] = user_input
        st.write("请稍等，我正在从我的《本草纲目》中为你准备药材的功效...")
        text_to_speech("请稍等，我正在从我的《本草纲目》中为你准备药材的功效...")
        response = zp.model_api.sse_invoke(
            model="chatglm_6b",
            content=user_input,
            prompt=[{"role": "user", "content": user_input + "的功效是什么？用小孩子能听的话说"}],
            temperature=0.9,
            top_p=0.7,
            incremental=True
        )

        output_data = []
        # 实时显示AI回应
        for event in response.events():
            if event.event == "add":
                cleaned_data = event.data.strip()
                if cleaned_data.endswith(','):
                    cleaned_data = cleaned_data[:-1] + ' '
                output_data.append(cleaned_data)
            elif event.event == "error" or event.event == "interrupted":
                st.error(event.data)
            elif event.event == "finish":
                output_data.append(event.data.strip())
                break
            else:
                output_data.append(event.data.strip())

        # 获取AI的回复
        response_text = ''.join(output_data).strip()
        st.session_state['output_data'] = response_text  # 保存输出数据到会话状态

        # 显示AI生成的文本
        st.write(f"李时珍：{response_text}")

        # 文字转语音并播放
        if response_text:
            text_to_speech(response_text)

    

# 识别植物
def page4():
    # 让用户上传图片
    uploaded_file = st.file_uploader("请上传您想识别的图片：（为保证识别效果，文件大小请保持在10MB以下；支持的文件格式：JPG, JPEG, PNG）", type=['jpg', 'jpeg', 'png'])

    # 检查是否有文件被上传
    if uploaded_file is not None:
        # 读取图片内容并进行base64编码
        encoded_string = base64.b64encode(uploaded_file.read()).decode()

        # 构建请求数据
        data = {
            'image': encoded_string,
            'baike_num': 1  # 可选参数，这里设置为1表示返回一个百科信息
        }

        # 构建请求头
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # 从百度云获取 access_token
        def get_access_token():
            host = 'https://aip.baidubce.com/oauth/2.0/token'
            params = {
                'grant_type': 'client_credentials',
                'client_id': '5sYiWNWSHg3KS6Mqa4eQvMQe',
                'client_secret': '40314FfsgaLbUyo8uKlOrp0tL06HXmaJ'
            }
            response = requests.get(host, params=params)
            if response:
                return response.json()['access_token']
            return None

        def text_to_speech(text):
            engine = pyttsx4.init()
            
            id = "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens\TTS_MS_ZH-CN_KANGKANG_11.0"#Male_voice
            engine.setProperty('voice', id)
            engine.setProperty('rate', 150)  # 语速
            engine.setProperty('volume', 0.9)  # 音量
            engine.say(text)
            engine.runAndWait()

        # 获取 access_token
        access_token = get_access_token()

        # 检查 access_token 是否有效
        if access_token:
            # 构建请求URL
            url = f'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}'

            # 发送POST请求
            response = requests.post(url, headers=headers, data=data)

            # 检查响应状态码
            if response.status_code == 200:
                # 解析响应内容
                result = response.json()
                # 检查是否有结果
                if 'result' in result and result['result']:
                    # 找到得分最高的结果
                    top_result = max(result['result'], key=lambda x: x['score'])
                    st.write("识别结果：")
                    text_to_speech("识别结果：")
                    st.write(f"名称：{top_result['name']}")
                    text_to_speech(f"名称：{top_result['name']}")
                    st.write(f"置信度：{top_result['score']:.4f}")
                    text_to_speech(f"置信度：{top_result['score']:.4f}")
                    # 检查是否有百科信息
                    if 'baike_info' in top_result and top_result['baike_info'].get('description', ''):
                        st.write(f"描述：{top_result['baike_info']['description']}")
                        text_to_speech(f"描述：{top_result['baike_info']['description']}")
                    else:
                        st.write("暂无描述信息。")
                        text_to_speech("暂无描述信息。")
                    # 显示图片
                    st.image(uploaded_file, caption='上传的图片', use_column_width=True)
                else:
                    st.error("没有识别结果。")
            else:
                st.error(f"请求失败，状态码：{response.status_code}")
        else:
            st.error("获取 access_token 失败，请检查 AK 和 SK 是否正确。")
    else:
        st.write("请上传一张图片。")
    st.write("若想了解更多，请在左侧进行选择，进入小郎中拜大师页面", height=50)

st.title('郎中培养日记')
# 熟悉中草药
def page1():
    st.title("药郎中学药材: 熟悉药材")
    st.write("熟悉药草是一个郎中的必修课，所以我们先见识一些常见的草药吧！:sunglasses:")
    # 药材列表
    # st.subheader('药材列表')
    herbs = [
        "人参",
        "黄芪",
        "当归",
        "金银花",
        "党参",
        "人参",
        "黄芪",
        "当归",
        "党参",
        "半夏",
        "鱼胆草",
        "路路通",
        "胆木",
        "山姜",
        "藤黄",
        "肉豆蔻",
        "山萸肉",
        "萝藦",
        "乌桕子",
        "一点红",
        "醉鱼草",
        "铁苋",
        "八角莲",
        "海马",
        "九节菖蒲",
        "防风草",
        "豆蔻",
    ]
    # st.write(herbs)
    # 选择药材
    st.subheader("选择一种药材了解更多")
    herb_choice = st.selectbox("选择一种药材", herbs)
    # 显示选中的药材信息
    if herb_choice:
        st.write(f"你选择的是：{herb_choice}")
        with st.expander("显示详细信息"):
            if herb_choice == "人参":
                st.write("人参，五加科植物，被誉为'百草之王'，具有大补元气、复脉固脱等功效。")
                st.image("pictures/yc1.bmp")  # 人参图片
            elif herb_choice == "黄芪":
                st.write("黄芪，豆科植物，有增强免疫力、利尿消肿等作用。")
                st.image("pictures/yc2.bmp")  # 黄芪图片
            elif herb_choice == "当归":
                st.write("当归，伞形科植物，用于补血活血、调经止痛。")
                st.image("pictures/yc3.bmp")  # 当归图片
            elif herb_choice == "党参":
                st.markdown("党参, 人参科植物，有补中益气、健脾益肺等功效。")
                st.image("pictures/党参.jpg")
            elif herb_choice == "半夏":
                st.markdown("半夏, 天南星科植物，有燥湿化痰、降逆止呕等功效。")
                st.image("pictures/半夏.jpg")
            elif herb_choice == "鱼胆草":
                st.markdown("鱼胆草, 龙胆科植物，有清热泻火、解毒利湿等功效。")
                st.image("pictures/鱼胆草.jpg")
            elif herb_choice == "路路通":
                st.markdown("路路通, 金缕梅科植物，有祛风活络、利水通经等功效。")
                st.image("pictures/路路通.jpg")
            elif herb_choice == "胆木":
                st.markdown("胆木, 茜草科植物，有清热解毒、消肿止痛等功效。")
                st.image("pictures/胆木.jpg")
            elif herb_choice == "山姜":
                st.markdown("山姜, 姜科植物，有温中散寒、祛风活血等功效。")
                st.image("pictures/山姜.jpg")
            elif herb_choice == "藤黄":
                st.markdown("藤黄, 藤黄科植物，有消肿排脓、散瘀解毒等功效。")
                st.image("pictures/藤黄.jpg")
            elif herb_choice == "肉豆蔻":
                st.markdown("肉豆蔻, 肉豆蔻科植物，有温中行气、涩肠止泻等功效。")
                st.image("pictures/肉豆蔻.jpg")
            elif herb_choice == "山萸肉":
                st.markdown("山萸肉, 山茱萸科植物，有补益肝肾、涩精固脱等功效。")
                st.image("pictures/山萸肉.jpg")
            elif herb_choice == "萝藦":
                st.markdown("萝藦, 萝藦科植物，有补精益气、通乳解毒等功效。")
                st.image("pictures/萝藦.jpg")
            elif herb_choice == "乌桕子":
                st.markdown("乌桕子, 大戟科植物，有杀虫、利水通便等功效。")
                st.image("pictures/乌桕子.jpg")
            elif herb_choice == "一点红":
                st.markdown("一点红, 菊科植物，有清热解毒、消炎利尿等功效。")
                st.image("pictures/一点红.jpg")
            elif herb_choice == "醉鱼草":
                st.markdown("醉鱼草, 马钱科植物，有止咳定喘、活血祛瘀等功效。")
                st.image("pictures/醉鱼草.jpg")
            elif herb_choice == "铁苋":
                st.markdown("铁苋, 大戟科植物，有清热利湿、凉血解毒等功效。")
                st.image("pictures/铁苋.jpg")
            elif herb_choice == "八角莲":
                st.markdown("八角莲, 小檗科植物，有化痰散结、祛瘀止痛等功效。")
                st.image("pictures/八角莲.jpg")
            elif herb_choice == "海马":
                st.markdown("海马, 海龙科动物，有温肾壮阳、散结消肿等功效。")
                st.image("pictures/海马.jpg")
            elif herb_choice == "九节菖蒲":
                st.markdown("九节菖蒲, 毛莨科植物，有开窍化痰、醒脾安神等功效。")
                st.image("pictures/九节菖蒲.jpg")
            elif herb_choice == "防风草":
                st.markdown("防风草, 唇形科植物，有祛风除湿、解毒止痛等功效。")
                st.image("pictures/防风草.jpg")
            elif herb_choice == "豆蔻":
                st.markdown("豆蔻, 姜科植物，有化湿消痞、行气温中等功效。")
                st.image("pictures/豆蔻.jpg")

    st.title("欢迎来到药材猜猜乐")
    st.write("这是一个通过图片猜测药材名称的小游戏。")
    herbs_data = [
        {"name": "人参", "image": "pictures/yc1.bmp"},
        {"name": "黄芪", "image": "pictures/yc2.bmp"},
        {"name": "当归", "image": "pictures/yc3.bmp"},
        {"name": "金银花", "image": "pictures/yc4.bmp"},
        {"name": "党参", "image": "pictures/党参.jpg"},
        {"name": "半夏", "image": "pictures/半夏.jpg"},
        {"name": "鱼胆草", "image": "pictures/鱼胆草.jpg"},
        {"name": "路路通", "image": "pictures/路路通.jpg"},
        {"name": "胆木", "image": "pictures/胆木.jpg"},
        {"name": "山姜", "image": "pictures/山姜.jpg"},
        {"name": "藤黄", "image": "pictures/藤黄.jpg"},
        {"name": "肉豆蔻", "image": "pictures/肉豆蔻.jpg"},
        {"name": "山萸肉", "image": "pictures/山萸肉.jpg"},
        {"name": "萝藦", "image": "pictures/萝藦.jpg"},
        {"name": "乌桕子", "image": "pictures/乌桕子.jpg"},
        {"name": "一点红", "image": "pictures/一点红.jpg"},
        {"name": "醉鱼草", "image": "pictures/醉鱼草.jpg"},
        {"name": "铁苋", "image": "pictures/铁苋.jpg"},
        {"name": "八角莲", "image": "pictures/八角莲.jpg"},
        {"name": "海马", "image": "pictures/海马.jpg"},
        {"name": "九节菖蒲", "image": "pictures/九节菖蒲.jpg"},
        {"name": "防风草", "image": "pictures/防风草.jpg"},
        {"name": "豆蔻", "image": "pictures/豆蔻.jpg"},
    ]
    # 设置游戏状态
    # 添加一个按钮，点击后进入游戏
    if st.button("开始游戏"):
        st.session_state["question_herb"] = random.choice(herbs_data)
        st.session_state["game_active"] = True

    if st.session_state.get("game_active", False):
        question_herb = st.session_state["question_herb"]

        with st.form("game_form"):
            st.image(question_herb["image"], caption="猜猜这是什么药材？")
            user_guess = st.text_input("请输入你的猜测：")
            submit_button = st.form_submit_button(label="提交")

        # 判断结果并给出反馈
        if submit_button:
            if user_guess.strip() == question_herb["name"]:
                st.write("恭喜你，答对了！")
            else:
                st.write(f"很遗憾，答错了。正确答案是：{question_herb['name']}")

            # 提供再次游戏的选项
            st.write("---")  # 分隔线
            # 将按钮放在表单外部
            if st.button("再玩一次"):
                st.session_state["game_active"] = False
                st.session_state.pop("question_herb", None)  # 移除药材问题
                st.session_state["question_herb"] = random.choice(
                    herbs_data
                )  # 刷新药材
            if st.button("结束游戏"):
                del st.session_state["question_herb"]  # 清除当前问题
                st.session_state["game_active"] = False
                st.session_state.pop("question_herb", None)  # 移除药材问题
                




#药食同源
def page3():
    st.divider() 
    st.title("小郎中练小手: 药食同源")
    st.write("在这里我们将学习一些之前学过药材，并将实现药食同源！给亲人们一个惊喜。")
    st.title('药食同源菜谱')
   
    # 简介部分
    st.header('药食同源简介')
    st.write("药食同源是指一些食材既可以作为食物，又具有药用价值。这些食材在中医理论中被广泛应用。")

    # 菜谱列表
    st.subheader('药食同源菜谱列表')
    menu = ["当归炖鸡", "黄芪炖羊肉", "枸杞红枣茶", "山药炒木耳"]
    st.write(menu)

    # 选择菜谱
    st.subheader('选择一个菜谱查看详情')
    recipe_choice = st.selectbox("选择一个菜谱", menu)

    # 显示选中的菜谱详情
    if recipe_choice:
        with st.expander("显示做法"):
            if recipe_choice == "当归炖鸡":
                st.write("当归炖鸡具有补血调经的功效。")
                st.image("pictures/ys1.png")  # 当归炖鸡图片文件
                st.write("做法：1. 将当归洗净备用。2. 鸡切块，焯水去血沫。3. 将当归和鸡块一同炖煮2小时。")
            elif recipe_choice == "黄芪炖羊肉":
                st.write("黄芪炖羊肉具有温阳补气的功效。")
                st.image("pictures/ys2.png")  # 黄芪炖羊肉图片文件
                st.write("做法：1. 将黄芪洗净备用。2. 羊肉切块，焯水去血沫。3. 将黄芪和羊肉块一同炖煮2小时。")
            elif recipe_choice == "枸杞红枣茶":
                st.write("枸杞红枣茶具有滋补肝肾、益精明目的功效。")
                st.image("pictures/ys3.png")  # 枸杞红枣茶图片文件
                st.write("做法：1. 将枸杞和红枣洗净。2. 加入适量水煮沸后小火煮10分钟。3. 可加入适量冰糖调味。")
            elif recipe_choice == "山药炒木耳":
                st.write("山药炒木耳具有健脾益肺、补肾涩精的功效。")
                st.image("pictures/ys4.png")  # 山药炒木耳图片文件
                st.write("做法：1. 山药切片，木耳泡发。2. 将山药和木耳一同炒至熟透。3. 加入适量盐和调味料。")

    # 注意事项
    st.subheader('注意事项')
    st.write("在使用药食同源的食材时，应注意以下几点：")
    st.write("- 了解食材的性质和功效")
    st.write("- 根据个人体质选择合适的食材")
    st.write("- 孕妇和特殊人群应在医生指导下使用")
    st.write("- 注意食材的新鲜度和卫生")
    # 相关链接
    st.subheader('相关链接')
    st.write("[了解更多药食同源的知识](http://www.zhongyoo.com/yaoshan/)")



#导航栏文本背景
custom_style2 = """
<style>
.text-box {
    background-color: #A66D56; /* 背景颜色 */
    border: 1px solid #00000; /* 边框颜色和样式 */
    border-radius: 8px; /* 边框圆角 */
    padding: 10px; /* 内边距 */
    margin:50px 0; /* 外边距 */
    max-width: 30px; /* 最大宽度 */
}
</style>
"""
# 应用自定义CSS样式
st.sidebar.markdown(custom_style2, unsafe_allow_html=True)
# 使用自定义样式显示文本
st.sidebar.markdown(
    """
<div class="text-box">
    <h1 style='text-align: center;'>小小大夫</h1>
</div>
""",
    unsafe_allow_html=True,
)




# 创建侧边栏导航
page = st.sidebar.selectbox(
    "选择一个页面:",
    ("主页", "小郎中学药材", "小郎中拜大师", "小郎中练小手","小郎中认植物")
)

# 根据选择的页面显示内容
if page == "主页":
    st.caption(":blush: 欢迎来到欢乐小药堂，你将从这里开始你的小小郎中之旅。")
    st.divider() 
    st.image('D:/xiao.png', width=400,)
    st.markdown(' <p style="font-size:30px;">中医药</p>' , unsafe_allow_html=True)
    st.caption("中医，中华民族瑰宝。以阴阳五行等理论为基础，通过望闻问切诊断病情。采用中药、针灸、推拿等疗法，注重整体观念与辨证论治。历经千年传承，在治疗疾病、养生保健方面发挥着独特作用，为人类健康作出卓越贡献。")
    st.divider() 


elif page == "小郎中学药材":
    page1()
elif page == "小郎中拜大师":
    page2()
elif page == "小郎中练小手":
    page3()
elif page == "小郎中认植物":
    page4()



# 设置侧边栏字体颜色的CSS样式
sidebar_font_color_style = """
<style>
    .st-eg {
        color: #00000; 
    }
</style>
"""
# 应用自定义的CSS样式
st.markdown(sidebar_font_color_style, unsafe_allow_html=True)

custom_style = """
<style>
.text-box {
    background-color: #65544F; /* 背景颜色 */
    border: 1px solid #00000; /* 边框颜色和样式 */
    border-radius: 8px; /* 边框圆角 */
    padding: 15px; /* 内边距 */
    margin: 5px 0; /* 外边距 */
    max-width: 600px; /* 最大宽度 */
}
</style>
"""
# 应用自定义CSS样式
st.sidebar.markdown(custom_style, unsafe_allow_html=True)
# 使用自定义样式显示文本
st.sidebar.markdown(
    """
<div class="text-box">
    <h4>ฅ^•ﻌ•^ฅ</h4>
    <h4>这里将走上条成为小大夫的"当归路"</h4>
</div>
""",
    unsafe_allow_html=True,
)


#左侧导航栏的背景
import base64
# 将本地图片转换为base64编码
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
# 设置侧边栏背景
def sidebar_bg(side_bg):
    side_bg_ext = 'png'
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url(data:image/{side_bg_ext};base64,{get_base64_of_bin_file(side_bg)});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
# 调用函数，设置侧边栏背景图片
sidebar_bg('D:/bj3.png')  


#主页的背景
import base64
# 将本地图片转换为base64编码
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
# 设置背景图片和透明度
def set_png_as_page_bg(png_file, opacity):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    body {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        opacity: {opacity};
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
# 设置背景图片和透明度
set_png_as_page_bg('D:/C.png', 0.9)  # 路径和透明度值







