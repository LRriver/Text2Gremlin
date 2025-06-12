# pip install antlr4-python3-runtime==4.13.1
# antlr4 -Dlanguage=Python3 -visitor /root/lzj/ospp/Gremlin_Antlr4/Gremlin.g4
#!/bin/bash

# 1. 安装 ANTLR4 Python 运行时库
echo "Installing ANTLR4 Python3 runtime..."
pip install antlr4-python3-runtime==4.13.1
if [ $? -ne 0 ]; then
    echo "Failed to install antlr4-python3-runtime. Please check pip and network."
    exit 1
fi

# 2. 定义 ANTLR4 jar 文件的路径
#    修改下面的路径为您实际存放 antlr-4.13.1-complete.jar 的位置
ANTLR_JAR_PATH="/root/lzj/ospp/Gremlin_Antlr4/antlr-4.13.1-complete.jar" 

# 检查 ANTLR jar 文件是否存在
if [ ! -f "$ANTLR_JAR_PATH" ]; then
    echo "ANTLR jar file not found at $ANTLR_JAR_PATH"
    echo "Please download antlr-4.13.1-complete.jar and update ANTLR_JAR_PATH in this script."
    exit 1
fi

# 3. 定义 Gremlin.g4 文件的完整路径
GRAMMAR_FILE="/root/lzj/ospp/Gremlin_Antlr4/Gremlin.g4"

# 检查 .g4 文件是否存在
if [ ! -f "$GRAMMAR_FILE" ]; then
    echo "Grammar file $GRAMMAR_FILE not found."
    exit 1
fi

# 4. 执行 ANTLR4 工具生成 Python 代码
echo "Generating ANTLR4 Python parser for Gremlin..."
java -jar "$ANTLR_JAR_PATH" -Dlanguage=Python3 -visitor "$GRAMMAR_FILE"
if [ $? -ne 0 ]; then
    echo "ANTLR4 code generation failed. Check Java installation and ANTLR jar path."
    exit 1
fi

echo "ANTLR4 code generation successful."
echo "Generated files should be in the current directory: $(pwd)"
ls -l Gremlin*.py # 列出生成的 Python 文件