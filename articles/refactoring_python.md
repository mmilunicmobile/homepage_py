This has been in the works for a while, but after a significant amount of refactoring, a beach vacation, a little tinkering, and a lot of obsessing over optimizations, I can finally say that my site is **fully Python powered**! 

<p align="center">
  <img src="../static/images/python-powered.png" width="200px" height = "80px" alt="a picture of the python powered logo"/>
</p>

Well... *mostly Python powered*.

## Structure

The site is now composed of a [Flask backend](https://palletsprojects.com/p/flask/) which combined with [Frozen-Flask](https://frozen-flask.readthedocs.io/en/latest/) allows me to properly render my pages statically. This way, not only do I not have to rerender each article every time it is accessed, but I can also deploy to a solution like [Github Pages](https://pages.github.com/) and have my website be easily accessed 24/7 without having to keep a Raspberry Pi running in my basement. 😃

The articles are still stored as Markdown, but the config file for the site is now a YAML file, making it much easier to edit than the previous XML file.

## One more thing...

I also hooked up the backend to be able to integrate [SolidJS](https://docs.solidjs.com/) with the help of [solid-element](https://github.com/solidjs/solid/tree/main/packages/solid-element) so I am able to simply integrate custom HTML web components wherever I want in my pages (including in Markdown). That allows me to do cool things like making this quote cycle through different famous quotes when you click/tap on it.

> <custom-quote></custom-quote>

See! Isn't that cool! By using SolidJS and solid-element I can also keep it very, very lightweight (and I get to say I use SolidJS).

## Why this is actually a mess

The issue is, I wasn't quite satisfied with my web components because they took a few milliseconds to load. *Not that this is a big deal*, but it did cause some page rearangement for a few tenths of a second. And this page drifting is **unnaceptable**. (So I guess it is kinda a big deal.) My fix was to figure out that I can just embed a `<template shadowrootmode="open">contents...<\template>` with whatever element I was eventually going to be creating inside the markdown. This made it so there was no more page shifting. 

The code on this page would look something like this:

<code-quote></code-quote>

(*Do you see how that part's reactive too?! Its sooooo cool.*)

But it still wasn't enough.

_I wanted it to be better._

One small issue that still remained (at least in my head) was that if you were to make a more complicated component that it would start to get tedious to constantly keep copying back and forth the code for the component. Wouldn't it be nice if you could have Flask or Python figure out how to replace a simple tag like `<custom-quote></custom-quote>` with a fully server side rendered component? Yes. It would be very nice. This lead to me spending hours and hours trying to figure out how to use the Vite build tool to somehow transmit built components to Python. Eventually I figured out that I could use the built in server side rendering part of SolidJS to render the components in a Node routine. This routine would then store a JSON file into a dictionary for each JavaScript file and then inside of those a dictionary with each filled out component.

All this so I could get a straight 0 on my Cumulative Layout Shift from Lighthouse. 😭

Anyway, thanks for reading my article. I hope you enjoy your day and I hope you enjoyed clicking/tapping on the quote <count-quote></count-quote>!

---
You should be able to find all the code for this on my [GitHub page](https://github.com/mmilunicmobile/homepage_py) for it. Don't do what I did though. It's not a good example.