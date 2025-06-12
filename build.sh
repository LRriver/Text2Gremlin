# 自定义ANTLR4 jar 文件的路径
ANTLR_JAR_PATH="./gremlin/antlr-4.13.1-complete.jar" 

if [ ! -f "$ANTLR_JAR_PATH" ]; then
    echo "ANTLR jar file not found at $ANTLR_JAR_PATH"
    echo "Please download antlr-4.13.1-complete.jar and update ANTLR_JAR_PATH in this script."
    exit 1
fi

# 3. 自定义 Gremlin.g4 文件的路径
GRAMMAR_FILE="./gremlin/Gremlin.g4"

if [ ! -f "$GRAMMAR_FILE" ]; then
    echo "Grammar file $GRAMMAR_FILE not found."
    exit 1
fi

# 执行 ANTLR4 工具生成 Python 代码
echo "Generating ANTLR4 Python parser for Gremlin..."
java -jar "$ANTLR_JAR_PATH" -Dlanguage=Python3 -visitor "$GRAMMAR_FILE"
if [ $? -ne 0 ]; then
    echo "ANTLR4 code generation failed. Check Java installation and ANTLR jar path."
    exit 1
fi

echo "ANTLR4 code generation successful."
echo "Generated files should be in the current directory: $(pwd)"
ls -l Gremlin*.py 