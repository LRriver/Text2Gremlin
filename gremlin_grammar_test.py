import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, './gremlin')

from gremlin.GremlinLexer import GremlinLexer
from gremlin.GremlinParser import GremlinParser

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """打印详细错误信息"""
        error_message = f"语法错误在 -> 行: {line}, 列: {column} | 消息: {msg}"
        self.errors.append(error_message)

    @property
    def has_errors(self):
        """判断是否发生了错误"""
        return len(self.errors) > 0


def check_gremlin_syntax(query_string):
    """
    检查给定的Gremlin查询字符串的语法。
    """
    print(f"--- 正在检查查询: \"{query_string}\" ---")
    
    input_stream = InputStream(query_string)
    lexer = GremlinLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GremlinParser(token_stream)


    parser.removeErrorListeners()
  
    error_listener = SyntaxErrorListener()
    parser.addErrorListener(error_listener)

    tree = parser.queryList()

    if error_listener.has_errors:
        print("结果: 查询存在语法错误！")
        for error in error_listener.errors:
            print(f"  - {error}")
        return False
    else:
        print("结果: 语法正确")
        # print("\n query的AST:")
        # print(tree.toStringTree(recog=parser))
        return True


def main():
    # 语法正确的查询
    correct_query = "g.V().has('person','name','marko').out('knows')"
    check_gremlin_syntax(correct_query)

    print("\n" + "="*50 + "\n")

    # 语法错误的查询 (SELECT错了)
    incorrect_query = "g.V().SELECT('name')"
    check_gremlin_syntax(incorrect_query)

if __name__ == '__main__':
    main()