# Experiment-Text2Gremlin
[English] | [中文](./README_zn.md)

This project aims to explore the method of generating Gremlin queries from natural language text and verify its feasibility.


## Environment Setup

### Python Environment
Make sure you have Python and pip installed, then run:
```bash
pip install -r requirements.txt
```

### ANTLR4 Environment
The Gremlin-related grammar files have already been processed using ANTLR4 and are located in the `./gremlin` directory. You can directly use them. If you want to process your own `.g4` grammar files, you need to install JDK and ANTLR4:

```bash
# Update package list
sudo apt update

# Install OpenJDK 21
sudo apt install openjdk-21-jdk

# Verify installation
java -version
javac -version
```

The ANTLR4 JAR file (`antlr-4.13.1-complete.jar`) has already been downloaded and is located in the `./gremlin` directory.

After that, run the `build.sh` script to process `.g4` files with ANTLR4 and generate parser code:
```bash
cd Experiment-Text2Gremlin
sh ./build.sh
```

## Running Scripts

### AST Generation
```bash
python ./gremlin_ast_gen.py
```

### Syntax Checking Using AST
```bash
python ./gremlin_grammar_test.py
```

### Modifying AST and Generating New Gremlin Queries
```bash
python ./gremlin_ast_generator.py
```