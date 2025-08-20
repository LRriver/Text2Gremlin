import re
import json
from collections import defaultdict

def create_structured_knowledge(file_path):
    """
    从 ANTLR v4 (.g4) 文件中稳健地提取规则，严格按照文件内的章节头进行分类，
    并进行语义成组，生成最终的结构化知识库
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"成功读取文件 '{file_path}'")
    except FileNotFoundError:
        print(f"无法找到文件 {file_path}")
        return {}

    # 定位主要章节的起始位置
    section_pattern = re.compile(r'/\*+[\s\n]+([\w\s]+)[\s\n]+\*+/', re.DOTALL)
    sections = []
    for match in section_pattern.finditer(content):
        section_name = match.group(1).strip()
        sections.append({"name": section_name, "start_pos": match.end()})

    if not sections:
        print("错误：未在文件中找到任何 /****...****/ 格式的章节头。")
        return {}
        
    sections.sort(key=lambda x: x['start_pos'])
    print(f"定位到 {len(sections)} 个主要章节框架: {[s['name'] for s in sections]}")

    rule_pattern = re.compile(
        r'((?:\s*(?:/\*.*?\*/|//[^\n]*)\s*)*)'  # 可选的前置注释
        r'((?:fragment\s+))?'                  # 可选的'fragment '关键字(现在是捕获组)
        r'([a-zA-Z_]\w*)'                      # 规则名称
        r'\s*:\s*'                             # 匹配冒号
        r'(.*?);',                             # 规则体(非贪婪匹配)
        re.DOTALL
    )
    
    all_found_rules = []
    for match in rule_pattern.finditer(content):
        groups = match.groups()
        
        comment = groups[0]
        is_fragment = bool(groups[1]) 
        rule_name = groups[2]
        rule_body = groups[3]
        
        rule_start_pos = match.start()
        assigned_section = "Uncategorized"
        for i in range(len(sections)):
            if i + 1 < len(sections):
                if sections[i]['start_pos'] <= rule_start_pos < sections[i+1]['start_pos']:
                    assigned_section = sections[i]['name']
                    break
            else:
                if rule_start_pos >= sections[i]['start_pos']:
                    assigned_section = sections[i]['name']
                    break
        
        all_found_rules.append({
            "rule_name": rule_name,
            "rule_body": ' '.join(rule_body.strip().split()),
            "comment": ' '.join(comment.strip().split()),
            "section": assigned_section,
            "is_fragment": is_fragment
        })
        
    print(f"✅ 阶段一：完成原子规则提取，共找到 {len(all_found_rules)} 条规则。")

    #按物理章节进行分类
    categorized_rules = defaultdict(list)
    for rule in all_found_rules:
        category_key = rule['section']
        # 将 fragment 规则作为 LEXER RULES 的一部分，如果它物理上在那里
        # 暂不做特殊处理，让它按章节走
        categorized_rules[category_key].append(rule)
    print(f"✅ 阶段二：规则已严格按物理章节分类。")


    # 将原子规则聚合成语义组
    print("⏳ 阶段三：开始进行语义成组...")
    structured_knowledge_base = {}
    for category, rules in categorized_rules.items():
        if category == "Uncategorized": continue

        grouped_rules = []
        i = 0
        while i < len(rules):
            current_rule = rules[i]
            prefix_parts = current_rule['rule_name'].split('_')
            
            if len(prefix_parts) > 1:
                prefix = '_'.join(prefix_parts[:-1])
                group_name = f"{prefix}_family"
                current_group = {"group_name": group_name, "rules": [current_rule]}
                
                j = i + 1
                while j < len(rules) and '_'.join(rules[j]['rule_name'].split('_')[:-1]) == prefix:
                    current_group["rules"].append(rules[j])
                    j += 1
                
                grouped_rules.append(current_group)
                i = j
            else:
                grouped_rules.append({"group_name": current_rule['rule_name'], "rules": [current_rule]})
                i += 1
        
        structured_knowledge_base[category] = grouped_rules

    print(f"✅ 阶段三：语义成组完成。")
    return structured_knowledge_base


input_g4_file = 'Gremlin.g4' 
output_json_file = 'structured_gremlin_grammar.json'

knowledge_base = create_structured_knowledge(input_g4_file)

if knowledge_base:
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    print(f"结构化知识库已成功保存到 '{output_json_file}'")
    
    print("\n--- 知识库部分结果 ---")
    for category, groups in knowledge_base.items():
        print(f"  📖 章节 '{category}': 包含 {len(groups)} 个语义组。")