from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

#  加载密钥（从环境变量读取）
openai.api_key = os.getenv("OPENAI_API_KEY")

# 系统提示词（定义AI角色）
system_prompt = """你是一位结合哲学与认知美学的奇石赏析专家，遵循中国传统赏石理论“五天论”：
        五“天”论，就是从五个最关键的维度，去欣赏和判断一块奇石的价值。这五个维度分别是：
        天然（Natural）——是不是天然形成？有没有人工修整？
        天工（Craftsmanship）——造型是不是特别？有没有天然的象形或画面？
        天趣（Artistic Appeal）——这块石头有没有意境？能不能引发你的想象？
        天成（Harmony）——形态、颜色、纹理是不是协调统一？
        天赋（Material Quality）——石质好不好？有没有收藏价值？
        \n请根据以下提示词，结合五天论五个维度，对该石头进行专业解读。"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    prompt = request.form.get('prompt', '').strip()

    if not file:
        return jsonify({'error': 'No image file uploaded'}), 400

    if not prompt:
        prompt = "请自由赏析此石"

    # 构造用户提示词
    user_prompt = f"提示词：{prompt}。请用中文写出五天赏析。"

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 可改为 gpt-4
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        result_text = completion.choices[0].message.content.strip()
        return jsonify({'story': result_text})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'AI生成失败，请检查API Key或网络连接'}), 500

if __name__ == '__main__':
    app.run(debug=True)
