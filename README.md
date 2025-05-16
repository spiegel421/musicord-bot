# musicord-bot

The once-official bot of the /r/Music Discord server, while I moderated there.

Note addressed to the reviewers of my job application at GitLab.

Though much of the recent work I've done has been proprietary, I have linked, here, a GitHub project, dating quite a while back, pre-employment in college. I was constructing a Discord bot that provided custom music recommendations, exclusive to users of that server, based on their music consumption habits from numerous websites.

These included both last.fm and RateYourMusic.com.

I intensively and extensively researched ML recommender systems, and derived "listening similarity measures" callable to the bot.

As well as top-recommended artists, albums, etc., based on prior listening.

At one point, I had desgned a web crawler designed to gather data from RateYourMusic.com.

This technically went against the website's crawling policy.

So, I also wrote code to try to reduce the timespan of successive calls by the crawler to the site, so the bot wouldn't get my IP banned.

This proved insufficient. I eventually set up a remote EC2 instance over AWS that regularly changed IP addresses to those usually expected from regular visitors.

I kept this going for a while.

I would not do something that violates site policy like that again. But, at the time, I felt it not immoral, because finding out new music ought to available to everybody.

I'm unsure how much of the code persists in this GitHub repo, but figured I'd at least link to a written explanation.

I really like finding ways to make new things.
