# Trabalho Prático de TCOMP 2025.1 (Fundamentos Teóricos da Computação)

## Sobre

Nesse trabalho foram implementadas as seguintes conversões:

- Gramática Linear Unitária a Direita (GLUD) → Automato Finito Não Deterministico (AFND)
- Automato Finito Não Deterministico (AFND) → Automato Finito Deterministico (AFD)

Também foram implementadas as operações:
- Complemento do AFD
- Reverso do AFD

## Como executar

Você pode executar o arquivo `main.py`. Nesse caso, se você tiver o arquivo `grammar.txt` seguindo uma notação como:

```text
# Gramática: G = ({A, S}, {a, b}, P, S)

A -> aA 
A -> b  
S -> aA  
S -> ε
```

Serão feitas todas as etapas de:
1. Converter para AFND
2. Converter para AFD
3. Operação de completo do AFD
4. Operação de reverso do AFD

> **Nota**: Caso tenha algum problema no `grammar.txt`, você poderá ajustar o objeto que vem do arquivo `test_input.py`

Ao final da execução do `main.py`, você poderá ver os resultados nos arquivos:
- `AFD.txt`
- `AFND.txt`
- `COMP.txt`
- `REV.txt`

Além dos prints que aparecerão no terminal.

### Testes manuais

No arquivo `test_input.py` tem um exemplo de um objeto que representa uma gramática que você pode usar para validar!

### Restrições

Para o funcionamento correto das conversões, você deve assumir que:

```python
EPSILON_SYMBOL = 'ε'
GRAMMAR_FINAL_STATE = 'G'
REVERSE_FINAL_STATE = 'R'
NULL_STATE = 'Ø'
```

Esses foram os símbolos selecionados para representar:
1. Estado final (G) usado para converter GLUD em uma AFND
2. Estado final (R) usado para fazer o reverso da AFD
3. Estado nulo (Ø) usado para transições sem destino nas conversões
4. 'ε' está representando o símbolo vazio