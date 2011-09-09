#coding: utf-8
from selenium import selenium
import unittest
from time import strptime
import datetime

class RedmineFiller(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "https://redmine.renapi.gov.br/issues/22464")
        self.selenium.start()

    def test_criar_tarefa(self): #, titulo_da_tarefa, descricao_da_tarefa, dono_da_tarefa, data_inicial, data_final, tempo_estimado_da_tarefa, nucleo, preencher_tempos=False, fechar_tarefa=False):

        titulo_da_tarefa = u"Adicionar **kw ao web_service"
        descricao_da_tarefa = u"adicionar **kw ao web_service"
        dono_da_tarefa = "gabriel.oliveira"
        data_inicial = "2011-04-23"
        data_final = "2011-04-27"
        tempo_estimado_da_tarefa = 20 #em horas
        nucleo = "IFF"
        preencher_tempos = True
        fechar_tarefa = True

        sel = self.selenium
        sel.open("22464")
        import ipdb;ipdb.set_trace()
        sel.click("link=Nova tarefa")
        sel.wait_for_page_to_load("30000")
        sel.select("issue_tracker_id", u"label=Codificação")
        sel.type("issue_subject", titulo_da_tarefa)
        sel.type("issue_description", descricao_da_tarefa)
        sel.select("issue_assigned_to_id", "label=%s" % dono_da_tarefa)
        sel.type("//input[@id='issue_start_date']", data_inicial)
        sel.type("//input[@id='issue_due_date']", data_final)
        sel.type("issue_estimated_hours", tempo_estimado_da_tarefa)
        sel.select("issue_custom_field_values_6", "label=%s" % nucleo)
        sel.click("commit")
        sel.wait_for_page_to_load("30000")

        if preencher_tempos:
            self.preencher_tempos(data_inicial, data_final)

        if fechar_tarefa:
            self.fechar_tarefa()

    def _discover_dates(self, data_inicial, data_final):
        data_inicial = strptime(data_inicial, "%Y-%m-%d")
        data_final = strptime(data_final, "%Y-%m-%d")

        #convert date objects to datetime.date objects
        data_inicial = datetime.date(data_inicial.tm_year, data_inicial.tm_mon, data_inicial.tm_mday)
        data_final = datetime.date(data_final.tm_year, data_final.tm_mon, data_final.tm_mday)

        dates_and_hours = []
        dias_de_tarefa = (data_final - data_inicial).days + 1

        data_atual = data_inicial
        for i in range(dias_de_tarefa):
            if data_atual.isoweekday() in range(1, 6): #dia de trabalho [1,2,3,4,5]
                data = data_atual.strftime("%Y-%m-%d")
                dates_and_hours.append((data, "4"))
            data_atual = datetime.timedelta(days=1) + data_atual

        return dates_and_hours

    def preencher_tempos(self, data_inicial, data_final):
        sel = self.selenium

        dates_and_hours = self._discover_dates(data_inicial, data_final)
        # like: [("2011-03-14": 4), .....]

        for date, hour in dates_and_hours:
            sel.click("link=Tempo de trabalho")
            sel.wait_for_page_to_load("30000")
            sel.type("time_entry_spent_on", str(date)) # "2011-03-14"
            sel.type("time_entry_hours", str(hour))
            sel.click("commit")
            sel.wait_for_page_to_load("30000")

    def fechar_tarefa(self):
        sel = self.selenium
        sel.click("link=Atualizar")
        sel.select("issue_done_ratio", "label=100 %")
        sel.select("issue_status_id", "label=Resolvido")
        sel.click("//input[@name='commit' and @value='Enviar']")
        sel.wait_for_page_to_load("30000")

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

