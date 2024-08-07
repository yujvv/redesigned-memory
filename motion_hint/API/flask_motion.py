from flask import Flask, request, jsonify
from multi_motion_query import ActionSemanticRetriever
from sentence_transformers import SentenceTransformer
import random


actions_set = {
    2: [2, 3, 4],
    3: [6],
    4: [7],
    5: [8],
    6: [27],
    7: [30],
    8: [33],
    9: [37],
    10: [39],
    11: [40],
    12: [65],
    13: [74, 80],
    14: [87, 88, 89],
    15: [92],
    16: [93, 95],
    # 16: [93],
    17: [96, 97, 98],
    18: [108],
    19: [110, 111],
    20: [112],
    21: [113, 115],
    22: [116],
    23: [117],
    24: [118],
    25: [131],
    26: [132],
    27: [133],
    28: [150],
    29: [153],
    30: [156],
    31: [157],
    32: [160],
    33: [161]
}


# actions_semantics = {
#     2: [
#         "有什么需要随时告诉我。",
#         "准备好了就请告诉我。",
#         "有问题随时可以问。",
#         "我会在这里等着。",
#         "需要的时候可以找我。",
#         "如果需要帮助,请随时联系我。",
#         "随时待命。",
#         "我会在附近,有需要随时叫我。",
#         "随时准备协助。",
#         "随时提供帮助。",
#         "需要时请叫我。",
#         "我就在这附近,有事尽管说。",
#         "如果有任何需要,请随时告知。",
#         "准备好时请让我知道。",
#         "有问题请随时提问。",
#         "请随时联系我。",
#         "我会在这里,有需要随时通知我。",
#         "如果有需要,随时叫我。",
#         "有任何需求随时告知。",
#         "我在这等您,有事请叫我。"
#     ],
#     3: [
#         "大家早上好,很高兴见到各位,",
#         "你好,欢迎各位,感谢大家的参与,",
#         "感谢大家的到来,我非常感激,",
#         "今天能见到大家我非常开心,",
#         "我非常高兴欢迎大家的到来,",
#         "各位下午好,感谢你们的光临,",
#         "大家好,很荣幸能在这里见到大家,",
#         "欢迎大家,感谢你们的出席,",
#         "各位好,感谢大家的到来,",
#         "大家好,今天能和大家在一起我感到非常荣幸,",
#         "大家好,很高兴见到这么多熟悉的面孔,",
#         "欢迎各位,非常感谢大家的支持,",
#         "各位朋友们,欢迎你们的到来,",
#         "大家好,感谢你们抽出宝贵时间来参加,",
#         "大家好,能够见到大家我感到非常开心,",
#         "各位好,非常荣幸能在这里见到你们,",
#         "欢迎大家的到来,我非常高兴,",
#         "大家好,非常感谢你们的参与,",
#         "各位朋友们,欢迎光临,",
#         "各位好,今天能在这里见到大家我感到非常荣幸,"
#     ],
#     4: [
#         "跳跳",
#         "跳一下",
#         "跳跃",
#         "你好呀！！",
#         "嗨！！早上好！！",
#         "你好！嘿嘿嘿",
#         "早上好！！今天感觉真棒！",
#         "嘿！你好吗？",
#         "你好！好久不见！",
#         "早安！希望你今天过得愉快！",
#         "嗨！一切都好吗？",
#         "你好！今天精神满满！",
#         "早上好！准备好迎接新的一天了吗？",
#         "嗨！今天有什么新鲜事？",
#         "你好！今天看起来很不错！",
#         "嘿！好兴奋见到你！",
#         "早上好！今天感觉超好！",
#         "你好！希望你有个美好的一天！",
#         "嗨！感觉真好,见到你真开心！",
#         "早安！今天一切顺利吗？",
#         "你好！准备好开始新的一天了吗？",
#         "嘿！今天特别有精神！",
#         "早上好！今天有很多期待的事情！"
#     ],
#     5: [
#         "你好。。。",
#         "早安,有点困。",
#         "晚安,哈欠。",
#         "嘿,有点累了。",
#         "你好,感觉好累。",
#         "早上好,不过我有点疲倦。",
#         "晚上好,今天真是累坏了。",
#         "你好,今天过得挺累的。",
#         "嗨,我有点疲惫。",
#         "晚上好,今天太累了。",
#         "早上好,但我还没完全醒。",
#         "晚安,我要去休息了。",
#         "嗨,今天有点筋疲力尽。",
#         "早安,昨晚没睡好。",
#         "晚上好,我已经累趴了。",
#         "你好,今天真是累人。",
#         "嘿,有点累,感觉需要休息。",
#         "早上好,昨晚没怎么睡。",
#         "晚上好,我已经打了好几个哈欠了。",
#         "你好,今天真的累得不行。"
#     ],
#     6: [
#         "请看右边。",
#         "注意力往右边。",
#         "注意右边。",
#         "向右看。",
#         "看看右边。",
#         "请往右边看。",
#         "注意右侧。",
#         "把目光转向右边。",
#         "请注意右边。",
#         "请看向右侧。",
#         "右边有重要的东西。",
#         "请留意右边。",
#         "请把注意力放在右边。",
#         "右边是重点。",
#         "向右侧看。",
#         "右边有重要信息。",
#         "往右边看一下。",
#         "请关注右边。",
#         "请转向右边。",
#         "注意右手边。"
#     ],
#     7: [
#         "请看左边。",
#         "注意力往左边。",
#         "注意左边。",
#         "向左看。",
#         "看看左边。",
#         "请往左边看。",
#         "注意左侧。",
#         "把目光转向左边。",
#         "请注意左边。",
#         "请看向左侧。",
#         "左边有重要的东西。",
#         "请留意左边。",
#         "请把注意力放在左边。",
#         "左边是重点。",
#         "向左侧看。",
#         "左边有重要信息。",
#         "往左边看一下。",
#         "请关注左边。",
#         "请转向左边。",
#         "注意左手边。"
#     ],
#     8: [
#         "请看前面。",
#         "注意力往前面。",
#         "注意前面。",
#         "向前看。",
#         "看看前面。",
#         "请往前面看。",
#         "注意前侧。",
#         "把目光转向前面。",
#         "请注意前面。",
#         "请看向前侧。",
#         "前面有重要的东西。",
#         "请留意前面。",
#         "请把注意力放在前面。",
#         "前面是重点。",
#         "向前侧看。",
#         "前面有重要信息。",
#         "往前面看一下。",
#         "请关注前面。",
#         "请转向前面。",
#         "注意您前面。"
#     ],
#     9: [
#         "请看上面的选项。",
#         "请看上面这点。",
#         "我们集中注意力在上面这点。",
#         "请注意上面的这个细节。",
#         "请看上面这个部分。",
#         "请把目光转向上面的这个点。",
#         "请留意上面的这一点。",
#         "请看向上面的这个位置。",
#         "上面的这个点很重要。",
#         "请把注意力集中在上面这个小点上。",
#         "上面这里请注意。",
#         "请关注上面的这个选项。",
#         "请看上面这个小目标。",
#         "向上面看这个细节。",
#         "上面有个重要点。",
#         "请看上面这个特定的点。",
#         "请留意上面的这个小部分。",
#         "请看上面的这个关键点。",
#         "请把注意力放在上面这个细节。",
#         "上面这个点请注意。"
#     ],
#     10: [
#         "请看右边选项。",
#         "请看右边这点。",
#         "我们集中注意力在右边这点。",
#         "请注意右边的这个细节。",
#         "请看右边这个部分。",
#         "请把目光转向右边的这个点。",
#         "请留意右边的这一点。",
#         "请看向右侧的这个位置。",
#         "右边的这个点很重要。",
#         "请把注意力集中在右边这个小点上。",
#         "右边这里请注意。",
#         "请关注右边的这个选项。",
#         "请看右边这个小目标。",
#         "向右侧看这个细节。",
#         "右边有个重要点。",
#         "请看右边这个特定的点。",
#         "请留意右侧的这个小部分。",
#         "请看右边的这个关键点。",
#         "请把注意力放在右边这个细节。",
#         "右边这个点请注意。"
#     ],
#     11: [
#         "请看左边选项。",
#         "请看左边这点。",
#         "我们集中注意力在左边这点。",
#         "请注意左边的这个细节。",
#         "请看左边这个部分。",
#         "请把目光转向左边的这个点。",
#         "请留意左边的这一点。",
#         "请看向左侧的这个位置。",
#         "左边的这个点很重要。",
#         "请把注意力集中在左边这个小点上。",
#         "左边这里请注意。",
#         "请关注左边的这个选项。",
#         "请看左边这个小目标。",
#         "向左侧看这个细节。",
#         "左边有个重要点。",
#         "请看左边这个特定的点。",
#         "请留意左侧的这个小部分。",
#         "请看左边的这个关键点。",
#         "请把注意力放在左边这个细节。",
#         "左边这个点请注意。"
#     ],
#     12: [
#         "交给我吧,包在我身上。",
#         "别担心,我来处理。",
#         "放心,我会处理的。",
#         "我来解决这个问题,没问题的。",
#         "交给我,保证完成。",
#         "我来搞定,放心。",
#         "这个问题交给我处理。",
#         "我会负责到底。",
#         "你就交给我吧,没问题。",
#         "这件事交给我办。",
#         "我来负责,保证搞定。",
#         "交给我吧,我会处理好的。",
#         "这事包在我身上,你放心。",
#         "让我来处理,保证没问题。",
#         "我会搞定的,放心吧。",
#         "我来解决,一定没问题。",
#         "我会全力以赴处理好。",
#         "交给我,放心吧。",
#         "我来处理,不用担心。",
#         "这件事我来负责,没问题。"
#     ],
#     13: [
#         "再见。",
#         "回见。",
#         "期待下次再会。",
#         "下次见。",
#         "回头见。",
#         "拜拜。",
#         "保重。",
#         "祝好。",
#         "后会有期。",
#         "祝你一切顺利。",
#         "下次再聊。",
#         "希望很快再见到你。",
#         "期待下次见面。",
#         "有缘再见。",
#         "改天见。",
#         "先告辞了。",
#         "暂别。",
#         "祝你一天愉快。",
#         "期待我们的下次见面。",
#         "祝你一切安好。"
#     ],
#     14: [
#         "感谢您的理解。"
#         "我们非常重视您的意见。",
#         "非常感谢您的合作。",
#         "我们尊重您的贡献。",
#         "能与您合作是我们的荣幸。",
#         "感谢您的支持。",
#         "我们感谢您的配合。",
#         "我们非常感激您的投入。",
#         "感谢您对我们的帮助。",
#         "与您合作是我们的荣幸。",
#         "我们重视您的反馈。",
#         "感谢您的耐心。",
#         "感谢您的信任。",
#         "我们非常感激您的理解。",
#         "感谢您的建议。",
#         "您的贡献对我们非常重要。",
#         "我们感谢您的参与。",
#         "您的合作对我们来说非常重要。",
#         "我们感谢您的意见。",
#         "感谢您与我们合作。"
#     ],
#     15: [
#         "那我为你鼓掌",
#         "拍手",
#         "鼓掌",
#         "你真棒！",
#         "太厉害了！！",
#         "好强啊！",
#         "你太牛了！",
#         "真了不起！",
#         "太精彩了！",
#         "你表现得太好了！",
#         "真是高手！",
#         "太优秀了！",
#         "你真是个天才！",
#         "你做得太好了！",
#         "太佩服你了！",
#         "你真是我的偶像！",
#         "你太有才了！",
#         "你真是无敌了！",
#         "真是太神了！",
#         "你太出色了！",
#         "你真是超凡脱俗！",
#         "你简直完美！",
#         "你真是才华横溢！"
#     ],
#     16: [
#         "哎呀，没事的。",
#         "你肯定没问题的。",
#         "相信自己没事的。",
#         "别担心，一切都会好起来的。",
#         "放心吧，你能做到的。",
#         "一切都会好起来的。",
#         "没关系的，你可以的。",
#         "别担心，事情会好转的。",
#         "别担心，问题不大。",
#         "你一定可以克服的。",
#         "相信我，你会没事的。",
#         "别紧张，你能搞定的。",
#         "放松点，没什么大不了的。",
#         "一切都会顺利的。"
#         "不用担心，一切都在掌控中。",
#         "你有能力应对的。",
#         "别急，慢慢来，一切都会好的。",
#         "你有这个能力，相信自己。",
#         "一切都会过去的。",
#         "相信你自己，你能行的。"
#     ],
#     17: [
#         "哈哈哈，太好笑了。",
#         "你太搞笑了。",
#         "这句话太好玩了。",
#         "真是笑死我了！",
#         "你简直是个笑星！",
#         "这个笑话真是绝了。",
#         "哈哈哈，笑得我肚子疼。",
#         "你真会逗人笑。",
#         "这个真是太有趣了！",
#         "你真幽默！",
#         "哈哈，这太逗了。",
#         "你这人真是太有意思了。",
#         "你的幽默感真好。",
#         "这个故事太搞笑了。",
#         "哈哈哈，太逗了。",
#         "你说的真有趣。",
#         "哈哈，这真是个好笑话。",
#         "你的笑话真棒！",
#         "笑得我眼泪都出来了。",
#         "你真是个开心果！"
#     ],
#     18: [
#         "太生气了！",
#         "你不要太不要脸！",
#         "我好气啊！",
#         "真是气死我了！",
#         "你太过分了！",
#         "我忍无可忍了！",
#         "这简直不可原谅！",
#         "你怎么可以这样！",
#         "真是太气人了！",
#         "我真的受够了！",
#         "你这样做太过分了！",
#         "这真让人火大！",
#         "你让我很生气！",
#         "我再也不能忍了！",
#         "你这人怎么这样！",
#         "这简直太无耻了！",
#         "我实在气得不行！",
#         "你真是太气人了！",
#         "我快要爆炸了！",
#         "你真是太令人失望了！"
#     ],
#     19: [
#         "啊？为什么？",
#         "这。。我该怎么办。。",
#         "这是什么意思？",
#         "这怎么回事？",
#         "你在说什么？",
#         "我不明白。",
#         "这让我很困惑。",
#         "怎么会这样？",
#         "你能解释一下吗？",
#         "这到底是怎么回事？",
#         "我搞不清楚。",
#         "你说的是什么意思？",
#         "我有点迷茫。",
#         "这让我有点摸不着头脑。",
#         "我不太理解。",
#         "能不能再说一遍？",
#         "我不明白你的意思。",
#         "这让我很困惑。",
#         "我需要更多的解释。",
#         "你能再详细说说吗？"
#     ],
#     20: [
#         "我还在查。",
#         "给我多一点时间。",
#         "我还在处理。",
#         "再稍等一会儿。",
#         "请耐心等待。",
#         "我正在处理中。",
#         "请再等一下。",
#         "我正在解决这个问题。",
#         "请稍候片刻。",
#         "请再给我一点时间。",
#         "我还在进行中。",
#         "我还在核实。",
#         "请稍微多等一会儿。",
#         "我正在查找相关信息。",
#         "请耐心等候。",
#         "我还在处理这个问题。",
#         "请稍稍等待。",
#         "我正在工作中。",
#         "请稍微再等一下。",
#         "我还在解决中。"
#     ],
#     21: [
#         "第一。",
#         "首先。",
#         "有一个重点。",
#         "重要的是。",
#         "需要特别注意的是。",
#         "关键在于。",
#         "必须指出的是。",
#         "尤为重要的是。",
#         "值得强调的是。",
#         "重点在于。",
#         "特别需要关注的是。",
#         "最重要的是。",
#         "需要记住的是。",
#         "核心问题是。",
#         "必须关注的是。",
#         "关键点是。",
#         "有一点必须明确。",
#         "最先要注意的是。",
#         "重要的一点是。",
#         "首先要理解的是。"
#     ],
#     22: [
#         "第二。",
#         "其次。",
#         "有两个点。",
#         "再者。",
#         "另外。",
#         "还有一点。",
#         "接下来。",
#         "其次要注意的是。",
#         "另一个重要的点是。",
#         "第二个重点是。",
#         "另外一个方面。",
#         "另外一个需要关注的是。",
#         "除了上述之外。",
#         "另一点是。",
#         "还有一个关键点是。",
#         "另外一个需要强调的是。",
#         "第二个要点是。",
#         "其次，值得一提的是。",
#         "再有就是。",
#         "再进一步。"
#     ],
#     23: [
#         "第三。",
#         "还有一个点。",
#         "总共有三个论点。",
#         "最后一个要点。",
#         "第三个方面是。",
#         "再一个重要的点是。",
#         "另外一个关键点。",
#         "第三个论点是。",
#         "还有一点需要提及。",
#         "最后但同样重要的是。",
#         "第三个需要注意的是。",
#         "还有一个重要方面。",
#         "最后一个要强调的点是。",
#         "另外一个要点是。",
#         "最后一个方面。",
#         "第三点是。",
#         "还有一个值得关注的点。",
#         "还有一个要强调的方面。",
#         "第三个需要关注的是。",
#         "还有一个重要的论点是。"
#     ],
#     24: [
#         "开始预定饭店。",
#         "开始与联络人通话。",
#         "开始询问。",
#         "开始预定会议室。",
#         "打电话给联系人。",
#         "开始询问价格。",
#         "开始预定机票。",
#         "与客户开始通话。",
#         "开始询问可用性。",
#         "开始预定活动场地。",
#         "拨打电话给供应商。",
#         "开始询问详情。",
#         "开始预定酒店房间。",
#         "与合作伙伴开始通话。",
#         "开始询问服务内容。",
#         "开始预定旅游行程。",
#         "开始与客服代表通话。",
#         "开始询问产品信息。",
#         "开始预定租车服务。",
#         "打电话给支持团队。"
#     ],
#     25: [
#         "结束预定饭店。",
#         "结束与联络人通话。",
#         "结束询问。",
#         "完成预定会议室。",
#         "结束与联系人的通话。",
#         "完成询价。",
#         "完成预定机票。",
#         "结束与客户的通话。",
#         "完成询问可用性。",
#         "结束预定活动场地。",
#         "挂断与供应商的电话。",
#         "完成询问详情。",
#         "完成预定酒店房间。",
#         "结束与合作伙伴的通话。",
#         "完成询问服务内容。",
#         "完成预定旅游行程。",
#         "结束与客服代表的通话。",
#         "完成询问产品信息。",
#         "完成预定租车服务。",
#         "结束与支持团队的电话。"
#     ],
#     26: [
#         "正在预定饭店。",
#         "正在与联络人通话。",
#         "正在询问。",
#         "正在预定会议室。",
#         "正在打电话给联系人。",
#         "正在询问价格。",
#         "正在预定机票。",
#         "正在与客户通话。",
#         "正在询问可用性。",
#         "正在预定活动场地。",
#         "正在拨打电话给供应商。",
#         "正在询问详情。",
#         "正在预定酒店房间。",
#         "正在与合作伙伴通话。",
#         "正在询问服务内容。",
#         "正在预定旅游行程。",
#         "正在与客服代表通话。",
#         "正在询问产品信息。",
#         "正在预定租车服务。",
#         "正在打电话给支持团队。"
#     ],
#     27: [
#         "恐怕那不太对。",
#         "不幸的是，事实并非如此。",
#         "让我们澄清一个常见的误解。",
#         "实际上，那是一个常见的误解。",
#         "不，那不准确。",
#         "很遗憾，这是错误的。",
#         "事实上，情况并非如此。",
#         "让我纠正一下这个误解。",
#         "恐怕你误解了这个点。",
#         "对不起，但这并不正确。",
#         "实际情况并不是这样的。",
#         "这需要澄清一下，因为这是一个误解。",
#         "对不起，这不是事实。",
#         "我得指出，这并不准确。",
#         "这个观点是错误的。",
#         "让我们纠正这个错误的看法。",
#         "恐怕事实并非如此。",
#         "这其实是一个误解。",
#         "不好意思，这不是正确的。",
#         "这个说法不准确。"
#     ],
#     28: [
#         "我不同意。",
#         "那不可能。",
#         "不，谢谢。",
#         "我宁愿不。",
#         "不行。",
#         "对不起，我不能同意。",
#         "恐怕不行。",
#         "我不能接受这个。",
#         "我觉得不妥。",
#         "这不符合我的意愿。",
#         "不好意思，我不能答应。",
#         "这不是我所希望的。",
#         "我不认为这是个好主意。",
#         "对不起，我不能这样做。",
#         "这不适合我。",
#         "我不能同意这个。",
#         "我不同意你的观点。",
#         "不，我不赞成。",
#         "这不行，我不能接受。",
#         "抱歉，我不能答应这个请求。"
#     ],
#     29: [
#         "恐怕那不太对。",
#         "不幸的是，事实并非如此。",
#         "让我们澄清一个常见的误解。",
#         "实际上，那是一个常见的误解。",
#         "不，那不准确。",
#         "很遗憾，这是错误的。",
#         "事实上，情况并非如此。",
#         "让我纠正一下这个误解。",
#         "恐怕你误解了这个点。",
#         "对不起，但这并不正确。",
#         "实际情况并不是这样的。",
#         "这需要澄清一下，因为这是一个误解。",
#         "对不起，这不是事实。",
#         "我得指出，这并不准确。",
#         "这个观点是错误的。",
#         "让我们纠正这个错误的看法。",
#         "恐怕事实并非如此。",
#         "这其实是一个误解。",
#         "不好意思，这不是正确的。",
#         "这个说法不准确。"
#     ],
#     30: [
#         "哎，现在正在下雨。",
#         "天气预报显示现在在下雨。",
#         "现在在下雨哦，别忘了带伞。",
#         "外面正在下雨。",
#         "下雨了，出门记得带伞。",
#         "注意，现在外面有雨。",
#         "现在正下着雨呢。",
#         "外面开始下雨了。",
#         "现在下雨了，小心不要淋湿。",
#         "哎呀，下雨了。",
#         "看来今天会有雨。",
#         "现在在下雨，出门前带把伞。",
#         "外面有雨，注意安全。",
#         "现在下着雨呢，记得带伞。",
#         "正在下雨，小心路滑。",
#         "下雨了，注意防雨。",
#         "今天有雨，记得带伞。",
#         "外面正在下雨，注意防水。",
#         "出门记得带伞，现在下雨。",
#         "外面有雨，出门要小心。"
#     ],
#     31: [
#         "好热啊。",
#         "今天天气很热，别中暑了哦。",
#         "今天太阳很大，注意防晒呀。",
#         "真热，感觉快要融化了。",
#         "外面好热，记得多喝水。",
#         "今天真是个大热天。",
#         "炎热的天气，小心别晒伤了。",
#         "这天气真是热得受不了。",
#         "今天热得让人喘不过气。",
#         "外面火辣辣的，记得防晒。",
#         "今天的气温好高啊。",
#         "热得连风都是热的。",
#         "这天气真是让人汗流浃背。",
#         "今天特别热，出门记得防晒。",
#         "太热了，感觉像在蒸桑拿。",
#         "炎热的天气，注意补水。",
#         "今天是个大热天，注意防暑。",
#         "好热，记得多休息。",
#         "今天阳光好强烈，注意防晒。",
#         "这天气热得让人烦躁。"
#     ],
#     32: [
#         "好冷啊。",
#         "今天天气很冷，别感冒了哦。",
#         "太冷了，注意保暖哦。",
#         "真冷，感觉像在冰箱里。",
#         "外面好冷，记得多穿点。",
#         "今天真是个寒冷的日子。",
#         "寒冷的天气，小心别冻着了。",
#         "这天气真是冷得刺骨。",
#         "今天冷得让人发抖。",
#         "外面寒风刺骨，记得保暖。",
#         "今天的气温好低啊。",
#         "冷得连风都是冰的。",
#         "这天气真是让人哆嗦。",
#         "今天特别冷，出门记得穿暖。",
#         "太冷了，感觉像在北极。",
#         "寒冷的天气，注意保暖。",
#         "今天是个冷天，注意防寒。",
#         "好冷，记得多穿衣服。",
#         "今天寒气逼人，注意保暖。",
#         "这天气冷得让人冻僵。"
#     ]
# }


