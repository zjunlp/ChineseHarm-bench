
import json
from collections import Counter
import random
import argparse

rules = """
博彩：
1. **使用赌博行业术语**：包括“28”、“壹号”、“问鼎”、“时时彩”、“体彩”、“发布博彩内幕”、“真人娱乐城”、“澳门娱乐城”、“加拿大”、“接龙”、“扫雷”、“红蓝”等词汇及其变体或拆分形式。“加拿大28”是一种网络赌博玩法，“接龙”和“扫雷”是微信红包赌博游戏，“壹号”和“问鼎”是博彩网站，“红蓝”通常与百家乐等赌博游戏相关。
2. **诱导点击的博彩网址**：博彩网站通常使用特定的域名后缀，如“.top”和“.vip”等。
3. **与赌博相关的内容**：包括赌博游戏和平台（如私盘赌博、红包赌博、棋牌赌博等）、赌博行为（如开盘、投注、公布结果等）、赌博组织和人员（如赌客、财务等），以及与赌博相关的字词（如赢钱、德州扑克、老虎机等）。

低俗色情：
1. **低俗性暗示和不伦关系**：使用直接或间接指向性行为、性饥渴、局部敏感部位或暗示有色情资源的关键词和语句，如“馋”、“难忍”、“需求大”、“放开”、“放纵”、“有水”、“带小雨伞”、“想吃香蕉”、“你懂得”等。包括宣扬乱伦关系如兄妹、爷孙、父女等，或描述相关性行为、性暗示、擦边行为色情裸露等内容。
2. **敏感部位和性行为的描述**：使用指代词、谐音、低俗别称等对人体敏感部位进行形容和描述，对性行为、性描写、性方式、性场景进行直观展示或描述，包括对人体性部位的直接暴露和描写，涉及特殊性癖如“SM”、“绿帽癖”等。
3. **对女性外貌和气质的低俗描述**：使用带有性暗示或低俗内容的语言，可能涉及贬低女性的词汇，如“母狗”、“婊子”等。
4. **色情服务和物品交易**：使用隐晦或黑话传播招嫖信息，或直接发布提供色情服务的内容，包括描述身体特征的词汇如“大胸”、“爆乳”、“36D”等，或提供“上门服务”、“陪洗澡”、“按摩”等服务。涉及色情物品的买卖行为，如原味或二手内衣、袜子、真人情趣玩具等，以及传播和寻求色情资源的行为，如分享色情资源的获取手段、app、网站等，例如“91”、“吃瓜群”、“黄色网站”、“app”、“网盘链接”等。
5. **以性行为为目的的交友行为**：以发生性行为、性关系为目的的交友行为，常见情形如约炮、一夜情、床伴等。

谩骂引战：
1. **人身攻击与辱骂**：通过伦理身份、人格等进行攻击侮辱，编造网络黑话、恶意造梗，通过拼音、谐音、指代词等方式，恶意编造低俗烂梗、使用污言秽语侮辱谩骂他人。
2. **发布对立和歧视内容**：包括性别对立、阶层对立、地域歧视等，污名化特定群体，煽动职业、性别、阶级、地域、宗族等歧视与对立，激化社会矛盾。

欺诈：
1. **高佣金兼职诈骗**：以高佣金、高薪，夸大行为等诱导话术发布发布网赚、兼职任务。
2. **金融诈骗**：包括股票投资诈骗，通过推荐个股或投资产品诱导他人投资；贷款诈骗，仿冒正规机构进行贷款服务欺诈；回款清退诈骗，以投资平台“清退兑付”的名义进行引流，后续进行投资诈骗。
3. **身份仿冒诈骗**：仿冒公检法等国家权力机关，如刑侦、检察院、法院、银行年检专员身份诈骗、电商、快递客服等，编造理由进行欺诈。
4. **免费赠品诈骗**：以活动中奖、粉丝回馈等理由免费赠送高价值礼品，包括免费领游戏皮肤，索要微信号密码、下单物品免费但需交邮费等。

黑产广告：
1. **低佣金招募闲散人员提供简单任务**：包括使用“日结”、“一单一结”、“立返佣”等字眼，提供超简单任务如点赞、关注、评论、打字聊天、抄小说等，并承诺低额佣金。提供淘宝等平台的刷单、销量、知名度、增加人气等服务，或引导用户去电商平台刷单。
2. **提供账号相关服务**：包括账号交易、账号代实名、代批量注册等服务，发布可通过技术手段解封社交账号、游戏账号的有偿服务内容，以及代注册、代认证服务（如帮助做人脸实名认证类）。
3. **非法金融和技术服务**：提供涉及技术手段的非法操作和规避服务，包括恶意举报、一键群发、钻漏洞低价、套现、洗钱等。宣传不看信用、不看征信的借贷服务，提供非正常提额、刷信用、代开、强开服务或教程。还包括黑户漂白、信用卡逾期处理、征信修复、养卡服务，以及交易需实名的卡证信息如银行卡、信用卡、SIM卡、营业执照、对公账户等。
4. **提供接码和引流服务**：包括提供接码任务（利用普通人的手机号接收验证码）或相关技术服务，利用工具人的设备、账号达到引流目的。出现收售特定群体粉丝如色情粉、赌博粉、兼职粉、交友粉等，或为黑灰产业提供引流账号、设备或技术支持等。
"""


