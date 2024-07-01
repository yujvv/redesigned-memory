from flask import Flask, request, jsonify
from multi_motion_query import ActionSemanticRetriever
from sentence_transformers import SentenceTransformer


actions_semantics = {
    "1": [
        # Providing information or clarification-answer_question
        "让我为您解答这个问题。",
        "我很高兴为您提供这方面的信息。",
        "这个问题的答案是...",
        "根据我所知，情况是这样的...",
        "我可以这样回答您的问题...",
        "关于这一点，我的理解是...",
        "让我来详细解释一下...",
        "这个问题很有趣，答案是...",
        "我很乐意为您澄清这一点。",
        "让我们一起来分析这个问题。"
    ],
    "2": [
        # Saying farewell-goodbye
        "再见，祝您有个愉快的一天！",
        "非常感谢您的时间，再见。",
        "希望我们很快能再次见面，再见。",
        "再见，如果还有问题随时联系我。",
        "祝您接下来一切顺利，再见。",
        "很高兴能为您服务，再见。",
        "再见，期待下次与您交流。",
        "祝您今天愉快，再见。",
        "感谢您的光临，再见。",
        "再见，请保重。"
    ],
    "3": [
        # Expressing readiness or availability-idle
        "有什么我可以帮您的吗？",
        "我在这里，随时为您服务。",
        "需要任何帮助就告诉我。",
        "您有什么问题吗？",
        "我随时准备协助您。",
        "有什么我可以解答的吗？",
        "如果您需要帮助，我就在这里。",
        "您想了解些什么？",
        "我很乐意为您提供帮助。",
        "请问有什么我可以为您做的？"
    ],
    "4": [
        # Discussing or describing images-picture_related
        "这张图片展示了...",
        "让我来描述一下这幅图像。",
        "这张照片中，我们可以看到...",
        "图片的主要内容是...",
        "这幅画的有趣之处在于...",
        "从这张图中，我们可以了解到...",
        "这张图片的背景似乎是...",
        "图中最引人注目的是...",
        "这幅图像给人的感觉是...",
        "让我们来分析一下这张图片的构图。"
    ],
    "5": [
        # Responding to information or events-reaction
        "哇，真是令人惊讶！",
        "这个消息真是太棒了！",
        "我完全没想到会这样。",
        "这确实是个有趣的发展。",
        "我对此感到非常兴奋。",
        "这是个令人深思的情况。",
        "我对此持谨慎乐观的态度。",
        "这个消息让我有些担心。",
        "我对此感到非常同情。",
        "这真是个出人意料的转折。"
    ],
    "6": [
        # Expressing disagreement or refusal-reject
        "对不起，我恐怕不能同意这一点。",
        "我理解您的观点，但我持不同意见。",
        "很遗憾，我们无法接受这个提议。",
        "我不认为这是一个好主意。",
        "恐怕这不太可行。",
        "我们需要考虑其他选择。",
        "这个方案可能不太适合我们。",
        "我们无法支持这个决定。",
        "我们需要重新考虑这个问题。",
        "很抱歉，我们必须拒绝这个请求。"
    ],
    "7": [
        # Discussing or analyzing text-text_related
        "这段文字的主要观点是...",
        "让我们来分析一下这篇文章。",
        "这个段落强调了...",
        "作者在这里想表达的是...",
        "这段话的关键词是...",
        "从这个文本中，我们可以推断...",
        "这篇文章的结构是...",
        "让我为您总结一下这段内容。",
        "这个句子的含义可能是...",
        "这段文字使用了很有趣的修辞手法。"
    ],
    "8": [
        # Discussing or describing videos-video_related
        "这段视频主要展示了...",
        "让我来描述一下这个视频的内容。",
        "视频中最引人注目的部分是...",
        "这个视频的主题似乎是...",
        "从这段影片中，我们可以看出...",
        "视频的背景音乐增添了...",
        "这个视频的剪辑技巧非常独特。",
        "视频中的人物表现出...",
        "这段视频给人的整体感觉是...",
        "让我们来分析一下这个视频的构图和镜头运用。"
    ]
}


EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
embedding_model = SentenceTransformer(EMBEDDING_PATH)
retriever = ActionSemanticRetriever(embedding_model, actions_semantics)



app = Flask(__name__)

@app.route('/get_action', methods=['POST'])
def get_action():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # 检索相关动作
    relevant_actions = retriever.query_actions(query)
    if not relevant_actions:
        return jsonify({"error": "No relevant actions found"}), 404
    
    # query = "你好,我将用右手为您指路。"
    # relevant_actions = retriever.query_actions(query)
    # for action, semantic, score in relevant_actions:
    #     print(f'Action: {action}, Semantic: {semantic}, Score: {score}')

    # 获取第一个相关动作的编号
    action_index = relevant_actions[0][0]

    for action, semantic, score in relevant_actions:
        print(f'Action: {action}, Semantic: {semantic}, Score: {score}')

    return jsonify({"action_number": action_index})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7777)
