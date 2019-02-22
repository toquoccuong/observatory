=================
Contributor guide
=================
Thanks for your interest in contributing to observatory!

The following is a set of guidelines for contributing to observatory.
These are not set in stone, use your own best judgement when making pull requests.
Feel free to propose changes to this document by submitting an issue and pull request!

.. contents:: Table of contents
    :depth: 3

What should I know before I start?
==================================

Program Design
--------------
Observatory is a fully featured python PIP package. You can learn about the 
design of our tool on the `Wiki <https://github.com/wmeints/observatory/wiki>`_.

Design decisions
----------------
Any significant design desicions are documented on the wiki as well.
We're using Architecture Decision Record (ADR) style documentation for this.
Please read all about this way of working on 
`Micheal Nygard's blog <http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions>`_.

Please refer to `the wiki <https://github.com/wmeints/observatory/wiki>`_ for an overview of the design decisions.

How can I contribute?
=====================

Reporting bugs
--------------
Sometimes observatory just doesn't work as expected. We understand that it can be very
frustracting when it acts up. Please follow these guidelines to help us triage and fix 
issues as fast as possible.

What should I do before submitting an issue?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Check for error messages** When we have a clear error message we can locate the problem faster.
- **Check your code without using tracking** to make sure that it's us and not a problem with your code.
- **Search for your issue** to make sure that it hasn't been reported before.

How do I submit an issue?
~~~~~~~~~~~~~~~~~~~~~~~~~
We track bugs as `Github issues <https://github.com/wmeints/observatory/issues>`_.
Please file an issue there following these guidelines:

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe how we can reproduce the problem** in as much detail as possible 
  including step-by-step instructions if you can.
- **Provide an example** so we don't need to build one ourselves. This 
  saves valuable time debugging the problem. Make sure that it is small and includes
  links to datasets that we might need. It's even better if we don't need any data at all.
- **Describe the observed behavior** to help us understand the problem. 
- **Describe the expected behavior** so we can work towards a solution.
- **Include any error messages and stacktraces** so we can locate where in 
  the code the problem is occurring.

Please enhance your issue with the following information:

- **Did it start to happen recently?** As we may have uploaded a faulty release.
- **Can you reliably reproduce the problem?** If not, please include how often it happens.
- **What OS are you running on?** As the problem may be related to linux/windows issues.
- **What version of python are you using?** So we can find out whether it is a python specific problem.

Suggesting enhancements
-----------------------
Are you missing a feature in observatory that you feel is important? These guidelines
provide you with the information you need to submit your suggestion to us.

What should I do before submitting an enhancement?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **Check the documentation** your feature may already be available.
- **Search for your enhancement in the issues list** and make sure that it hasn't been suggested before.

How do I submit an enhancement suggestion?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We track enhancements as `Github issues <https://github.com/wmeints/observatory/issues>`_.
Please file an issue there following these guidelines:

- **Provide a clear and descriptive title** for the issue to identify the ehancement.
- **Explain why the enhancement is useful** so we can make a decision to accept/reject the idea.
- **Provide steps that describe how the enhancement should work** so we know the expected behavior.
- **Provide a description of behavior that needs to be replaced** in case you want to change existing behavior.

Submitting your first pull request
----------------------------------
Are you unsure where to begin contributing to observatory? 
We add labels to issues that are good candidates to start with:

- `Good first issues <https://github.com/wmeints/observatory/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22>`_
- `Help wanted issues <https://github.com/wmeints/observatory/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22>`_

Local development
~~~~~~~~~~~~~~~~~
You can work on observatory on your local computer. Please check 
`the wiki <https://github.com/wmeints/observatory/wiki>`_ for specific development instructions.

Debugging observatory
~~~~~~~~~~~~~~~~~~~~~
You can debug observatory on your local computer. Please check 
`the wiki <https://github.com/wmeints/observatory/wiki>`_ for specific development instructions.

Pull requests
-------------
We use pull requests extensively in our development process. They help us achieve the following goals:

- Maintain the quality of the code base through automated builds and tests
- Fix problems that are important to our users
- Engage the community to build a useful product
- Enable a sustainable system that is easy to maintain by the people working on the software.

Please follow these guidelines when submitting a pull request:

- Describe the change, what are you changing in the pull request? 
- Tell us which issue the pull request is for so we can discuss the design of the change
  before we start to work on the code.
- Follow `Style guides`_ to ensure that the code is uniform.
- Please make sure all checks pass

Backlog structure
=================
Managing a backlog on github can be challenging. It's near impossible to have a parent-child
relationship in issues. Also, it can get quite messy if you're not using the right labels, etc.

We've chosen a specific structure to manage our backlog and a set of status flags to manage
progress on our project. Please feel free to contribute your ideas if something is unclear.

Themes, Epics, Features
-----------------------
Every now and then we pick up a few themes around which we'll improve the observatory product.
You can find these themes in the repository by search for specific :code:`theme:<theme-name>` labels.

As with any software product, observatory has a few large chunks of functionality that we build.
We call these epics and you can find them on the backlog by searching for the `epic` label.

Finally, we have features as the lowest level of describing individual features in the software.
You can search for the `features` label to get an overview of all the features we're working on.

Status flags
------------
All issues are marked with a status flag to indicate what we're currently working on.

- :code:`status:accepted`: Indicates the issue is accepted and on the backlog for a future release.
- :code:`status:blocked`: Indicates that there's a problem with the issue that we need to resolve.
- :code:`status:available`: Indicates that the issue is ready for development.
- :code:`status:in-progress`: Indicates that the issue is currently being worked on.
- :code:`status:review-needed`: Indicates that an issue is completed but needs a review.
- :code:`status:revision-needed`: Indicates that the review is completed and that we need to fix a few issues.

Additional labels
-----------------
We have a few additional labels that we use:

- :code:`good first issue`: Indicates that this is something a beginning developer can pick up.
- :code:`help wanted`: Indicates that this is a nice to have feature and we need your help to complete it.
- :code:`invalid`: Indicates that the issue has some kind of problem with it and we dumped it.

It's always good to read the issue description in case you're wondering what is going on
for that specific issue. We sometimes mark issues as invalid, we do this to clean up the backlog. 

Style guides
============

Commit message guidelines
-------------------------
We're using conventional commits based on the 
`Angular way of working <https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit>`_.

Python style guide
------------------
We're following the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide for Python code.
When you're using Pycharm or Visual Studio Code you can use the standard formatting shortcuts to
automatically format your code according to this style.
