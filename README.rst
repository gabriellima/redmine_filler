Redmine Filler
==============

Are you tired of 'cornal' stuff on Redmine? Have you postponed all that working time and tasks into Redmine?

So this is for you!

Installation
-------------

::

    git clone git@github.com:gabriellima/redmine_filler.git

Observations
-------------

This is a first release, without placing things in their places.

So try to not judge this harshly, yet.

Also, for now, desconsider things at 'Pre-Setup' tutorial, because settings are all under `redmine.py`, instead of `settings.py`.

Pre-Setup
-------------

Edit file `settings.py` changing params

Explanations before running
---------------------------

First edit `helper_issue_dict` under `redmine.py`, putting your data to create some issue, if you need to create some.

This will be required until I realise good way to convert some input to unicode.

Also, please note that in my case, my project url is this one:

    `http://my_redmine.com/projects/aos/`

So, my `url` is `'http://my_redmine.com/'`, and my `project_id` is `'aos'`.

Also, sadly my url to create new issues is not the default one:

    `http://my_redmine.com/projects/aos/issues/new`

Mine new-issue url is a little different, requiring a custom 'eap_id' param, like in this url:

    `http://my_redmine.com/projects/aos/issues/new?eap_id=224`

So, I also pass it into `Redmine` constructor, in order to correctly create new issues.


Running
----------

* **Import redmine_filler.Redmine and helper to create new issues**

    ::

        from redmine_filler.redmine import Redmine, helper_issue_dict

* **Open redmine**

    ::

        r = Redmine('http://my_redmine.com/','user', 'pass','aos','eap_id=224')

* **Create new issue and return its id**

    ::

        issue_id = r.create_issue(stop_before_commit=True,**helper_issue_dict)

    Ps: I just set 'stop_before_commit' to True so that I can analyze
    the browser window before saving the new issue

* **Automatically fill the time between '2011-08-08' and '2011-09-02', with 4 working hours per day**

    ::

        r.fill_time(issue_id,'2011-08-08','2011-09-02','4')

