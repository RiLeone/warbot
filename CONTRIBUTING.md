# Contributing

In order to facilitate everybody's work, contributors are asked to follow these
guidelines when developing code for `warbot`.


## Python Styleguide

As a baseline, try to adhere to PEP8 https://www.python.org/dev/peps/pep-0008/.
Exceptions can be made where they make sense.

### In a Nutshell

In a nutshell, we can summarize the guidelines as follows:

* Use four spaces for indentation. Do not use tabs. Setup your editor accordingly.
* Name classes using `CapitalCamelTyping`, use underscores for `naming_methods_and_functions_and_variables`.
* Give exhaustive names to everything. "The name is too long to type" is not a valid excuse for not giving a proper name. Even in `for`-loops, e.g. DO `for line in lines:` and not `for i in lines:`
* Functions and methods should contain verbs in their names, like `get`, `set`, `compute`, and so on, depending on what they actually do.
* Optionally, class attribute names can start with an underscore `_` so to immediately distinguish them from methods.
* Write docstrings and annotate your code.
* Separate code blocks with single blank lines. Separate `def` blocks with two blank lines. Separate `class` blocks with three blank lines.
* Implement tests for each method and function you write.
* Use the `if __name__ == "__main__":` part of modules to perform basic functionality tests.
* Your code should read as much as possible as English.
* Put one space before and one after operators mathematical an logical operators, e.g. `+ - * / = == === < > <= >= != ** += -= *= /= & ¦`.
* Put one space immediately after `, : ;`, like you would do while writing a text.
* Do not put any space:
  * Right before parenthesis or brackets `() [] {}`.
  * Immediately inside parenthesis or brackets.
  * To vertically align things.
* Avoid inline `if/while/for` routines, e.g. AVOID  `if condition: do_that()`, all on the same line.
* Keep your code structured and write your own modules.

Of course, as stated in https://pymbook.readthedocs.io/en/latest/pep8.html:
> **Two good reasons to break a particular rule**: *1)* When applying the rule would make the code less readable, even for someone who is used to reading code that follows the rules. To be consistent with surrounding code that also breaks it (maybe for historic reasons) – although this is also an opportunity to clean up someone else’s mess (in true XP style); *2)* When applying the rule would make the code less readable, even for someone who is used to reading code that follows the rules. To be consistent with surrounding code that also breaks it (maybe for historic reasons) – although this is also an opportunity to clean up someone else’s mess (in true XP style).


## Unit Testing

Try to alway develop tests for your code as you proceed with the development.
Doing this in a consistent manner allows for the tests to always be up to date
and also makes the tests effective, as they will trigger appropriate inspections
if and when they start to fail.

**Write a test for each feature you develop.**


### Commented Code

Once you are done with a specific feature development and its testing, please
delete all commented-out code. It is useless, ugly, and confusing to other users
to keep code there in a commented form. If some code might be useful at some
point find an alternative way to make it conditional, add it to the `playground`
or add it to the snippets, but **do not leave it in the code itself**.

Remember:
> **Deleted code is debugged code**


## Submitting Issues and Repository Branching

It is advised that you create your own branch for experimental developing, but
also not to focus/rely too much on working on this branch. Instead, you are
asked to submit an issue for each bug/feature improvement you and the team find
and then **create a dedicated branch for said issue when working on it**. So, the
workflow in terms of development in this repository is the following (assuming
you just found a new issue):
1. **Open an issue** where you describe the problem and what has to be done to solve it. You can also specify who should take care of it (will most likely be yourself), to which milestone the issue is part of and what the deadline for the issue is.
2. For sake of argument, let's assume you just created the issue: *Issue 42: Filtering Bug*. Then you have to **create**, from the `master`, **the new branch** `iss42`. Check it out and start working on it.
3. As you start working on it, **add the "doing" label to it**.
4. Once you are done with your issue, i.e. you tested it thoroughly, you shall open a **pull-request**.
5. **Mark the issue as closed** and done once the request has been accepted and merge to master has occurred.
6. Tackle the next issue or create a new one and then tackle it.
