# Plano detalhado — Projeto A-Maze-ing

# Visão geral

Este plano organiza o desenvolvimento do projeto **A-Maze-ing** em dupla, com foco em entrega incremental, boa divisão de responsabilidades, revisão constante e preparação para a avaliação.

O projeto exige um gerador de labirintos em **Python 3.10+**, execução via `python3 a_maze_ing.py config.txt`, leitura de arquivo de configuração, geração aleatória com **seed**, possibilidade de labirinto perfeito, exportação em formato hexadecimal por célula, representação visual, tratamento robusto de erros, `Makefile`, qualidade com **flake8** e **mypy**, documentação e um módulo reutilizável empacotável (`mazegen-*`).

# Objetivo da dupla

Entregar um projeto que:

- funcione de forma confiável do começo ao fim;
- seja fácil de explicar durante a avaliação;
- tenha arquitetura reutilizável;
- cubra completamente a parte obrigatória antes de pensar em bônus;
- deixe cada integrante apto a modificar rapidamente partes do código na defesa.

# Escopo obrigatório resumido

## Entrada

- Arquivo de configuração com pares `KEY=VALUE`.
- Chaves obrigatórias: `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`.
- Linhas com `#` são comentários e devem ser ignoradas.
- Pode haver chaves extras, como `SEED`, algoritmo e modo de exibição.

## Regras centrais do labirinto

- Entrada e saída devem existir, ser diferentes e estar dentro dos limites.
- O labirinto precisa ser coerente entre células vizinhas.
- Deve haver conectividade total, sem células isoladas, exceto a exceção relacionada ao padrão visual “42”.
- Bordas externas precisam respeitar que entrada e saída são células específicas.
- Não pode haver áreas abertas grandes: corredores não podem gerar áreas 3x3 abertas.
- Quando possível pelo tamanho, o visual deve conter um **“42”** formado por células totalmente fechadas.
- Com `PERFECT=True`, deve existir **exatamente um caminho** entre entrada e saída.

## Saída

- Arquivo com uma linha por linha do labirinto.
- Cada célula deve ser escrita com **1 dígito hexadecimal**, representando paredes fechadas em N/E/S/W.
- Depois de uma linha vazia: coordenadas de entrada, coordenadas de saída e o menor caminho válido usando `N E S W`.

## Visualização

- Pode ser ASCII no terminal ou gráfica.
- Deve mostrar paredes, entrada, saída e caminho.
- Deve permitir pelo menos:
    - regenerar labirinto;
    - mostrar/ocultar caminho mínimo;
    - mudar cor das paredes.

## Reusabilidade

- O gerador deve existir como uma classe única reutilizável.
- O módulo deve ser empacotado como `mazegen-*` na raiz do repositório.
- README principal também precisa documentar como usar a parte reutilizável.

# Estratégia técnica recomendada

## Decisão de arquitetura

Separar o projeto em blocos independentes:

1. **Parser de configuração**
2. **Validador de configuração**
3. **Modelo interno do labirinto**
4. **Gerador do labirinto**
5. **Validador estrutural do labirinto**
6. **Resolvedor do menor caminho**
7. **Exportador do arquivo hexadecimal**
8. **Renderer visual**
9. **Camada CLI / programa principal**
10. **Módulo reutilizável empacotável**

## Escolha recomendada de algoritmo

Para a primeira versão, usar **Recursive Backtracker** ou outra estratégia simples que gere bem labirintos perfeitos. Motivos:

- implementação mais previsível para explicar;
- fácil garantir conectividade;
- boa compatibilidade com seed;
- mais simples de adaptar para a parte de caminho e validação.

Depois que a versão obrigatória estiver estável, a dupla pode avaliar um segundo algoritmo como bônus.

## Estratégia para o menor caminho

Separar claramente:

- geração do labirinto;
- cálculo do menor caminho;
- serialização da solução no arquivo.

Isso ajuda na defesa e reduz risco de acoplamento confuso.

# Divisão de trabalho da dupla

## Pessoa A — núcleo do projeto

Responsável principal por:

