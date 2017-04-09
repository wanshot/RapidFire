RapidFire
=================

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
      - clipboard option - Copy the result to the cripboard
      - per_page - Lines per page

Example
--------------------------

.. code-block:: py

   from rapidfire import task

   @task(next_action='sample_method2', per_page=2)
   def sample_method1():
       return ['text1', 'text2', 'text3']


   @task(clipboard=True)
   def sample_method2():
       text = sample_method1 # The value selected by sample_method1 is entered
       return ['{} is selected'.format(text)]
