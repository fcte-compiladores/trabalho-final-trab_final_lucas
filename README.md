# Interpretador Micro-C em Python

**Integrante**: Lucas Chaves Itacaramby - 231026456 - Turma 02

## Micro-C

* `Micro-C` é um **subconjunto** da `linguagem padrão C`, funcionando como uma versão simplificada da mesma.
  * A linguagem inclue:
    * tipos de dados `int`, `bool` e `void`
    * **declaração de variáveis** (`int x;`)
    * **inicialização de variáveis** (`int x = 5;`)
    * **variáveis globais** (variáveis criadas fora de funções)
    * operadores **Aritméticos** (`+`, `-`, `*`, `/`), **Relacionais** (`<`, `>`, `<=`, `>=`, `==` `!=`), e **Lógicos** (`&&`, `||`, `!`)
    * estruturas **Condicionais** (`if`/`else`), **Loops** (`while`) e **Funções**
* Acesse a gramática de `Micro-C` utilizada no projeto pelo link abaixo
  * Aqui a gramática `Micro-C` -> [click here!](MicroC/grammar.lark)

## Instalacão

* certifique-se de baixar os pré-requisitos!
    ```bash
    // primeiro Instale o uv
    pip install uv
    // por ultimo baixe as dependencias
    uv run MicroC

    // após isso, para executar o interpretador use
    uv run MicroC nome_do_arquivo.mc
    ```

* caso queira mais informações na execução do código, utilize:
    ```bash
    uv run MicroC nome_do_arquivo.mc // execução padrão
    uv run MicroC -c nome_do_arquivo.mc // árvore sintática concreta (cst)
    uv run MicroC -t nome_do_arquivo.mc // árvore sintática abstrata (ast)
    ```

## Exemplos

* a pasta `exemplos` possui cerca de 5 arquivos `.mc` na linguagem de programação implementada
    ```bash
    exemplos
    ├── fun_escopo.mc
    ├── fun_example.mc
    ├── if.mc
    ├── var_global.mc
    ├── while.mc
    ```

## Referências usadas no Projeto

* **documentação do Lark**: a biblioteca Lark foi fundamental para a implementação do analisador léxico e sintático. A documentação oficial foi usada para aprender sobre definição de gramáticas, criação de transformadores e manipulação de árvores sintáticas

* **material didático da disciplina**: o código do interpretador lox para python utilizado durante a matéria serviu de base para a estrutura geral do interpretador, especialmente na separação das etapas de análise e execução

* **projetos open-source similares**: foram consultados repositórios públicos de interpretadores de linguagens simples em Python para entender padrões de organização de código e boas práticas, a lógica de execução, ast e integração foi desenvolvida do zero para este projeto.

## Estrutura do Código

* o projeto está organizado no diretório MicroC, com os seguintes módulos principais:
    * `grammar.lark`: define a gramática da linguagem `Micro-C`, especificando regras léxicas e sintáticas
    * `parser.py`: responsável por carregar a gramática e realizar a análise sintática, transformando o código-fonte em uma árvore sintática concreta (cst)
    * `transformer.py`: converte a cst em uma árvore sintática abstrata (ast), instanciando objetos das classes definidas em `ast.py`
    * `ast.py`: define as classes da ast, como `Program`, `VarDecl`, `FunDecl`, `IfStmt`, `WhileStmt`, `Assign`, `BinOp`, entre outras. Cada classe possui um método `eval` para execução
    * `node.py`: implementa o interpretador, visitando os nós da ast e executando o programa. Gerencia escopos, funções, variáveis e operadores
    * `ctx.py`: implementa a estrutura de contexto (escopo de variáveis), permitindo variáveis locais e globais
    * `errors.py`: define exceções para erros semânticos e de controle de fluxo (como retorno de função)
    * `cli.py`: implementa a interface de linha de comando, permitindo executar o interpretador, imprimir a ast ou cst
    * `__init__.py` e `__main__.py`: pontos de entrada do pacote, facilitando a execução via terminal

* etapas de compilação:
    * **análise léxica e sintática**: realizadas pelo Lark, usando a gramática em `grammar.lark` e o parser em `parser.py`
    * **análise semântica e execução**: realizadas durante a transformação da cst para ast (`transformer.py`) e principalmente na execução dos nós da ast pelo interpretador (`node.py`)

## Bugs/Limitações/problemas conhecidos

* **mensagens de erro**: as mensagens de erro sintático e semântico ainda são simples e poderiam ser mais informativas, indicando linha/coluna e contexto do erro

* **cobertura de tipos**: apenas os tipos `int` e `bool` são suportados. O tipo `void` existe apenas para funções sem retorno, não sendo possível declarar variáveis desse tipo

* **funções**: não há suporte para funções aninhadas ou recursão profunda, podendo ocorrer problemas de stack overflow em casos extremos

* **entrada/saída**: apenas a função `print` está disponível para saída. Não há suporte para entrada de dados do usuário

* **verificação de tipos**: a verificação de tipos é feita em tempo de execução, não havendo checagem estática de tipos

* **expressões complexas**: algumas construções sintáticas mais avançadas da linguagem C não são suportadas (ex: ponteiros, structs, arrays)

* **possíveis melhorias incrementais**:
    * Melhorar as mensagens de erro e adicionar mais testes.
    * Implementar suporte a arrays e funções recursivas.
    * Adicionar checagem estática de tipos.
    * Permitir entrada de dados do usuário.
    * Refatorar o código para facilitar a extensão da linguagem com novos recursos.