- parser e validação de configuração;
- estrutura interna do labirinto;
- geração do labirinto;
- coerência entre paredes vizinhas;
- regra de conectividade;
- seed e reprodutibilidade.

## Pessoa B — entrega e experiência final

Responsável principal por:

- resolução do menor caminho;
- exportação do arquivo final;
- visualização ASCII ou gráfica;
- interações do visual;
- README;
- empacotamento do módulo reutilizável.

## Responsabilidades compartilhadas

Os dois devem revisar juntos:

- definição do modelo de dados;
- decisões de arquitetura;
- estratégia para o “42”;
- tratamento de erros;
- lint, mypy e testes;
- preparação para avaliação.

# Regras de colaboração

- Toda feature importante deve ser explicada pelo autor para o colega.
- Nenhuma parte crítica deve ficar conhecida por apenas uma pessoa.
- Toda mudança em estrutura de dados precisa ser validada em conjunto.
- Antes de mergear, a outra pessoa revisa funcionalmente e conceitualmente.
- A cada fase, os dois devem conseguir explicar como aquela parte funciona.

# Plano em fases

## Fase 1 — entendimento e definição da arquitetura

### Objetivo

Fechar o escopo e alinhar o modelo interno do projeto.

### Tarefas

- Ler o enunciado completo juntos.
- Anotar requisitos obrigatórios e bônus separadamente.
- Decidir o formato interno da célula e do labirinto.
- Definir convenção fixa para direções: N, E, S, W.
- Decidir como representar paredes e vizinhos.
- Definir estratégia para seed.
- Escolher a primeira forma de visualização: ASCII ou gráfica.
- Definir o algoritmo principal do gerador.
- Planejar a estrutura do repositório.

### Entregáveis

- Mapa de módulos.
- Lista de regras obrigatórias.
- Lista de riscos técnicos.
- Acordo sobre convenções de dados.

### Critério de pronto

A dupla consegue desenhar no quadro ou papel como os dados fluem do `config.txt` até o arquivo final e a visualização.

## Fase 2 — parsing e validação da configuração

### Objetivo

Garantir entrada confiável antes de gerar qualquer labirinto.

### Tarefas

- Ler arquivo linha por linha.
- Ignorar comentários e linhas vazias.
- Separar `KEY=VALUE` com tolerância a erros comuns.
- Validar presença de todas as chaves obrigatórias.
- Validar tipos e formatos.
- Validar limites de `ENTRY` e `EXIT`.
- Validar que entrada e saída são diferentes.
- Validar dimensões possíveis.
- Validar `PERFECT`.
- Definir mensagens de erro claras.
- Criar arquivo de configuração padrão para o repositório.

### Entregáveis

- Parser funcionando.
- Validação robusta.
- Casos de erro documentados.

### Critério de pronto

Qualquer configuração inválida retorna erro claro, sem crash inesperado.

## Fase 3 — modelo interno + gerador base

### Objetivo

Construir a estrutura interna do labirinto e gerar um primeiro labirinto válido.

### Tarefas

- Criar a estrutura da célula.
- Garantir quatro direções cardeais por célula.
- Implementar construção da grade.
- Implementar algoritmo com seed.
- Garantir conectividade total.
- Garantir simetria entre paredes vizinhas.
- Garantir bordas externas válidas.
- Diferenciar fluxo para `PERFECT=True`.

### Entregáveis

- Labirinto gerado internamente.
- Consistência de paredes validada.
- Seed reproduzindo resultado.

### Critério de pronto

A mesma seed gera o mesmo labirinto e o validador interno não encontra incoerências.

## Fase 4 — regras especiais e validações de qualidade

### Objetivo

Fazer o labirinto atender ao enunciado de forma completa.

### Tarefas

- Verificar ausência de células isoladas.
- Verificar conectividade global.
- Verificar restrição de áreas abertas grandes.
- Implementar estratégia do padrão visual “42”.
- Detectar quando o tamanho é pequeno demais para inserir “42”.
- Emitir mensagem de erro quando o “42” não puder ser aplicado.
- Garantir que entrada e saída continuem válidas após todas as regras.

