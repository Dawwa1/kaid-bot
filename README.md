## Kaid Bot

Kaid is a multipurpose bot, designed to be easy to use and easy to understand!

## Installation

Clone the folder, and install everything in requirments.txt

```bash
pip install -r requirements.txt
```

---
## To Do
https://trello.com/b/2K0Z4Jul/kaid-bot

## Configuration

Configuring the bot is pretty self explanatory

```toml
token = "" #Put your discord bot token here
guildID = 980870866638340166 #The id of your guild
prefix = "!" #The prefix for your bot

[on_join]
enabled = false #enable on join messages
welcomeChannel = 980870867145871412 # if enabled, will send welcome messages to this channel
welcomeMessage = "pls welcome {member} to the server!" #Welcome message. Placeholders are {member} and {guild}
roleOnJoin = 997412646523523102 #The role that it will give on join


[economy]
enabled = true #enable the economy features

[economy.cooldown]
# in minutes
workCooldown = 10 
begCooldown = 5
slutCooldown = 15
```
---

To start the bot, either double click on main.py or open it with command prompt

```bash
python main.py
```
## Commands
Since this bot is a WIP, the commands are always changing! This are the current ones
---

###### Economy Commands
-bal : Check you account balance

-work : Work legally and earn money!

-beg : Hustle on the streets for a lil bit of cash.

-slut : Solicit people on the streets. High risk, high reward!

-guess {choice} {amt} - If you choose the same number as the bot, you win money!

###### Admin Economy Commands
-eco {action} {account id} {amt} : Remove or add money and remove or add xp

-createAccountForMembers : Creates an account for any member that doesn't have one.

###### General admin commands
-lock {role name - OPTIONAL} : Lock the channel for everyone, or for a specific role

-unlock {role name - OPTIONAL} : Unlocks the channel for everyone, or for specified role

-clear {number of messages - OPTIONAL} : Deletes the specified number of messages in a channel. If not specified, deletes 5000.

###### Other
-help : Shows the available commands

---

## Contributing
If you want to contribute to this project, your welcome to open a pull request!

## License
MIT License

Copyright (c) 2022 Dawwa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
