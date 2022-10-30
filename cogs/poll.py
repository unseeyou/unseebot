import requests
from discord.ext import commands

ENDPOINT = "https://api.strawpoll.com/v3"
API_KEY = 'unseebot'


class PollCommands(commands.Cog):
    @commands.hybrid_command(description='create a poll! split options with a semicolon (;)')
    async def createpoll(self, ctx, poll_title: str, poll_description: str, poll_options: str):
        option_list = poll_options.split(';')
        options = []
        for i in option_list:
            option = {
                "type": "text",
                "value": i
            }
            options.append(option)
        payload = {
            "title": poll_title,
            "media": None,
            "poll_options": options,
            "poll_config": {
                "is_private": False,
                "vote_type": "default",
                "allow_comments": True,
                "allow_indeterminate": False,
                "allow_other_option": False,
                "custom_design_colors": None,
                "deadline_at": None,
                "duplication_checking": "ip",
                "allow_vpn_users": False,
                "edit_vote_permissions": "nobody",
                "force_appearance": None,
                "hide_participants": False,
                "is_multiple_choice": False,
                "multiple_choice_min": None,
                "multiple_choice_max": None,
                "number_of_winners": 1,
                "randomize_options": False,
                "require_voter_names": False,
                "results_visibility": "always",
                "use_custom_design": False
            },
            "poll_meta": {
                "description": poll_description,
                "location": None,
            },
            "type": "multiple_choice",
        }

        response = requests.post(ENDPOINT + '/polls', json=payload, headers={'X-API-KEY': API_KEY})

        if response:
            poll = response.json()  # response is Poll object
            await ctx.send(f'Success! click here to vote -> {poll["url"]}')
        else:
            print('ERROR')
            error = response.json()
            print(error)
            await ctx.send(error)


async def setup(bot):
    await bot.add_cog(PollCommands(bot))
