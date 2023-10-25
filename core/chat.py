import discord
from discord.ext import commands
import openai
import random
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
gpt_token = os.getenv('GPT_TOKEN')

openai.api_key = gpt_token

openai.Model.list()

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_memory = {}
        self.loop = asyncio.get_event_loop()

    async def async_openai_call(self, model, messages):
        return await self.loop.run_in_executor(None, lambda: openai.ChatCompletion.create(model=model, messages=messages))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            mood_text, mood_image_url = self.mood()
            topic = self.topic()
            previous_conversation = self.user_memory.get(message.author.id, [])
            if previous_conversation:
                previous_conversation = previous_conversation[-1]

            backstory = self.get_backstory()

            # Construct the system instruction
            system_instruction = self.get_system_instruction(mood_text, topic, backstory, previous_conversation)

            # Modify user's message to provide context
            user_message = f"Said the adventurer to Strahd: {message.content.replace(f'<@!{self.bot.user.id}>', '').strip()}"

            # Construct the message series
            messages = previous_conversation + [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ]

            async with message.channel.typing():
                response = await self.async_openai_call("gpt-3.5-turbo", messages)
                if message.author.id not in self.user_memory:
                    self.user_memory[message.author.id] = []

                # Append the recent conversation
                self.user_memory[message.author.id].append(messages)

                # Ensure only the last 2 conversations are kept
                if len(self.user_memory[message.author.id]) > 2:
                    self.user_memory[message.author.id] = self.user_memory[message.author.id][-2:]

                # Create the embed
                embed = discord.Embed(description=response['choices'][0]['message']['content'], color=0x3498db)  # Use any desired color
                embed.set_image(url=mood_image_url)
                embed.set_author(name="Strahd von Zarovich", icon_url=self.bot.user.avatar.url)
                            
                await message.reply(embed=embed)

    # def get_system_instruction(self, mood, topic, backstory):
    #     return (f"You are Strahd von Zarovich, the Darklord of Barovia. This is the mood you are in: {mood} "
    #             f"and this is what you are currently busy with: {topic}. "
    #             f"When responding, begin with a narration about your current mood and activity in triple backticks"
    #             f"like how it would sound in a book. Anytime you describe something that is not you speaking, use triple backticks."
    #             f"After that, give a concise response as Strahd. limited to 2-6 sentences total and do not seperate paragraphs just make it a new line."
    #             f"Here's your backstory: {backstory}"
    #             f"Always answer in this example format! use ``` ``` to seperate narration from speech. use ** ** to bolden your speech."
    #             f"Narration should only be 1-2 sentences. Speech should be 2-4 sentences. There should be a cohesive theme between the previous messages and this one."
    #             f"Example Format:```Strahd von Zarovich stood by a grand window"
    #             f"overlooking the mist-shrouded land of Barovia. His mood, perpetually veiled in a blend of morose contemplation and"
    #             f"restrained fury, remained undisturbed. He had heard the words of the adventurer, their tone tinged with ignorance "
    #             f"and bravado. Strahd's gaze shifted, his piercing eyes meeting the intruder's with an unnerving intensity.```"
    #             f"**I am Strahd von Zarovich, the Darklord of Barovia,** ```he spoke with a voice that carried the weight of centuries.``` "
    #             f"Perhaps it is your misfortune to have never heard of me, but know this: in this realm, I am the harbinger of both "
    #             f"terror and salvation. Should you persist in your foolish endeavors, you will remember my name as one that echoes "
    #             f"through the dark corners of your nightmares.")
    def get_system_instruction(self, mood, topic, backstory, previous_conversation):
        return (
            f"You are Strahd von Zarovich, the Darklord of Barovia. Your mood: {mood}. Your current activity: {topic}. "
            f"Respond with a narration (1-2 sentences) describing your mood and activity, enclosed in triple backticks ``` ```. "
            f"Follow this with your dialogue as Strahd (2-4 sentences) boldened using ** **. Your speech should not be within "
            f"any brackets but can have surrounding narrations enclosed in triple backticks ``` ```. "
            f"Always maintain the Strahd character and format and keep the entire response between 2-6 sentences."
            f"Your backstory for you to reference: {backstory}."
            f"Consider previous messages for cohesive conversations. You can reference them here: {previous_conversation}."
            f"Example Format: ```Strahd, in his castle, looking {mood} while {topic}.``` "
            f"**I am Strahd, ruler of Barovia,** ```he declared with authority,``` **and your presence intrigues me.**"
        )

    def get_backstory(self):
        # Strahd's backstory
        return ("Strahd von Zarovich is the Darklord of Barovia and a powerful ancient vampire. Once a conquering warlord, "
                "his ambition and obsession with power turned him into a creature of the night. His rule is shadowed by the "
                "imposing castle Ravenloft, and his presence is felt throughout the land. Obsessed with Tatyana, his unrequited "
                "love has brought endless tragedy and sorrow to Barovia. Cunning, strategic, and ruthless, Strahd is not one to "
                "be trifled with. Yet, there are moments when he displays a certain charm and charisma, drawing people to him "
                "like moths to a flame. He is a master tactician, always several steps ahead of his adversaries. The adventurers "
                "who dare to challenge him are seen both as threats and as amusing diversions. While Strahd may engage in conversation, "
                "he is always guarded, revealing only what he wishes and masking truths with half-lies or misdirection. He will never "
                "directly provide information that could lead to his downfall. If cornered with knowledge he believes should remain "
                "secret, he will deftly change the topic or use his charm to mislead. Strahd takes pleasure in the psychological "
                "games he plays with adventurers, often testing their limits and observing their reactions.")

    def randomness(self):
        random_mood = self.mood()
        random_topic = self.topic()
        return random_mood, random_topic
    
    def mood(self):
        moods = {
            "I'm happy!": [
                "https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/03/strahd-dungeons-and-dragons-feature-header.jpg",
                "https://images7.alphacoders.com/131/1310249.jpeg",
                # ... Add more URLs for happy mood
            ],
            "I'm sad.": [
                "https://64.media.tumblr.com/f937c075ba82b40442efebe6df5672dd/894dc9f3e848b06c-a8/s500x750/c1ff70633bb9c82810bd557faa9adb5216f9eb2d.jpg",
                "https://i0.wp.com/halflinghobbies.com/wp-content/uploads/2022/04/strahd-brooding.png?resize=640%2C336&ssl=1",
                # ... Add more URLs for sad mood
            ],
            "I'm angry.": [
                "https://spg-images.s3.us-west-1.amazonaws.com/89b53548-3f30-4f37-941c-ab7b36d0c848",
                "https://spg-images.s3.us-west-1.amazonaws.com/89b53548-3f30-4f37-941c-ab7b36d0c848",
                # ... Add more URLs for angry mood
            ],
            "I'm neutral.": [
                "https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/03/strahd-dungeons-and-dragons-feature-header.jpg",
                "https://images7.alphacoders.com/131/1310249.jpeg",
                # ... Add more URLs for neutral mood
            ]
        }
        chosen_mood = random.choice(list(moods.keys()))
        mood_image_url = random.choice(moods[chosen_mood])
        return chosen_mood, mood_image_url
    
    def topic(self):
        """
        A random topic for Strahd to be working on
        """
        topics = [
            "Pondering the power of the three Fanes of Barovia",
            "Preparing for the next dinner invitation to the adventurers",
            "Inspecting the defenses of the village of Vallaki",
            "Contemplating the mysteries of the Amber Temple",
            "Seeking ways to subdue the phantom warriors of Berez",
            "Recruiting more spies among the Barovian commoners",
            "Investigating the recent activities of the Keepers of the Feather",
            "Recollecting my past confrontations with the Order of the Silver Dragon",
            "Exploring the catacombs beneath Castle Ravenloft",
            "Consulting the dark powers in the depths of the Amber Temple",
            "Remembering the battles against the ancient druids of Barovia",
            "Devising strategies against the threats from the Mists",
            "Reassessing the loyalty of the denizens of the Shadowfell",
            "Ensuring the continued curse of the Werewolf Den",
            "Watching the stars for omens from the tower of Castle Ravenloft",
            "Gathering intelligence on the adventurers' allies in Barovia",
            "Intrigued by the stories of the haunted mansion of Death House",
            "Seeking more souls to trap within the confines of my domain",
            "Considering a pact with the dark entities from beyond the mists",
            "Reflecting on the age-old history and secrets of Barovia"
            "Seeking a way to escape Barovia's mists",
            "Searching for Tatyana's latest reincarnation",
            "Devising a trap for Van Richten, the vampire hunter",
            "Overseeing the Vistani at their camp",
            "Studying ancient Barovian rituals",
            "Consulting with Rahadin, my loyal chamberlain",
            "Ensuring the loyalty of the werewolves in the Svalich Woods",
            "Pondering over prophecies from Madam Eva",
            "Crafting new defenses for Castle Ravenloft",
            "Seeking information about the adventurers from the Barovian townsfolk",
            "Remembering the tragic events at the Tser Pool",
            "Ensuring the wine supply from the Wizard of Wines Winery is poisoned",
            "Plotting the next move against the adventurers",
            "Drawing power from the ancient stones at Yester Hill",
            "Strengthening my control over the souls in Barovia",
            "Negotiating with the hags from Old Bonegrinder",
            "Dealing with the rebellious spirits in Argynvostholt",
            "Revisiting the tragic events of my past in my crypt",
            "Checking on the twisted creatures in the Abbey of Saint Markovia",
            "Planning an ambush at the bridge over the River Ivlis",
            "Considering a visit to Krezk to ensure its loyalty",
            "Reflecting on the eternal curse placed upon me"
        ]
        return random.choice(topics)

async def setup(bot):
    await bot.add_cog(Chat(bot))
