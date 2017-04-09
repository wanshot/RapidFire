RapidFire
=================

.. image:: https://img.shields.io/pypi/v/rapidfire.svg
   :target: https://pypi.python.org/pypi/rapidfire

.. image:: https://img.shields.io/pypi/l/rapidfire.svg
   :target: https://pypi.python.org/pypi/rapidfire

.. image:: https://img.shields.io/pypi/wheel/rapidfire.svg
   :target: https://pypi.python.org/pypi/rapidfire

.. image:: https://img.shields.io/pypi/pyversions/rapidfire.svg
    :target: https://pypi.python.org/pypi/rapidfire

.. image:: https://circleci.com/gh/wanshot/RapidFire/tree/master.svg?style=svg
    :target: https://circleci.com/gh/wanshot/RapidFire/tree/master

SETUP
----------


- Init RapidFire

.. code-block:: shell

   $ pip install rapidfire
   $ rap --init
   $ vi /Your/home/directory/.rapidfire.d/raprc

- Set the value in RAPIDFIRE_PYFILE_PATH

::

	RAPIDFIRE_PYFILE_PATH = /path/hoge.py

- Edit sample code

.. code-block:: shell

   $ vi /path/hoge.py

.. code-block:: py

   from rapidfire import task

   @task
   def sample():
       return ['text1', 'text2', 'text3']

- Run RapidFire

.. code-block:: shell

   $ rap sample


API
--------------------------

- rapidfire.task(next_action, clipboard, per_page)
   - Parameters
      - next_action - For next_action, specify the function name to be executed next
      - clipboard - Copy the result to the cripboard
      - per_page - Lines per page

Example
--------------------------

.. code-block:: py

   from rapidfire import task

   ### Case.1
   @task(next_action='sample_method2', per_page=2)
   def sample_method1():
       return ['text1', 'text2', 'text3']

   @task(clipboard=True)
   def sample_method2():
       selected_value = sample_method1 # The value selected by sample_method1 is entered
       return ['{} is selected'.format(selected_value)]


.. code-block:: shell

   $ rap sample_method1
