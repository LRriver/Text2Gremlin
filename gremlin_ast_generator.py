import sys
import random
from antlr4 import *
from antlr4.tree.Tree import TerminalNode
sys.path.insert(0, './gremlin')

from gremlin.GremlinLexer import GremlinLexer
from gremlin.GremlinParser import GremlinParser
from gremlin.GremlinVisitor import GremlinVisitor

REPLACEMENT_MAP = {
    'keys': {
        'name': 'person_name',
        'userId': 'person_id',
        'age': 'person_age'
    },
    'values': {
        'person_name': ["'Bob'", "'Charlie'", "'David'", "'Eve'"],
        'person_id': ["'user123'", "'user456'", "'user789'"],
        'person_age': [30, 40, 50]
    },
    'steps': {
        'out': 'in',
        'in': 'out'
    }
}

# 重构Visitor，修改AST结构
class GremlinTransformVisitor(GremlinVisitor):
    
    def visitTraversalMethod_out(self, ctx:GremlinParser.TraversalMethod_outContext):
        method_name = 'out'
        if method_name in REPLACEMENT_MAP['steps']:
            new_method = REPLACEMENT_MAP['steps'][method_name]
            print(f"步骤替换: {method_name} -> {new_method} ")
            
            arguments = self.visit(ctx.getChild(2)) if ctx.getChildCount() > 3 else ""
            return f"{new_method}({arguments})"
        return self.visitChildren(ctx)

    def visitTraversalMethod_in(self, ctx:GremlinParser.TraversalMethod_inContext):
        method_name = 'in'
        if method_name in REPLACEMENT_MAP['steps']:
            new_method = REPLACEMENT_MAP['steps'][method_name]
            print(f"步骤替换: {method_name} -> {new_method} ")
            
            arguments = self.visit(ctx.getChild(2)) if ctx.getChildCount() > 3 else ""
            return f"{new_method}({arguments})"
        return self.visitChildren(ctx)


    def visitTraversalMethod_has_String_Object(self, ctx:GremlinParser.TraversalMethod_has_String_ObjectContext):
        original_key_node = ctx.getChild(2)
        original_value_node = ctx.getChild(4)
        
        original_key = original_key_node.getText().strip("'")
        
        # --- 替换键 (Key) ---
        available_keys = list(REPLACEMENT_MAP['keys'].keys())
        
        # 提高替换率，防止重复率高
        if random.random() < 0.5 and original_key in available_keys:
            other_keys = [k for k in available_keys if k != original_key]
            if other_keys:
                new_key = random.choice(other_keys)
                print(f" 键替换: {original_key} -> {new_key}")
            else:
                new_key = original_key # 没有其他键可选，保持原样
        else:
            new_key = original_key
            
        # 替换Value
        original_value = original_value_node.getText()
        value_type = REPLACEMENT_MAP['keys'].get(new_key)
        
        # 尽量使得替换后的新值与旧值不同
        if value_type and value_type in REPLACEMENT_MAP['values']:
            possible_new_values = REPLACEMENT_MAP['values'][value_type]

            other_values = [v for v in possible_new_values if v != original_value]
            if other_values:
                new_value = random.choice(other_values)
            else:
                new_value = random.choice(possible_new_values) # 所有可选值都一样，任选一个
            
            print(f"替换了'{new_key}'属性值: {original_value} -> {new_value} ")
        else:
            new_value = original_value
            
        return f"has('{new_key}', {new_value})"
    # 拼接
    def visitTerminal(self, node: TerminalNode):
        return node.getText()

    def defaultResult(self):
        return ""

    def aggregateResult(self, aggregate, nextResult):
        if not aggregate: return nextResult
        if not nextResult: return aggregate
        return aggregate + nextResult


def main():
    input_gremlin = "g.V().has('name', 'Alice').out('knows').values('age')"
    print(f"原始 Gremlin 语句:\n{input_gremlin}\n")

    input_stream = InputStream(input_gremlin)
    lexer = GremlinLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = GremlinParser(stream)
    tree = parser.query()

    visitor = GremlinTransformVisitor()
    transformed_query = visitor.visit(tree)

    print(f"\n转换后的 Gremlin 语句:\n{transformed_query}")


if __name__ == '__main__':
    main()