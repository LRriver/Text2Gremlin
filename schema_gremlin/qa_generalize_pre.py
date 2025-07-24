# main.py

import pandas as pd
import time
from itertools import islice

from gremlin_checker import check_gremlin_syntax
from llm_handler import generate_gremlin_variations, generate_texts_for_gremlin


INPUT_CSV_PATH = 'text2gremlin.csv'  # 种子qa数据
OUTPUT_CSV_PATH = 'test_augmented_text2gremlin.csv' # 输出路径
CHUNK_SIZE = 100 # 每次从CSV中读取的行数
GROUP_SIZE = 3 # 基于多少条相似数据去泛化


def save_new_data(new_data: list, is_first_batch: bool):
    """
    分批次将新生成的数据追加到输出文件中。
    """
    if not new_data:
        return
        
    df_new = pd.DataFrame(new_data)
    df_new.to_csv(
        OUTPUT_CSV_PATH, 
        mode='a', 
        header=is_first_batch, 
        index=False,
        encoding='utf-8-sig' 
    )
    print(f"Successfully saved {len(new_data)} new data pairs to {OUTPUT_CSV_PATH}")

def process_data_groups(df_groups):
    """
    处理分组后的数据，生成并返回新的数据对。
    """
    newly_generated_data = []
    
    for gremlin_query, group_df in df_groups:
        print("\n" + "="*80)
        print(f"Processing group for query: {gremlin_query}")
        
        # 种子数据
        seed_questions = group_df['question'].tolist()
        # 根据 GROUP_SIZE 参数截取，因为之前要求每条数据泛化几次
        seed_questions_subset = list(islice(seed_questions, GROUP_SIZE))

        # 生成新的gremlin
        print(f"Step 1: Calling LLM to generate Gremlin variations based on {len(seed_questions_subset)} questions...")
        candidate_queries = generate_gremlin_variations(gremlin_query, seed_questions_subset)
        if not candidate_queries:
            print("   -> LLM did not return Gremlin variations. Skipping group.")
            continue
        
        print(f"   -> LLM generated {len(candidate_queries)} candidate queries.")

        # AST语法检查
        valid_queries = []
        for query in candidate_queries:
            is_valid, msg = check_gremlin_syntax(query)
            if is_valid:
                valid_queries.append(query)
                print(f"   Syntax OK: {query}")
            else:
                print(f"   ❌ Syntax FAIL: {query} | Reason: {msg}")
        
        if not valid_queries:
            print("   -> No valid Gremlin queries after syntax check. Skipping group.")
            continue

        # 翻译+泛化
        print(f"Step 2: Generating text for {len(valid_queries)} valid queries...")
        for valid_query in valid_queries:
            generated_texts = generate_texts_for_gremlin(valid_query)
            if generated_texts:
                print(f"   -> Generated {len(generated_texts)} questions for: {valid_query}")
                for text in generated_texts:
                    newly_generated_data.append({'question': text, 'gremlin_query': valid_query})
            time.sleep(1) # 避免频率过高，服务端响应过慢

    return newly_generated_data


def main():
    is_first_write = True
    
    try:
        # 按照chunksize 分块读取CSV
        csv_reader = pd.read_csv(INPUT_CSV_PATH, chunksize=CHUNK_SIZE, iterator=True)
        
        for chunk_df in csv_reader:
            print("\n" + "#"*35 + f" Processing a new chunk of {len(chunk_df)} rows " + "#"*35)
            # 按 gremlin_query 分组
            grouped = chunk_df.groupby('gremlin_query')
            
            new_data_batch = process_data_groups(grouped)
            
            # 分批次保存，防止内存溢出
            if new_data_batch:
                save_new_data(new_data_batch, is_first_write)
                is_first_write = False

    except FileNotFoundError:
        print(f"Error: Input file not found at '{INPUT_CSV_PATH}'")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("\nQA泛化过程完成")


if __name__ == '__main__':
    main()