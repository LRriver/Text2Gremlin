import sys
import random
from antlr4 import *

sys.path.insert(0, './gremlin')

from gremlin.GremlinLexer import GremlinLexer
from gremlin.GremlinParser import GremlinParser
from gremlin.GremlinVisitor import GremlinVisitor

class GremlinCorrectAnalyzer(GremlinVisitor):
    """
    从AST中提取出方法名。
    """
    def __init__(self):
        self.steps = []

    def visitTraversalSourceSpawnMethod(self, ctx: GremlinParser.TraversalSourceSpawnMethodContext):
        # 提取起始步骤的方法名, 例如 'V'
        method_name = ctx.getChild(0).getChild(0).getText()
        self.steps.append(method_name)
        return self.visitChildren(ctx)

    def visitTraversalMethod(self, ctx: GremlinParser.TraversalMethodContext):
        # 提取链式步骤的方法名, 例如 'has', 'out'
        method_name = ctx.getChild(0).getChild(0).getText()
        self.steps.append(method_name)
        return self.visitChildren(ctx)

    def get_analysis(self, tree):
        """分析入口，并根据步骤列表判断查询类型"""
        self.visit(tree)
        query_type = "unknown"
        # 如果查询以V().has()开头，给一个特定的类型
        if len(self.steps) >= 2 and self.steps[0] == 'V' and self.steps[1] == 'has':
            query_type = "vertex_has_query"
        return query_type, self.steps


class GremlinQueryBuilder:
    """
    构建Gremlin查询。
    """
    def __init__(self, g_var='g'):
        self.steps = []
        self.g_var = g_var

    def add_step(self, method, *args):
        str_args = []
        for arg in args:
            if isinstance(arg, str):
                str_args.append(f"'{arg}'")
            else:
                str_args.append(str(arg))
        
        self.steps.append({"method": method, "args": ", ".join(str_args)})
        return self

    def build(self):
        if not self.steps:
            return ""
        
        first_step = self.steps[0]
        query = f"{self.g_var}.{first_step['method']}({first_step['args']})"
        
        for step in self.steps[1:]:
            query += f".{step['method']}({step['args']})"
            
        return query

def main():
    
    gremlin_query = "g.V().has('person','name','marko')"
    print(f"原始查询: {gremlin_query}\n")

    # AST
    input_stream = InputStream(gremlin_query)
    lexer = GremlinLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GremlinParser(token_stream)
    tree = parser.queryList()


    analyzer = GremlinCorrectAnalyzer()
    query_type, steps = analyzer.get_analysis(tree)
    print(f"分析结果: 类型='{query_type}', 步骤={steps}")

    RULE_LIBRARY = {
        "vertex_has_query": {
            "description": "从“查找特定顶点”转换为“按属性分组计数”",
            "build_logic": "group_count_by_property"
        }
    }
    DATASET = {
        "labels": ["person", "software"],
        "group_by_properties": ["age", "lang"]
    }

    new_query = ""
    if query_type in RULE_LIBRARY:
        rule = RULE_LIBRARY[query_type]
        print(f"匹配成功,转换规则: '{rule['description']}'")
        
        if rule['build_logic'] == 'group_count_by_property':
        
            label = random.choice(DATASET['labels'])
            prop = random.choice(DATASET['group_by_properties'])
            
            # 使用构造器搭建新查询
            builder = GremlinQueryBuilder()
            builder.add_step("V") \
                   .add_step("hasLabel", label) \
                   .add_step("groupCount") \
                   .add_step("by", prop)
            
            new_query = builder.build()

    print("\n" + "="*50)
    print("生成的新查询:")
    print(new_query)


if __name__ == '__main__':
    main()