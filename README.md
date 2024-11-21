[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/H1QdPKuv)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=16992133&assignment_repo_type=AssignmentRepo)
# INF0413 - Processamento Digital de Sinais e Imagens

Equipe: \
202303342 - HERIK KAUAN DE ASSIS \
202303352 - LUIS EDUARDO FONSECA ALVES FERREIRA MATHIAS CRUVINEL \
202303355 - MATEUS LACERDA ALVES SILVA \
202305745 - NICKOLAS IORY BERNARDES SILVA \
202303359 - PEDRO REIS PIMENTA 

# Conteúdos
1. [Artigo](#nome_artigo)
    1. [Resumo](#resumo)
    2. [Palavras-chave](#palavras_chave)
    3. [Introdução](#introducao)
    4. [Fundamentação teórica](#fund_teorica)
    5. [Metodologia](#metodologia)
    6. [Resultados e conclusões](#resultados)
    7. [Referências](#referencias)
    8. [Apêndices](#apendices)
2. [Ambiente de desenvolvimento](#ambiente)
3. [Utilização](#utilizacao)


# Geração de Músicas Binaurais <a name="nome_artigo"></a>
## Uma aplicação de IA generativa com técnicas de modularização de áudio

### Resumo <a name="resumo"></a>
Do processo de ideação, tem-se como fator motivador a capacidade cognitiva presente nos áudios com frequências binaurais. Para este projeto, utiliza-se o **AudioCraft** da **Meta** para gerar músicas a partir de descrições textuais com o modelo **MusicGen**. Em seguida, aplica-se um processo de modulação de frequência para criar batimentos binaurais para cada ouvido. O processo envolve gerar ondas senoidais com frequências diferentes, combiná-las com a música gerada e ajustar o volume para preservar a qualidade sonora. A tecnologia utilizada foi a linguagem de programação `Python`, com as bibliotecas `librosa`, `pydub` e `audiocraft`.

### Palavras-chave <a name="palavras_chave"></a>
[Inteligência Artificial Generativa](https://en.wikipedia.org/wiki/Generative_artificial_intelligence), [Binaural](https://en.wikipedia.org/wiki/Binaural_beats), [AudioCraft](https://github.com/facebookresearch/audiocraft), [Transposição de Pitch](https://en.wikipedia.org/wiki/Pitch_shift), [Modulação de Frequência](https://en.wikipedia.org/wiki/Frequency_modulation)

### Introdução <a name="introducao"></a>
A música tem um impacto significativo na cognição humana, influenciando estados emocionais, níveis de concentração e processos terapêuticos. Neste contexto, as frequências binaurais são uma ferramenta promissora, que, ao serem sincronizadas com as ondas cerebrais fundamentais, promovem benefícios como relaxamento, aumento de atenção e alívio de estresse (Gao & Hsu, 2020; Lane et al., 1998). No entanto, a criação personalizada de músicas que as incorporam de maneira eficiente ainda apresenta desafios, especialmente no que tange à integração harmoniosa entre elementos musicais e batimentos binaurais, além da adaptação para diferentes personas e suas frequências fundamentais ideais. Desta forma, este projeto busca abordar a problemática utilizando **Inteligência Artificial (IA) generativa**, mais especificamente o **AudioCraft** da **Meta**, para gerar composições musicais a partir de descrições textuais fornecidas pelos usuários, seguido pela aplicação de técnicas de **modulação de frequência** para inserir batimentos binaurais específicos. \
Para alcançar esses objetivos, serão utilizadas diversas amostras de músicas geradas pelo modelo MusicGen como fonte de dados, permitindo alta capacidade de experimentação. Esse aspecto de pesquisa necessita de um abrangente estudo da literatura sobre geração de músicas por IA (Choi et al., 2020; Oord et al., 2016), bem como pesquisas sobre os efeitos e aplicações das frequências binaurais (Le Scouarnec et al., 2001). Por outro lado, no aspecto da aplicação, serão empregados métodos de **transposição de pitch** e **modulação de frequência**, implementados através das bibliotecas Python `librosa`, `pydub` e `audiocraft`. Desta forma, ainda que a avaliação dos resultados seja uma tarefa substancialmente subjetiva em termos de funcionalidade,  objetivamente serão feitos testes de qualidade sonora e análise de percepção dos batimentos binaurais pelos usuários, utilizando benchmarks como o **Mean Opinion Score (MOS)**, o **Perceptual Evaluation of Audio Quality (PEAQ)** e o **Mel-Cepstral Distortion (MCD)**, e **feedback qualitativo**. Por fim, este estudo visa integrar avanços em IA generativa com técnicas de processamento de áudio para proporcionar experiências auditivas personalizadas que potencializam benefícios cognitivos e terapêuticos.

### Metodologia <a name="metodologia"></a>
Em uma página online, para o usuário testar, haverá um estágio inicial que será usado para pegar os inputs, sendo eles a frequência desejada — a sensacao que o usuario deseja ter — e uma descrição textual da música. Essa informação passará por um processo de abstração, transformando a sensação desejada em uma **frequência binaural**. Após isso, a **inferência** será feita em uma máquina separada de acordo com a descrição textual, que passará por uma pipeline de processamento para que a binauralidade com a frequência desejada seja aplicada. Assim, o modelo retornará o áudio. Na plataforma online, juntamente com perguntas para coletar o _feedback_, haverá o áudio para o usuário ouvir e baixar. Além disso, haverá uma parte separada para a pesquisa de satisfação do usuário, que consistirá em uma sequência de 8 áudios, cada um de 15 segundos, separados em 4 grupos, cada grupo contendo a mesma música com ondas bineurais e sem, em uma ordem não informada. Ademais, será apresentada uma lista para o usuário escolher o que sentiu em cada áudio e qual ele preferiu, valendo ressaltar que esse processo, desde a apresentação dos áudios até a demonstração de agrado, será feito na plataforma online, utilizando o framework `Streamlit`. Outrossim, o backend estará separado em inferência, processamento e o backend da própria plataforma.

### Referências <a name="referencias"></a>
1. K. Choi, G. Fazekas, and M. Sandler, “A survey on music generation with deep learning: Challenges and future directions,” *IEEE Transactions on Affective Computing*, vol. 11, pp. 150, 2020.
2. X. Gao and L. Hsu, “Binaural beats and their effects on human cognition and mood: A review,” *Frontiers in Psychology*, vol. 11, p. 150, 2020.
3. J. D. Lane, S. J. Kasian, J. E. Owens, and G. R. Marsh, “The effect of binaural beats on cognitive performance and mood states,” *Psychology of Music*, vol. 26, pp. 250–254, 1998.
4. A. Puel, T. Hospedales, and D. P. W. Ellis, “MusicGen: Generation of high-quality music with controllable semantics,” *GitHub Repository*, Jun. 2023. [Online]. Available: [https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md). [Accessed: Oct. 30, 2024].
5. A. Puel, T. Hospedales, and D. P. W. Ellis, “MusicGen: Generation of high-quality music with controllable semantics,” *arXiv preprint arXiv:2306.05284*, Jun. 2023.

---
## Ambiente de desenvolvimento <a name="ambiente"></a>
### Versão do Python

Este projeto requer o Python 3.10, por motivos de compatibilidade. Siga as instruções abaixo para instalar a versão correta do Python em seu sistema operacional.

#### Windows

1. Baixe o instalador do Python 3.10 no site oficial: [Python.org](https://www.python.org/downloads/release/python-3100/).
2. Execute o instalador e siga as instruções na tela. Certifique-se de marcar a opção "Add Python to PATH".
3. Verifique a instalação abrindo o Prompt de Comando e digitando:
    ```sh
    python --version
    ```

#### Linux

1. Atualize a lista de pacotes:
    ```sh
    sudo apt update
    ```
2. Instale as dependências necessárias:
    ```sh
    sudo apt install software-properties-common
    ```
3. Adicione o repositório de terceiros para Python 3.10:
    ```sh
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```
4. Instale o Python 3.10:
    ```sh
    sudo apt install python3.10
    ```
5. Verifique a instalação digitando:
    ```sh
    python3.10 --version
    ```

### Requirements

As dependências do projeto, na parte que carrega e serve o modelo de geração de áudio, são listadas no repositório oficial. Para utilizar o audiocraft e instalar as dependências, rode o script:

```sh
bash requirements/install_model_requirements.sh
```
## Utilização <a name="utilizacao"></a>

Para utilizar o script `BinauralSounds.AI`, siga as instruções abaixo:

1. Certifique-se de ter todas as dependências instaladas conforme descrito na seção [Ambiente de desenvolvimento](#ambiente).
2. Execute o script com os argumentos desejados:

    ```sh
    python src/binaural_sounds.py [opções]
    ```

### Opções disponíveis:

- `-lm`, `--load_model`: Carrega o modelo pré-treinado `facebook/audiogen-medium`.
- `-g`, `--generate`: Ativar o modo de geração de música.
- `-sm`, `--serve_model`: Serve a API do modelo localmente com `ngrok`.
- `-sa`, `--serve_app`: Serve o aplicativo de feedback localmente com `Streamlit` (não implementado).

### Exemplos de uso:

- Para carregar o modelo pré-treinado:

    ```sh
    python src/binaural_sounds.py --load_model
    ```

- Para servir o modelo com ngrok com geração de música ativada:

    ```sh
    python src/binaural_sounds.py --serve_model --generate
    ```

- Para exibir a ajuda:

    ```sh
    python src/binaural_sounds.py --help
    ```

**Nota:** A funcionalidade `serve_app` ainda não está implementada.
