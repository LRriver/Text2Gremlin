# Text2Gremlin
中文 | [English](./README.md)

本项目旨在探索从自然语言文本生成 Gremlin 查询语句的方法，并验证其可行性。

## 环境准备

### Python 环境
请确保已安装 Python 及 pip，并运行以下命令安装依赖：
```bash
pip install -r requirements.txt
```

### Antlr4 环境
Gremlin 相关的语法文件已经使用 ANTLR4 处理完成，位于 `./gremlin` 路径下，可直接调用相关文件。若你想处理自己的 `.g4` 语法文件，请先安装 JDK 和 ANTLR4：

```bash
# 更新软件包列表
sudo apt update

# 安装 OpenJDK 21
sudo apt install openjdk-21-jdk

# 验证是否安装成功
java -version
javac -version
```

ANTLR4 的 jar 包（`antlr-4.13.1-complete.jar`）已下载并放在 `./gremlin` 目录中，可直接使用。

之后运行 `build.sh` 脚本即可使用 ANTLR4 处理 `.g4` 文件，生成相应的解析器代码：

```bash
cd Text2Gremlin
sh ./build.sh
```

## 第一阶段: 基于AST的Text2Gremlin测试
此阶段仅基于AST测试Text2Gremlin的实现，无实际实现意义

### AST生成
```bash
python ./gremlin_ast_gen.py
```

### 使用AST进行语法检查
```bash
python ./gremlin_grammar_test.py
```

### 修改AST并生成新的Gremlin查询
```bash
python ./gremlin_ast_generator.py
```
## 第二阶段: 基于LLM的垂类场景Text2Gremlin数据增强

相关代码位于[`./schema_gremlin`](./schema_gremlin/)