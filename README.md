# Str-AI-hd_von_ZaroBot

## Description

Str-AI-hd_von_ZaroBot is an interactive Discord bot that simulates the character Strahd von Zarovich using ChatGPT. Engage in immersive conversations, experience Strahd's cunning wit, and delve into the depths of Barovia without ever leaving your Discord server.

## Spoiler Warning

Players and DM's beware! Strahd cannot be controlled and could spoil the entire campain. Only use this bot if you are ok with the users reading the campaign book. That is esentially what you are giving them access to.

## Features

- **Dynamic Conversations:** The bot crafts responses based on Strahd's character, mood, current activities, and remembers past interactions with users.
- **Deep Lore:** Engage in discussions about Barovia, its inhabitants, and the tragic tale of Strahd and Tatyana.
- **Interactive Gameplay:** Challenge Strahd, seek his guidance, or just chat. The experience is tailored to each interaction.
- **Customizeable:** You can change anything in the prompt to attempt to make Strahd act a certain way. You can also adjust the format and length of the response I have set.

## Prerequisites

- Before setting up the bot, you need to obtain a few API keys, inatall Docker (recommended), and setup a bot in Discord Dev portal:
- Open the .env.edit.this.txt file and rename it to just .env and save it. This is the secret file you will save your keys. Do not leak it to anyone!!

### Discord Token

- **Skip if you already have a bot setup and have the bot token.**

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and give it a name.
3. Navigate to the "Bot" tab and click "Add Bot".
4. Give it any permissions and intents needed.
5. Under the "TOKEN" section, click "Copy" to copy your bot token. Enter it into the .env file.

### OpenAI API Key

- **Skip if you already have an API key**
- **The code is setup to use 3.5 turbo. If you want to use 4 you need to adjust the code**
- **This costs money for each API call. Please make sure you check the pricing and know what you are going to be spending. I spend around $0.05 per day on my bot but this will increase if you have a large numbers of users.**

1. Create an account or log in to [OpenAI](https://beta.openai.com/signup/).
2. Navigate to the API section.
3. Create a new API key and name it whatever you want. Copy your API key and enter it into the .env file.
4. Set a $$ limit for your API usage. You do not want to wake up one day and find someone spamming the bot and costing you hundreds of dollars.  

## Recommended Installation: Docker

Using Docker is the easiest and most hassle-free way to get your bot up and running. Just install docker (I also recommend Docker Desktop for an easy to view GUI)

### Step 1: Install Docker

If you don't have Docker installed:

- For Windows and Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- For Linux: Check your distribution's package manager (e.g., `sudo apt-get install docker` for Ubuntu)

### Step 2: Setup

1. **Cloning the repository using git**:
   If you have `git` installed on your computer, you can clone the repository by running the following command in your terminal (for macOS/Linux) or Command Prompt (for Windows):
    ```
    git clone https://github.com/kalebbroo/Str-AI-hd_von_ZaroBot.git
    ```

2. Navigate to the project's directory.
3. Open the `.env` file and replace the placeholders with your Discord token and OpenAI API key if you have not done so already.

### Step 3: Run the Bot

- **Windows**: Double-click on the `windows_install.bat` file.
- **Linux/Mac**: Open a terminal in the project's directory and run the ```./linux_install.sh``` script or run ```chmod +x linux_install.sh``` and tahat will allow you to just double click that file to install.

The mists of Barovia have awakened the presence of Strahd's digital avatar. With the bot now summoned and active, invite this dark presence to your Discord domain and dare to invoke it by mentioning its name. Engage if you must, but tread with caution, adventurer!

Should you desire to venture further into the shadows, join my dev Discord server to test the bot. Beware, for you are not alone in these haunted halls: https://discord.gg/CmrFZgZVEE

---

**Note**: Always ensure your tokens and keys are kept private and are not pushed to public repositories or shared openly.

