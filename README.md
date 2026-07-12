# LIBRAS to Speech

Um aplicativo desktop open-source desenvolvido em Python para traduzir o alfabeto de LIBRAS (Língua Brasileira de Sinais) em texto e sintetizá-lo em voz em tempo real. O foco principal é auxiliar pessoas com deficiência auditiva ou vocal a interagir em livestreams.

## Funcionalidades
- **Detecção em Tempo Real**: Usa a webcam para rastrear os movimentos da mão (MediaPipe).
- **Tradução LIBRAS -> Português**: Converte os gestos do alfabeto em letras, compondo palavras completas e frases.
- **Texto para Voz (TTS)**: Fala em português as palavras formadas em tempo real.
- **Interface Estilo OBS**: Layout escuro, painel de vídeo com sobreposição de dados e histórico de traduções.
- **Modo de Treinamento Integrado**: Permite a qualquer pessoa coletar novos dados da câmera e retreinar o modelo de Inteligência Artificial localmente.

## Requisitos
- Python 3.8+
- Webcam

## Instalação

1. Clone o repositório ou acesse a pasta.
2. Crie um ambiente virtual (opcional mas recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como usar
1. Execute o arquivo principal:
   ```bash
   python main.py
   ```
2. Ao abrir o aplicativo, ele começará a capturar a imagem da sua câmera.
3. Se for a primeira vez usando, clique no botão **Modo de Treinamento** (botão vermelho na interface).
4. No Modo de Treinamento:
   - Selecione a letra que deseja ensinar ao programa (ex: A, B, ESPAÇO, APAGAR).
   - Segure a posição da mão para essa letra em frente à câmera.
   - Clique em **Iniciar Coleta** e o programa começará a salvar os pontos da sua mão. 
   - Mexa a mão suavemente para capturar diferentes ângulos por alguns segundos, e então clique em **Parar Coleta**.
   - Repita para outras letras que desejar treinar.
   - Ao final, clique em **Treinar e Salvar Modelo**. O programa treinará a IA baseada nas suas fotos e salvará em `libras_model.pkl`.
5. Agora basta fazer os sinais para a câmera no painel inicial. O programa irá formar a palavra. Para finalizar uma palavra e ouvi-la (TTS), faça o sinal ensinado como **ENTER**.

## Arquitetura e Tecnologias
- **UI:** PyQt6
- **Computer Vision:** OpenCV e MediaPipe (Hands)
- **Machine Learning:** scikit-learn (RandomForestClassifier)
- **Text-To-Speech:** pyttsx3
