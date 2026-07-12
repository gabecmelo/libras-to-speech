# libras-to-speech 🤟🎙️

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

O **libras-to-speech** é um aplicativo desktop open-source focado em acessibilidade para livestreams. Ele traduz a soletração em LIBRAS (Língua Brasileira de Sinais) capturada pela webcam diretamente para texto e sintetiza a frase em voz em tempo real.

O projeto foi criado para permitir que streamers surdos ou com deficiência vocal interajam organicamente com seus chats, de forma 100% offline, local e segura (sem chamadas a APIs na nuvem que consomem banda ou enviam a sua imagem para a internet).

---

## ✨ Funcionalidades
- **Tradução Ultrarrápida**: Leitura fluída dos sinais diretamente pela sua câmera em tempo real.
- **Treinamento Personalizado**: O aplicativo aprende com você. Cadastre seus próprios gestos adaptados ao seu ambiente e iluminação.
- **Corretor Automático**: Correção inteligente de pequenas falhas durante a sinalização.
- **Sintetizador de Voz**: O sistema fala as palavras em voz alta automaticamente assim que a frase é finalizada.
- **Modo Escuro (Estilo OBS)**: Interface pensada para não cansar a vista durante as transmissões.

---

## 🗺️ Roadmap (Próximos Passos)
O projeto está apenas começando! Nossa visão de futuro inclui:
- [ ] **OBS Browser Overlay:** Disponibilizar a legenda transparente direto via WebSockets para ser inserida como fonte de navegador (Browser Source) no OBS.
- [ ] **Polimento de UI/UX:** Refatorar as telas de treinamento e listas para dar um ar mais moderno e premium ao aplicativo.
- [ ] **Base de Dados Pré-Treinada:** O app vir com um modelo universal base para que novos usuários não precisem treinar o alfabeto inteiro do zero.
- [ ] **Integração com Chat e Doações (Livepix/Superchat):** Alert boxes que traduzam o chat de volta (Texto -> LIBRAS).
- [ ] **Reconhecimento Contínuo de Sinais:** Evoluir da soletração (letras) para palavras contínuas da língua de sinais.

---

## 🎮 Para Usuários (Quero Apenas Usar!)
Se você não é programador e só quer testar o app na sua live, estamos automatizando a geração do executável.
*(Em breve)* Basta acessar a aba [Releases](../../releases) deste repositório, baixar o arquivo `libras-to-speech-windows.zip`, extrair e clicar duas vezes no `.exe`. 

**Não precisa instalar o Python!**

---

## 🛠️ Para Desenvolvedores (Como Contribuir)

Nós amamos Pull Requests! Se quiser construir as features do nosso Roadmap, siga o passo a passo:

### 1. Preparando o Ambiente
Clone o repositório para a sua máquina:
```bash
git clone https://github.com/gabecmelo/libras-to-speech.git
cd libras-to-speech
```

Crie um ambiente virtual (recomendado) e ative-o:
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

Instale as dependências locais:
```bash
pip install -r requirements.txt
```

### 2. Rodando o Projeto
```bash
python main.py
```
*Se for a sua primeira vez abrindo, lembre-se de clicar no botão "Modo de Treinamento" para cadastrar os gestos do alfabeto na sua câmera.*

### 3. Contribuindo
1. Faça um *Fork* do projeto.
2. Crie uma branch com a sua nova feature: `git checkout -b feature/minha-feature`.
3. Faça seus commits (comentários em inglês na estrutura do *Conventional Commits*).
4. Suba para sua branch: `git push origin feature/minha-feature`.
5. Abra um *Pull Request* aqui no repositório oficial!

---

## 📄 Licença
Distribuído sob a licença **GNU GPLv3**. Veja o arquivo `LICENSE` para mais detalhes. O código deve permanecer livre e aberto, sendo totalmente permitido seu uso por criadores e streamers na monetização do seu próprio conteúdo. 
Qualquer modificação no código fonte original também deve ser mantida pública.