actions_semantics = {
    2: [
        # Idle state: Expressing readiness and availability
        "有什么需要随时告诉我。",
        "准备好了就请告诉我。",
        "有问题随时可以问。",
        "我会在这里等着。",
        "需要的时候可以找我。",
        "如果需要帮助,请随时联系我。",
        "随时待命。",
        "我会在附近,有需要随时叫我。",
        "随时准备协助。",
        "随时提供帮助。",
    ],
    3: [
        # Formal greeting: Expressing gratitude and welcome
        "打个招呼",
        "问好",
        "大家早上好,很高兴见到各位。",
        "欢迎各位,感谢大家的参与。",
        "感谢大家的到来,我非常感激。",
        "今天能见到大家我非常开心。",
        "我非常高兴欢迎大家的到来。",
        "各位好,感谢你们的光临。",
        "很荣幸能在这里见到大家。",
        "欢迎大家,感谢你们的出席。",
        "今天能和大家在一起我感到非常荣幸。",
        "欢迎各位,非常感谢大家的支持。",
    ],
    4: [
        # Energetic greeting: Expressing enthusiasm and positivity
        "跳跃",
        "跳跳",
        "跳一下",
        "你好呀！！",
        "嗨！！早上好！！",
        "你好！好久不见！",
        "早安！希望你今天过得愉快！",
        "嗨！一切都好吗？",
        "你好！今天精神满满！",
        "早上好！准备好迎接新的一天了吗？",
        "嗨！今天有什么新鲜事？",
        "你好！今天看起来很不错！",
        "嘿！好兴奋见到你！",
    ],
    5: [
        # Tired greeting: Expressing fatigue or sleepiness
        "你好。。。有点困。",
        "早安,不过我有点疲倦。",
        "晚上好,今天真是累坏了。",
        "嗨,我有点疲惫。",
        "晚上好,今天太累了。",
        "早上好,但我还没完全醒。",
        "晚安,我要去休息了。",
        "嗨,今天有点筋疲力尽。",
        "早安,昨晚没睡好。",
        "你好,今天真是累人。",
    ],
    6: [
        # Guiding attention to the right: Using both hands to direct focus
        "请看右边。",
        "注意力往右边。",
        "向右看。",
        "请往右边看。",
        "注意右侧。",
        "把目光转向右边。",
        "请注意右边。",
        "请看向右侧。",
        "右边有重要的东西。",
        "请留意右边。",
    ],
    7: [
        # Guiding attention to the left: Using both hands to direct focus
        "请看左边。",
        "注意力往左边。",
        "向左看。",
        "请往左边看。",
        "注意左侧。",
        "把目光转向左边。",
        "请注意左边。",
        "请看向左侧。",
        "左边有重要的东西。",
        "请留意左边。",
    ],
    8: [
        # Guiding attention to the front: Using both hands to direct focus
        "请看前面。",
        "注意力往前面。",
        "向前看。",
        "请往前面看。",
        "注意前侧。",
        "把目光转向前面。",
        "请注意前面。",
        "请看向前侧。",
        "前面有重要的东西。",
        "请留意前面。",
    ],
    9: [
        # Pointing upwards with right hand: Directing attention with facial orientation
        "请看上面的选项。",
        "请看上面这点。",
        "我们集中注意力在上面这点。",
        "请注意上面的这个细节。",
        "请看上面这个部分。",
        "请把目光转向上面的这个点。",
        "请留意上面的这一点。",
        "请看向上面的这个位置。",
        "上面的这个点很重要。",
        "请把注意力集中在上面这个小点上。",
    ],
    10: [
        # Pointing to the right with right hand: Directing attention with facial orientation
        "请看右边选项。",
        "请看右边这点。",
        "我们集中注意力在右边这点。",
        "请注意右边的这个细节。",
        "请看右边这个部分。",
        "请把目光转向右边的这个点。",
        "请留意右边的这一点。",
        "请看向右侧的这个位置。",
        "右边的这个点很重要。",
        "请把注意力集中在右边这个小点上。",
    ],
    11: [
        # Pointing to the left with right hand: Directing attention with facial orientation
        "请看左边选项。",
        "请看左边这点。",
        "我们集中注意力在左边这点。",
        "请注意左边的这个细节。",
        "请看左边这个部分。",
        "请把目光转向左边的这个点。",
        "请留意左边的这一点。",
        "请看向左侧的这个位置。",
        "左边的这个点很重要。",
        "请把注意力集中在左边这个小点上。",
    ],
    12: [
        # Expressing confidence: "Leave it to me" gesture
        "交给我吧,包在我身上。",
        "别担心,我来处理。",
        "放心,我会处理的。",
        "我来解决这个问题,没问题的。",
        "交给我,保证完成。",
        "我来搞定,放心。",
        "这个问题交给我处理。",
        "我会负责到底。",
        "你就交给我吧,没问题。",
        "这件事交给我办。",
    ],
    13: [
        # Waving goodbye: Arm movement to say farewell
        "挥挥手",
        "再见。",
        "回见。",
        "期待下次再会。",
        "下次见。",
        "回头见。",
        "拜拜。",
        "保重。",
        "祝好。",
        "后会有期。",
        "祝你一切顺利。",
    ],
    14: [
        # Showing appreciation: Grateful gestures
        "感谢您的理解。",
        "我们非常重视您的意见。",
        "非常感谢您的合作。",
        "我们尊重您的贡献。",
        "能与您合作是我们的荣幸。",
        "感谢您的支持。",
        "我们感谢您的配合。",
        "我们非常感激您的投入。",
        "感谢您对我们的帮助。",
        "与您合作是我们的荣幸。",
    ],
    15: [
        # Clapping hands to praise: Expressing admiration
        "鼓掌",
        "拍手",
        "你真棒！",
        "太厉害了！！",
        "好强啊！",
        "你太牛了！",
        "真了不起！",
        "太精彩了！",
        "你表现得太好了！",
        "真是高手！",
        "太优秀了！",
        "你真是个天才！",
    ],
    16: [
        # Comforting gesture: Tapping head to reassure
        "摸摸头",
        "哎呀，没事的。",
        "你肯定没问题的。",
        "相信自己没事的。",
        "别担心，一切都会好起来的。",
        "放心吧，你能做到的。",
        "一切都会好起来的。",
        "没关系的，你可以的。",
        "别担心，事情会好转的。",
        "别担心，问题不大。",
        "你一定可以克服的。",
    ],
    17: [
        # Laughing expression: Showing amusement
        "大笑",
        "哈哈哈，太好笑了。",
        "你太搞笑了。",
        "这句话太好玩了。",
        "真是笑死我了！",
        "你简直是个笑星！",
        "这个笑话真是绝了。",
        "哈哈哈，笑得我肚子疼。",
        "你真会逗人笑。",
        "这个真是太有趣了！",
        "你真幽默！",
    ],
    18: [
        # Showing anger: Hand on waist to express fury
        "叉腰生气",
        "太生气了！",
        "你不要太不要脸！",
        "我好气啊！",
        "真是气死我了！",
        "你太过分了！",
        "我忍无可忍了！",
        "这简直不可原谅！",
        "你怎么可以这样！",
        "真是太气人了！",
        "我真的受够了！",
    ],
    19: [
        # Expressing confusion: Puzzled gestures
        "啊？为什么？",
        "这。。我该怎么办。。",
        "这是什么意思？",
        "这怎么回事？",
        "你在说什么？",
        "我不明白。",
        "这让我很困惑。",
        "怎么会这样？",
        "你能解释一下吗？",
        "这到底是怎么回事？",
    ],
    20: [
        # Countdown gesture: Showing 3, 2, 1 with fingers
        "数数",
        "倒计时",
        "三二一",
        "我还在查。",
        "给我多一点时间。",
        "我还在处理。",
        "再稍等一会儿。",
        "请耐心等待。",
        "我正在处理中。",
        "请再等一下。",
        "我正在解决这个问题。",
        "请稍候片刻。",
        "请再给我一点时间。",
    ],
    21: [
        # Showing number 1 with finger: Indicating first point
        "第一。",
        "首先。",
        "有一个重点。",
        "重要的是。",
        "需要特别注意的是。",
        "关键在于。",
        "必须指出的是。",
        "尤为重要的是。",
        "值得强调的是。",
        "重点在于。",
    ],
    22: [
        # Showing number 2 with fingers: Indicating second point
        "第二。",
        "其次。",
        "有两个点。",
        "再者。",
        "另外。",
        "还有一点。",
        "接下来。",
        "其次要注意的是。",
        "另一个重要的点是。",
        "第二个重点是。",
    ],
    23: [
        # Showing number 3 with fingers: Indicating third point
        "第三。",
        "还有一个点。",
        "总共有三个论点。",
        "最后一个要点。",
        "第三个方面是。",
        "再一个重要的点是。",
        "另外一个关键点。",
        "第三个论点是。",
        "还有一点需要提及。",
        "最后但同样重要的是。",
    ],
    24: [
        # Picking up phone: Starting order delivery
        "接电话",
        "开始预定饭店。",
        "开始与联络人通话。",
        "开始询问。",
        "开始预定会议室。",
        "打电话给联系人。",
        "开始询问价格。",
        "开始预定机票。",
        "与客户开始通话。",
        "开始询问可用性。",
        "开始预定活动场地。",
    ],
    25: [
        # Hanging up phone: Ending order delivery
        "挂电话",
        "结束预定饭店。",
        "结束与联络人通话。",
        "结束询问。",
        "完成预定会议室。",
        "结束与联系人的通话。",
        "完成询价。",
        "完成预定机票。",
        "结束与客户的通话。",
        "完成询问可用性。",
        "结束预定活动场地。",
    ],
    26: [
        # Talking on phone: Ordering delivery
        "打电话",
        "正在预定饭店。",
        "正在与联络人通话。",
        "正在询问。",
        "正在预定会议室。",
        "正在打电话给联系人。",
        "正在询问价格。",
        "正在预定机票。",
        "正在与客户通话。",
        "正在询问可用性。",
        "正在预定活动场地。",
    ],
    27: [
        # Waving hand palm to negate: Expressing disagreement
        "拒绝的手势",
        "恐怕那不太对。",
        "不幸的是，事实并非如此。",
        "让我们澄清一个常见的误解。",
        "实际上，那是一个常见的误解。",
        "不，那不准确。",
        "很遗憾，这是错误的。",
        "事实上，情况并非如此。",
        "让我纠正一下这个误解。",
        "恐怕你误解了这个点。",
        "对不起，但这并不正确。",
    ],
    28: [
        # Crossing arms to refuse: Expressing strong disagreement
        "我不同意。",
        "那不可能。",
        "不，谢谢。",
        "我宁愿不。",
        "不行。",
        "对不起，我不能同意。",
        "恐怕不行。",
        "我不能接受这个。",
        "我觉得不妥。",
        "这不符合我的意愿。",
    ],
    29: [
        # Shaking head to negate: Expressing disagreement with head movement
        "恐怕那不太对。",
        "不幸的是，事实并非如此。",
        "让我们澄清一个常见的误解。",
        "实际上，那是一个常见的误解。",
        "不，那不准确。",
        "很遗憾，这是错误的。",
        "事实上，情况并非如此。",
        "让我纠正一下这个误解。",
        "恐怕你误解了这个点。",
        "对不起，但这并不正确。",
    ],
    30: [
        # Holding umbrella: Indicating rainy weather
        "打伞的动作",
        "哎，现在正在下雨。",
        "天气预报显示现在在下雨。",
        "现在在下雨哦，别忘了带伞。",
        "外面正在下雨。",
        "下雨了，出门记得带伞。",
        "注意，现在外面有雨。",
        "现在正下着雨呢。",
        "外面开始下雨了。",
        "现在下雨了，小心不要淋湿。",
        "看来今天会有雨。",
    ],
    31: [
        # Hand against sun: Indicating hot weather
        "好热啊。",
        "今天天气很热，别中暑了哦。",
        "今天太阳很大，注意防晒呀。",
        "真热，感觉快要融化了。",
        "外面好热，记得多喝水。",
        "今天真是个大热天。",
        "炎热的天气，小心别晒伤了。",
        "这天气真是热得受不了。",
        "今天热得让人喘不过气。",
        "外面火辣辣的，记得防晒。",
    ],
    32: [
        # Coughing: Indicating cold weather or illness
        "好冷啊。",
        "今天天气很冷，别感冒了哦。",
        "太冷了，注意保暖哦。",
        "真冷，感觉像在冰箱里。",
        "外面好冷，记得多穿点。",
        "今天真是个寒冷的日子。",
        "寒冷的天气，小心别冻着了。",
        "这天气真是冷得刺骨。",
        "今天冷得让人发抖。",
        "外面寒风刺骨，记得保暖。",
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

    # 从actions_set中随机选择一个编号
    if action_index in actions_set:
        action_number = random.choice(actions_set[action_index])
        print("action_number___________", action_number)
        return jsonify({"action_number": action_number})
    else:
        return jsonify({"error": "Action index not found in actions_set"}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