### Entregáveis

- Validador estrutural do labirinto.
- Regra do “42” definida e documentada.

### Critério de pronto

O labirinto satisfaz todas as regras do enunciado ou informa claramente a limitação permitida.

## Fase 5 — caminho mínimo e exportação do arquivo

### Objetivo

Gerar a saída exatamente no formato exigido.

### Tarefas

- Calcular menor caminho entre entrada e saída.
- Converter o caminho para sequência `N/E/S/W`.
- Converter cada célula para dígito hexadecimal com mapeamento correto de bits.
- Exportar linhas do grid na ordem correta.
- Inserir linha vazia.
- Inserir entrada, saída e solução nas três linhas finais.
- Garantir `\n` ao fim das linhas.
- Testar com pequenos exemplos manuais.

### Entregáveis

- Arquivo final válido.
- Função de serialização documentada.
- Casos de teste para saída.

### Critério de pronto

O arquivo gerado pode ser verificado logicamente e segue exatamente o contrato do enunciado.

## Fase 6 — visualização e interações

### Objetivo

Entregar uma experiência visual clara e defensável.

### Tarefas

- Exibir paredes, entrada, saída e caminho.
- Implementar regeneração do labirinto.
- Implementar mostrar/ocultar menor caminho.
- Implementar troca de cor das paredes.
- Destacar o padrão “42” se desejarem.
- Garantir que a visualização reflita fielmente a estrutura interna.

### Entregáveis

- Visualização usável.
- Interações mínimas obrigatórias.

### Critério de pronto

Alguém externo consegue entender visualmente o labirinto e interagir com os comandos pedidos.

## Fase 7 — reusabilidade, empacotamento e README

### Objetivo

Fechar a entrega formal do projeto.

### Tarefas

- Isolar a classe geradora reutilizável.
- Garantir API clara para criar labirinto, usar seed e acessar solução.
- Preparar pacote `mazegen-*` na raiz do repositório.
- Garantir que a documentação do módulo exista.
- Escrever README com tudo o que o enunciado exige.
- Incluir instruções de uso, configuração e algoritmo escolhido.
- Documentar a organização da dupla e a evolução do planejamento.

### Entregáveis

- Pacote construível.
- README completo.
- Estrutura de projeto pronta para avaliação.

### Critério de pronto

Um avaliador consegue instalar, entender e executar o projeto lendo apenas o repositório.

## Fase 8 — qualidade, testes e preparação para defesa

### Objetivo

Reduzir risco de falha na avaliação.

### Tarefas

- Revisar `flake8`.
- Revisar `mypy` com os flags exigidos.
- Revisar docstrings e type hints.
- Revisar `Makefile` com `install`, `run`, `debug`, `clean`, `lint` e opcional `lint-strict`.
- Criar casos de teste manuais e automatizados.
- Simular defesa com pequenas mudanças no projeto.
- Fazer troca de papéis: cada pessoa explica a parte do colega.

### Entregáveis

- Projeto limpo e estável.
- Checklist de defesa concluído.

### Critério de pronto

Os dois conseguem responder perguntas e fazer pequenas modificações com segurança.

# Cronograma sugerido

## Sprint 1

- Fase 1
- Fase 2

## Sprint 2

- Fase 3

## Sprint 3

- Fase 4
- início da Fase 5

## Sprint 4

- fim da Fase 5
- Fase 6

## Sprint 5

- Fase 7
- Fase 8

# Quadro de tarefas sugerido no Notion

## Backlog

- Ler enunciado e transformar em checklist.
- Definir estrutura do grid.
- Definir representação das paredes.
- Implementar parser.
- Implementar validador.
- Implementar gerador com seed.
- Implementar verificador de conectividade.
- Implementar verificador de simetria entre paredes.
- Implementar restrição de áreas abertas.
- Implementar padrão “42”.
- Implementar menor caminho.
- Implementar exportação hexadecimal.
- Implementar visualização.
- Implementar interações.
- Criar README.
- Criar pacote reutilizável.
- Revisar Makefile.
- Rodar lint e mypy.
- Simular defesa.

