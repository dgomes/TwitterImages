===============
 twitterimages
===============

Twitter Bot to post random images from a directory



Requirements
============

* Python 3
* Tweepy
* SqlAlchemy

Features
========

* ToDo: Rewrite me.

Setup
=====

::

  $ pip install --user twitterimages
  or
  (venv)$ pip install twitterimages

Usage
=====

::

  $ python twitterimages --sync
  to load images from the image_dir to the database

  $ python twitterimages --post
  to post next least posted image

  $ python twitterimages
  just look for replies and update captions

