## Preface
This question has begun to plague the internet more and more each coming day. You can barely browse YouTube without being confronted with multiple advertisements telling you their website has the answer. The question: "Am I gay?" Most of these tests are nothing more than a few questions with either incredibly blatant infograbs about your age and gender or awfuly random inquiries about your favorite Disney movie. None of them seemed to combine both the aspects of entertainment and accuracy, and all of them seemed to use far to simple an agorithm to determine sexuality. How would I know the algorithm is too simple? Well...

*I am not gay.* Many of my friends insist I am. I tell them they are wrong and I'm just effeminate. They respond telling me that it's okay to be who I am and they're here to support me when I come out of the closet. To worsen the situation, every single "Am I gay?" test I take comes back saying that I'm gay. This is *clearly* an issue with the quality of the tests and not me failing to realize my true self. From this I set off to create perhaps the most mathematically advanced "Am I gay?" test there is for the sole purpose of making sure I'm not gay.

Now, you may be asking, "why did you make it for the TI 84 Plus CE instead of some better more accesibly platform like ... the web?" First off, the TI 84 Plus CE is the best platform to ever exist, and second off, I am almost *in love* with my calculator. If you ask my friends to say something about me, there is a high chance it will be about my calculator. I take it *everywhere*: to school (obviously), to the movies, to football games, the list goes on. One day at marching band, someone suggested that I add a gay quiz to my calculator as a joke. I of course immediately realized the immense potential this had and decided to go make the joke a reality.

## Creation

Now that you have the overall idea behind my motivation to create this I can start on the specifics. For the TI-84 Plus CE side of things, I wrote this in C using the [CE C/C++ Toolchain](https://github.com/CE-Programming/toolchain) which allows easy access to useful methods for displaying information to the calculator screen. Most of the graphics are done simply using the toolchain's built in str display functions. I do avoid clearing the screen, as that causes flickering, and instead prefer writing over the previous screen and adding whitespace to fill every line. This creates a much less flickery experience.

I wanted to create a quiz that would just ask you, the quiz taker, a few multiple choice questions and would then give you a nice percentage breakdown of your predicted sexuality with the possibilities being gay, bisexual, and straight. Basically, if you were to get 70% straight and 30% gay, that would mean you answered 70% of the questions like you were straight and 30% like you were gay. This is not straight forward, as some of the questions could have absolutely no assosiation with sexuality, while some could be answered by multiple sexualities the same way. If we want to accurately measure these proportions and prove once and for all that *I am not gay*, we're going to need an aglorithm.

## Algorithm

*Note: This is the meat and potatoes of this article, but if you aren't really into technical stuff, just skip down to the [questions](#Questions) section.*

For the algorithm, for simplification, someone can have same-sex feelings, or opposite-sex feelings. This means each question can give away the info that they have same-sex feelings, do not have same-sex feelings, have opposite-sex feelings, and/or do not have opposite-sex feelings.

|sexuality|same-sex|opposite-sex|
|-|-|-|
|gay|true|false|
|bisexual|true|true|
|straight|false|true|

I do not have asexuality programmed in on this test and do not really plan to do so as it would be quite a bit of a pain to add to the program at this point.

This table shows how the different response weights are treated by the program.

|weight|gay|bi|cis|
|-|-|-|-|
|nil|maybe|maybe|maybe|
|gay|true|false|false|
|bi|false|true|false|
|cis|false|false|true|
|cisbi|false|maybe|maybe|
|cisgay|maybe|false|maybe|
|bigay|maybe|maybe|false|

For calculating the final percentages, I have two rules:
 - If a person answers a question, the way they responded to that question in the final percents is some combination of all the possibilites of its maybes, e.g. a cisgay weight comes out to be some portion cis and some portion gay.
 - That portion is the same for each question and is determined by the final portions that are returned at the end of the test.

From this we can create recursive equations to solve for the final gay portions, bisexual portions, and straight portions.

$P_a$ is the final straight portion, $P_b$ is the final bisexual portion, and $P_c$ is the final gay portion. $C_a$ is the number of cis weighted responses, $C_b$ is the number of bi weighted responses, and $C_c$ is the number of gay weighted responses. Variables like $C_{ac}$, $C_{ab}$, $C_{bc}$, and $C_{abc}$ are combined weights and are the number of cisgay, cisbi, bigay, and nil weighted responses respectively. $C$ is the total number of responses.

Below is a system of equations that could theoretically be solved to give exact answers for the three portions system.

$$\left(C_a + \frac{C_{ab} \cdot P_a}{P_a + P_b} + \frac{C_{ac} \cdot P_a}{P_a + P_c} + C_{abc} \cdot P_a\right)=P_a \cdot C$$

$$\left(C_b + \frac{C_{ab} \cdot P_b}{P_a + P_b} + \frac{C_{bc} \cdot P_b}{P_b + P_c} + C_{abc} \cdot P_b\right)=P_b \cdot C$$

$$\left(C_c + \frac{C_{ac} \cdot P_c}{P_a + P_c} + \frac{C_{ac} \cdot P_c}{P_a + P_c} + C_{abc} \cdot P_c\right)=P_c \cdot C$$

$$P_a + P_b + P_c = 1$$
I have not solved it.

Theoretically it should be solvable as there are only three unknowns, $P_a$, $P_b$, and $P_c$, and there are at least 3 equations. 
I am not sure the fourth equation is neccesary to solve the system, but I am not an expert at this sort of thing either. 
What we can do is plug in guess unknowns on the left sides of the first three equations, and then calculate what that would make the unknowns on the right sides. We can then use these new unknowns as our new guess unknowns and repeat. This will converge to a set of portions which solve the system and is the system I use in this program. In practice, this solution works very well and will usually give highly accurate solutions to the equation after only 10 iterations through the equations. Additionally, it only requires 3 of the equations to use the recursive method, proving that the fourth equation is redundant.

## Questions
Now this is just the algorithm of course, we still need to get questions for the quiz. For this I played the easy move and took most of them from [this quiz](https://www.arealme.com/gay-test/en/), however some answers and questions have been modified. Because the online quiz does not show the weights of the answers to each question, I had to choose my own weights. Those are all simply stored in a two dimensional array along with the 11 questions and their possible answers.

## Finale
The Gay Quiz TI was both a success and a faliure. I showed the quiz to a multitude of my friends, and every single one found it quite fun. The calculator form is a great hook. "Would you take this online gay test?" just doesn't have the same ring as, "My calculator will calculate how gay you are." The number of people who ended up taking the test on my calculator is *ridiculous* and probably close to 80 people. Quite a few of those people asked me actively to take the test, and since I *always* have my calculator on me, I was able to let them take it as well.

Irony pulled a cruel trick on me through this project. To put it simply, I tried to make the most accurate gay test I could, I poured my mathematical heart and soul into it, and it *betrayed* me. My results are 82.3% gay, 17.6% bisexual, and 0.1% straight. Maybe betray is a harsh word to use here. Perhaps I did succeed in making a perfect test after all. Perhaps my friends and the tests and my systems of equations could see what I was blind to all along. Maybe it's time I read the writing on the wall and realize that the programs weren't wrong about me. I was.

*Nahhhh...*  

The program's probably just wrong. I mean, I can't possibly be *gay*.

Right?

---
This article is somewhat adapted from the readme on the [GitHub page](https://github.com/mmilunicmobile/gay-quiz-ti) for this program. You can download it and run it on your own TI-84 Plus CE and look at the code for your own enjoyment. Again, all thanks to the wonderful contributors on the [CE C/C++ Toolchain](https://github.com/CE-Programming/toolchain)! Without their work this wouldn't have been made.