## Status sugeridos

- A fazer
- Em andamento
- Em revisão
- Bloqueado
- Concluído

# Checklist de requisitos obrigatórios

- Programa principal com nome correto.
- Um único argumento: arquivo de configuração.
- Tratamento de erro sem crash.
- Python 3.10+.
- flake8.
- mypy com os flags exigidos.
- Type hints.
- Docstrings.
- Makefile obrigatório.
- `.gitignore`.
- Configuração padrão no repositório.
- Seed para reprodutibilidade.
- Labirinto válido e coerente.
- Opção de labirinto perfeito.
- Saída hexadecimal por célula.
- Menor caminho exportado.
- Visualização com interações mínimas.
- Classe reutilizável.
- Pacote `mazegen-*`.
- README completo.

# Critérios de revisão por fase

## Revisão técnica

- O comportamento bate com o enunciado?
- Há risco de casos de borda não tratados?
- O nome das funções e responsabilidades estão claros?
- Está fácil de explicar oralmente?

## Revisão da dupla

- O colega consegue reproduzir o raciocínio?
- O colega sabe testar essa parte?
- O colega conseguiria corrigir um bug nela?

# Riscos e mitigação

## Risco 1 — escolher arquitetura muito acoplada

Mitigação: definir cedo um modelo interno simples e separar geração, solução, exportação e visualização.

## Risco 2 — deixar a visualização para o final

Mitigação: criar uma versão visual mínima cedo, mesmo simples.

## Risco 3 — o “42” quebrar a validade do labirinto

Mitigação: tratar o “42” como regra validada e testada isoladamente.

## Risco 4 — output hexadecimal sair quase certo, mas não exatamente

Mitigação: testar manualmente labirintos pequenos conhecidos e revisar o mapeamento de bits.

## Risco 5 — só uma pessoa dominar parte crítica

Mitigação: revisão cruzada obrigatória e sessões curtas de explicação mútua.

# Reunião rápida diária sugerida

Responder em 5 minutos:

- O que foi concluído?
- O que está bloqueado?
- O que entra hoje?
- O que o outro precisa entender hoje?

# Estrutura sugerida do README

- Linha inicial obrigatória do 42.
- Descrição.
- Instruções de instalação/execução.
- Estrutura completa do arquivo de configuração.
- Algoritmo escolhido.
- Justificativa da escolha.
- Parte reutilizável e como usar.
- Organização da equipe.
- Planejamento previsto e evolução real.
- O que funcionou bem.
- O que pode melhorar.
- Ferramentas usadas.
- Recursos estudados.
- Como IA foi usada e em quais partes.

# detalhadoPreparação para a avaliação

## Perguntas que vocês devem conseguir responder

- Como a configuração é validada?
- Como as paredes são representadas internamente?
- Como vocês garantem consistência entre células vizinhas?
- Como garantem conectividade?
- Como garantem unicidade do caminho quando o labirinto é perfeito?
- Como o hexadecimal é calculado?
- Como o menor caminho é encontrado?
- Como o “42” é inserido sem quebrar o labirinto?
- O que é reutilizável no projeto?
- Como empacotar e instalar a parte `mazegen-*`?

## Simulações recomendadas

- Trocar formato de exibição de um detalhe visual.
- Adicionar uma chave opcional no config.
- Mudar regra de cor da visualização.
- Ajustar serialização da solução.
- Mostrar uma propriedade extra da estrutura interna.

# Regra final da dupla

**Terminou a parte obrigatória antes de pensar em bônus.**

Bônus só entram quando:

- o output obrigatório estiver correto;
- o visual mínimo estiver pronto;
- o README estiver quase fechado;
- os dois souberem explicar tudo.

# Base usada

Plano montado a partir do enunciado do projeto A-Maze-ing que pede Python 3.10+, flake8, mypy, Makefile, configuração por arquivo, geração com seed, opção de labirinto perfeito, saída hexadecimal, visualização, módulo reutilizável e README completo.
