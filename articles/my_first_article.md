I can write my own articles and stuff! After all my hard work of stealing people's code from online and copying it into my shoddy PHP mockery of a program, I have something I can run! I mean, it does what I have asked of it. It also gives off vibes of the old internet, which I personally love. It pretty much displays the articles I want it too and it generates markdown HTML for the articles. I guess now would be a good time to describe both how it works and what it can do at the same time, so here it goes.

## How it works and what it can do at the same time.

Look at that! A subheading or whatever the heck that thing is called. This whole page is made using the great tool [Parsedown](https://parsedown.org/). Parsedown is a markdown processor written for PHP, and takes all the articles I have written in markdown and converts them to usable HTML code that can be displyed in the browser. Since each individual element such as a header or a paragraph has a different element in HTML because of Parsedown processor, the themeing can look how I like simply though the use of generic CSS. Additionally, since the program is stored as a file in my project, I can edit the Parsedown code to add features such as [MathJax](https://www.mathjax.org/) support, though I have not gotten around to doing that anyway.

$$\ln(\text{test} )= e^{\pi \cdot i \cdot \text{works}}$$

*Nevermind. It was really easy to get it working! Now I can $y = mx + b$ all over the place!*

Other than the markdown file processing, the only code is just PHP to find all of the articles in an XML file and then publish only the ones I have listed with the published attribute. Eventually, all this code will hopefully be open source so you readers can point out all of my security flaws and detail exactly how you would hack this website to bits.

## Conclusion

Honestly, for a first article, this was kind of trash. Check out my other web projects or something like that. Hopefully when you are reading this, they will all be listed under the same domain that way they act nicely together.