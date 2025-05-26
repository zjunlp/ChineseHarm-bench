import json
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse



class ChatProxy(object):
    def __init__(self, base_url, api_key):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def chat(self, message: str):
        response = self.client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            max_tokens=1024,
            temperature=1,
            top_p=1
        )

        return response

def process_item(proxy, idx, x, wait_time=5):
    while True:
        try:
            message = x['prompt']
            response = proxy.chat(message)
            x["文本"]=response.choices[0].message.content

            return (idx, x, None)
        except Exception as e:
                error_message = str(e)
                print(error_message)
                if "限流" in error_message or "rate limit" in error_message or "Error" in error_message :
                    time.sleep(wait_time)
                else:
                    return (idx, None, error_message)


def main():

    parser = argparse.ArgumentParser(description="批量处理文本并调用API")
    parser.add_argument("--base_url", type=str, required=True, help="OpenAI API 的基础 URL")
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API 的密钥")
    parser.add_argument("--input_file", type=str, required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output_file", type=str, required=True, help="输出 JSON 文件路径")
    parser.add_argument("--max_workers", type=int, default=1000, help="最大并发线程数")
    args = parser.parse_args()

    proxy = ChatProxy(base_url=args.base_url, api_key=args.api_key)
    
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = [None] * len(data)


    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = []
        for idx, x in enumerate(data):
            futures.append(executor.submit(process_item, proxy, idx, x))
        
        for future in tqdm(as_completed(futures), total=len(futures)):
            idx, result, error = future.result()
            if error:
                print(f"Error processing item {idx}: {error}")
                results[idx] = data[idx]  
            else:
                results[idx] = result

    with open(args.output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
