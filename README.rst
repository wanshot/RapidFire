RapidFire
=================

SETUP
----------

- Init RapidFire

.. code-block:: shell

   $ rap --init
   $ vi /your/home/directory/.rapidfire.d/raprc

- Set the value in RAPIDFIRE_PYFILE_PATH

::

	RAPIDFIRE_PYFILE_PATH = /path/hoge.py

- Create Python file

.. code-block:: shell

   $ vi /path/hoge.py

- Edit sample code

.. code-block:: py

   from rapidfire import render

   @render
   def sample():
       return ['text1', 'text2', 'text3']

- Run RapidFire

.. code-block:: shell

   $ rap sample


API
--------------------------

- render
   - Execute the selected result with Shell
   - next_action option
      - For next_action, specify the function name to be executed next
   - clipboard option
      - Copy the result to the cripboard

- example

.. code-block:: py

   from rapidfire import render

   @render(next_action='sample1')
   def sample_method1():
       return ['text1', 'text2', 'text3']


   @render(clipboard=True)
   def sample_method2():
       text = sample_method1 # The value selected by sample_method1 is entered
       return ['{} is selected'.format(text)]
