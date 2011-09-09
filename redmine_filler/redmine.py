#-*- coding:utf-8 -*-
from splinter.browser import Browser
from redmine_filler.settings import *
from time import strptime
import datetime

helper_issue_dict = {"tracker_id": "",
                     "subject": "",
                     "description": "",
                     "assigned_to_id": "",
                     "start_date": "",
                     "due_date": "",
                    }

helper_issue_dict['assigned_to_id']=u'Gabriel Oliveira'
helper_issue_dict['description']=u'Checar se há comportamentos implementados pelo javascript utilizado pelo UNG (principalmente os métodos necessários apenas para a página inicial), e que estão sendo executados também em locais desnecessários (como as páginas de texto, tabela e ilustração), entre outras'
helper_issue_dict['due_date']=u'2011-09-02'
helper_issue_dict['start_date']=u'2011-08-08'
helper_issue_dict['subject']=u'Checar métodos do UNG javascript que estão sendo executados em locais desnecessários'
helper_issue_dict['tracker_id']=u'Codificação';

class Redmine(object):

    def __init__(self, url, login, password, project,
                                                   custom_project_params=None):
        """ This will open redmine page, and then login

            url: your redmine url
            login: your redmine login
            password: your redmine password
            project: the id of your project
            custom_project_params: some custom parameters to pass into projects
                url, in order to create a new issue
        """
        if not url.endswith('/'):
            url += '/'
        self._url = url
        self._login = login
        self._password = password
        self._project = project
        self._custom_project_params = custom_project_params

        self._browser = Browser()
        self._do_login()

    def _do_login(self):
        self._browser.visit(self._url + LOGIN_URL)
        self._browser.fill('username', self._login)
        self._browser.fill('password', self._password)
        self._browser.find_by_name('login').first.click()

    def create_issue(self, stop_before_commit=False, **issue_fields):
        """ Create a new issue into your redmine.

        This is an awesome (crazy) method. Pay attention:

        - You need to pass at least the required fields of your redmine.
          * For instance, if my redmine requires a title, and this field has the
          name:
                'issue[subject]'

          than I must pass my title as follows:
               create_issue(subject='My name')

        - You can also pass the name of other fields you'd like to fill,
          remembering to just pass the inner content of the field's name.
          For example, in this case:
                'issue[another_field]'
          The parameter would be:
              create_issue(another_field='My content')

        - As an example, in a default Redmine, I think this are the default
          required parameters that you must pass:
              create_issue(tracker_id, subject, description, assigned_to_id,
                           start_date, due_date, estimated_hours)

        - stop_before_commit is a flag, used when you have some extra fields that
          are not yet handled by this method, so you need to deal with it by
          hand. In this cases, call this method like this:
              create_issue(do_not_commit=True)

          And the method will just fill the fields you passed, without clicking
          'commit' button.

        - IMPORTANT: Scenarios that contains custom fields are also covered.
          A custom field has its name as something like:
              'issue[custom_field_values][20]'

          In this cases, you must pass a 'custom_field_values' parameter as a dict,
          where the key is the number of the field, and the value is the content
          you want. In this example, the parameter would be as follows:
              create_issue(custom_field_values={'20': 'My content'})

          Then the method will do the rest.
        """
        new_issue_url = self._url + PROJECT_TAG + '/' + self._project + '/issues/new'
        if self._custom_project_params:
            new_issue_url += '?%s' % self._custom_project_params
        self._browser.visit(new_issue_url)

        def fill_custom_field(field_id, field_value):
            for custom_field_number, custom_field_value in field_value.items():
                self._browser.fill(ISSUE_TAG + '[%s][%s]' % (field_id,
                    custom_field_number), custom_field_value)
        for field_id, field_value in issue_fields.items():
            if type(field_value) == type({}):
                fill_custom_field(field_id, field_value)
            else:
                self._browser.fill(ISSUE_TAG + '[%s]' % field_id, field_value)

        if not stop_before_commit:
            self._browser.find_by_name('commit').first.click()
        # TODO: find 'task_id' to return
        # (the last number under page url may be this)

    def fill_time(self, issue_id, start_date, end_date, time_per_day):
        """ Fill time into some issue that already exists.

            issue_id: id of the existing issue
            start_date: date to start filling in time
            end_date: date to end filling in time (self-including)

        - Pass start and end date as YYYY-MM-DD format, like on this example:

            fill_time(1, start_date="2011-04-23", end_date="2011-04-27", 4)

          Following this example, after method is run, the issue with id '1'
          will have, from monday to friday (2011/04/23, 2011/04/27), a new
          working time, with value 4 (4 hours), with a total of 20 hours worked
          on the week.
        """
        def discover_working_days(start_date, end_date, time_per_day):
            # format date
            start_date = strptime(start_date, '%Y-%m-%d')
            end_date = strptime(end_date, '%Y-%m-%d')
            # convert date to datetime
            start_date = datetime.date(start_date.tm_year, start_date.tm_mon,
                                                             start_date.tm_mday)
            end_date = datetime.date(end_date.tm_year, end_date.tm_mon,
                                                               end_date.tm_mday)

            working_days = []
            total_number_of_days = (end_date - start_date).days + 1

            current_date = start_date
            for day in range(total_number_of_days):
                if current_date.isoweekday() in range(1, 6): # working day [1,2,3,4,5]
                    date = current_date.strftime('%Y-%m-%d')
                    working_days.append((date, time_per_day))
                current_date = datetime.timedelta(days=1) + current_date

            return working_days

        working_days = discover_working_days(start_date, end_date, time_per_day)
        # like: [("2011-03-14", 4), ("2011-03-15", 4), .....]

        new_time_url = self._url + ISSUE_TAG + 's/' + issue_id + '/' + TIME_URL
        for date, hour in working_days:
            self._browser.visit(new_time_url)
            self._browser.fill(TIME_TAG + '[spent_on]', str(date)) # "2011-03-14"
            self._browser.fill(TIME_TAG + '[hours]', str(hour))
            self._browser.find_by_name('commit').first.click()

    def close_issue(self, issue_id):
        issue_url = ISSUE_TAG + 's/' + issue_id
        self._browser.open(self._url + issue_url)
        self._browser.find_link_by_partial_href(issue_url + '/edit').first.click()
        self._browser.select(ISSUE_TAG + '[done_ratio]', "label=100 %")
        self._browser.select(ISSUE_TAG + '[status_id]', "label=Resolvido")
        self._browser.find_by_name('commit').first.click()