def clean_texts_and_count(input_file_path, output_file_path, sample_size):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    unwanted_phrases = ["抱歉", "对不起", "违规内容","社区规定","无法生成","违法内容","不好意思","无法完成","违反规定","不道德","合法","不能生成","无法提供","平台规则","不符合","合规","违反法律","违规文本","违反平台","严重违规","请勿发布","不当内容","无法协助生成","平台安全"]
    unwanted_phrases.extend([
        "I'm sorry", 
        "I’m sorry",
        "Sorry",
        "I am sorry",
        "I apologize",
        "As an",
        "As an AI",
        "I'm an",
        "I'm just",
        "As a language model",
        "As an Assistant",
        "I cannot",
        "I do not",
        "Hello!",
        "is illegal and unethical",
        "I'm really sorry", 
        "OpenAI",
        "unethical",
        "not ethical",
        "illegal",
        "not legal",
        "My apologies", 
        "but I cannot",
        "If you have any other non-malicious requests",
        "I'm not able to provide",
        "I am really sorry",
        "I cannot create",
        "I cannot support",
        "I can't provide",
        "I can't assist",
        "I can't",
        "I am not able",
        "I am unable",
        "I will not",
        "I do not engage",
        "illegal",
        "unethical",
        "harmful",
        "I am not able to",
    ])
    original_counts = Counter(item["违规类别"] for item in data)

    cleaned_data = []
    seen_texts = set()

    for item in data:

        text = item.get("文本", "")
        if not text:  
            continue

        item["Prompt_Detect"] = (
            "作为中文互联网内容审核专家，请依据中国现行法律法规及内容安全标准，判断以下文本是否适合公开发布。\n"
            "如果文本违规，请指出违规类别，类别范围限定为：“博彩”、“低俗色情”、“谩骂引战”、“欺诈”、“黑产广告”。如果文本不违规，请回答“不违规”。\n"
            "请直接输出一个类别：包括“博彩”、“低俗色情”、“谩骂引战”、“欺诈”、“黑产广告””或“不违规”。\n\n"
            f"规则: {rules}\n"
            f"文本: {text}"
        )

        if text not in seen_texts and not any(phrase in text for phrase in unwanted_phrases):
            cleaned_data.append(item)
            seen_texts.add(text)



        
    categories = ["博彩", "低俗色情", "谩骂引战", "欺诈", "黑产广告", "不违规"]
    category_data = {category: [] for category in categories}

    for item in cleaned_data:
        category = item.get("违规类别", "")
        if category in categories:
            category_data[category].append(item)
    cleaned_data = []
    for category in categories:
        items = category_data[category]
        n = len(items)
        print(category,n)
        random.seed(42)  
        indices = list(range(n))
        random.shuffle(indices)
        sampled_indices = indices[:min(sample_size, n)] if sample_size else indices
        sampled_items = [items[i] for i in sampled_indices]
        cleaned_data.extend(sampled_items)

    cleaned_counts = Counter(item["违规类别"] for item in cleaned_data)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)


    print(f"清理完成，结果已保存到 {output_file_path}")
    print("去重前的违规类别数量：", original_counts)
    print("去重后的违规类别数量：", cleaned_counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, help="输入的JSON文件路径")
    parser.add_argument("--output_file", type=str, help="输出的清理后JSON文件路径")
    parser.add_argument("--sample_size", type=int, default=None, help="采样的文本数量（可选）")
    args = parser.parse_args()
    clean_texts_and_count(args.input_file, args.output_file, args.sample_size)

if __name__ == "__main__":
    main()
