import sys
from antlr4 import *

sys.path.insert(0, './gremlin')
from gremlin.GremlinLexer import GremlinLexer
from gremlin.GremlinParser import GremlinParser
from gremlin.GremlinVisitor import GremlinVisitor




class GremlinCorrectAnalyzer(GremlinVisitor):
    """
    这个Visitor现在能正确地从AST中提取出方法名。
    """
    def __init__(self):
        self.steps = []

    def visitTraversalSourceSpawnMethod(self, ctx: GremlinParser.TraversalSourceSpawnMethodContext):
        method_name = ctx.getChild(0).getChild(0).getText()
        self.steps.append(method_name)
        return self.visitChildren(ctx)

    def visitTraversalMethod(self, ctx: GremlinParser.TraversalMethodContext):
        method_name = ctx.getChild(0).getChild(0).getText()
        self.steps.append(method_name)
        return self.visitChildren(ctx)


def main():
    gremlin_query = "g.V().has('person','name','marko').out('knows')"
    print(f"--- Analyzing Gremlin Query ---\nQuery: \"{gremlin_query}\"\n")

    # 解析得到AST
    input_stream = InputStream(gremlin_query)
    lexer = GremlinLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GremlinParser(token_stream)
    
    tree = parser.queryList()
    print("AST of Gremlin Query:",tree.toStringTree(recog=parser))
    # Visitor遍历AST
    visitor = GremlinCorrectAnalyzer()
    visitor.visit(tree) 
    print(f"Correctly extracted steps: {visitor.steps}")
    
    
    query_type = "unknown"
    if len(visitor.steps) >= 2 and visitor.steps[0] == 'V' and visitor.steps[1] == 'has':
        query_type = "vertex_has_query"
    
    print(f"Determined query type: {query_type}")


if __name__ == '__main__':
    main()