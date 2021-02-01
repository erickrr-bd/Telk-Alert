import sys
sys.path.append('./modules')
from UtilsClass import Utils

class Rules:

	utils = Utils()

	options_level_alert = [("Low", "Low level alert", 1),
						  ("Medium", "Medium level alert", 0),
						  ("High", "High level alert", 0)]

	options_unit_time = [("minutes", "Time expressed in minutes", 1),
						("hours", "Time expressed in hours", 0),
						("days", "Time expressed in days", 0)]

	def createNewRule(self, form_dialog):
		options_type_alert = [("Frequency", "Make the searches in the index periodically", 1)]

		options_filter_alert = [("Query String", "Perform the search using the Query String of ElasticSearch", 1)]

		data_conf = self.utils.readFileYaml(self.utils.getPathTalert('conf') + '/es_conf.yaml')
		data_rule = []
		name_rule = form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", "rule1")
		data_rule.append(name_rule)
		level_alert = form_dialog.getDataRadioList("Select a option:", self.options_level_alert, "Alert Rule Level")
		data_rule.append(level_alert)
		index_name = form_dialog.getDataInputText("Enter the index pattern where the searches will be made:", "winlogbeat-*")
		data_rule.append(index_name)
		type_rule = form_dialog.getDataRadioList("Select a option:", options_type_alert, "Alert Rule Type")
		data_rule.append(type_rule)
		if type_rule == "Frequency":
			num_events = form_dialog.getDataNumber("Enter the number of events found in the rule to send the alert to:", "1")
			unit_time_search = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
			num_time_search = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " in which you want the search to be repeated:", "2")
			unit_time_back = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
			num_time_back = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " of time back in which you want to perform the search:", "2")
			data_rule.append(num_events)
			data_rule.append(unit_time_search)
			data_rule.append(num_time_search)
			data_rule.append(unit_time_back)
			data_rule.append(num_time_back)
		filter_type = form_dialog.getDataRadioList("Select a option:", options_filter_alert, "Alert Rule Filter:")
		if filter_type == "Query String":
			query_string = form_dialog.getDataInputText("Enter the query string:", "event.code : 4120")
			use_restriction_fields = form_dialog.getDataYesOrNo("Do you want your search results to be restricted to certain fields?", "Restriction By Fields")
			if use_restriction_fields == "ok":
				number_fields = form_dialog.getDataNumber("Enter how many fields you want to enter for the restriction:", "2")
		print(data_rule)
		form_dialog.mainMenu()



