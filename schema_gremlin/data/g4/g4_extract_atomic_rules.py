import re
import json

def extract_grammar_rules(file_path):
    """
    从 ANTLR v4 (.g4) 语法文件中提取所有独立的语法规则，并将其结构化。

    Args:
        file_path (str): .g4 文件的路径。

    Returns:
        list[dict]: 一个包含所有提取规则的列表。每个规则是一个字典，
                    格式为 {"rule_name": "...", "rule_body": "..."}。
        如果失败则返回空列表。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"成功读取文件: {file_path}")
    except FileNotFoundError:
        print(f"错误：无法找到文件 {file_path}")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []

    # 移除块注释 /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # 移除行注释 // ...
    content = re.sub(r'//.*', '', content)

    # 正则表达式匹配
    # (fragment)? : 匹配可选的 'fragment' 关键字
    # ([a-zA-Z_]\w*) : 匹配规则名 (大小写字母或下划线开头)
    # \s*:\s* : 匹配冒号
    # (.*?) : 非贪婪匹配规则体
    # ; : 匹配规则结束的分号
    rule_pattern = re.compile(
        r'^\s*(?:fragment\s+)?([a-zA-Z_]\w*)\s*:\s*(.*?);',
        re.MULTILINE | re.DOTALL
    )

    matches = rule_pattern.findall(content)
    
    extracted_rules = []
    for rule_name, rule_body in matches:
        # 清理规则主体中的多余空白和换行符
        cleaned_body = ' '.join(rule_body.strip().split())
        
        rule_data = {
            "rule_name": rule_name,
            "rule_body": cleaned_body
        }
        extracted_rules.append(rule_data)
    
    print(f"成功提取了 {len(extracted_rules)} 条语法规则。")
    return extracted_rules

def save_rules_to_json(rules, output_path):
    """
    Args:
        rules (list): 提取出的规则列表。
        output_path (str): 输出的 JSON 文件路径。
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        print(f"所有语法知识点已成功保存到: {output_path}")
    except Exception as e:
        print(f"保存文件时发生错误: {e}")

input_g4_file = 'Gremlin.g4'
output_json_file = 'gremlin_grammar_points.json'

grammar_points = extract_grammar_rules(input_g4_file)

if grammar_points:
    save_rules_to_json(grammar_points, output_json_file)

    # print("\n--- 部分提取结果 ---")
    # for point in grammar_points[:5]:
    #     print(json.dumps(point, indent=2, ensure_ascii=False))