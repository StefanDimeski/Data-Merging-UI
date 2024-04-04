import pandas as pd
import numpy as np
import re

def process_files(class_filename, cds_service1_filename,
								 cds_service2_filename="None",
								 cds_service3_filename="None",
								 cds_service4_filename="None", encoding="cp1252"):
		
		all_dfs = []
		
		for filename in [class_filename, cds_service1_filename, cds_service2_filename,
									cds_service3_filename, cds_service4_filename]:
			if filename == "None":
				continue

			extension = filename.split(".")[-1]

			if extension == 'csv':
				curr_df = pd.read_csv(filename, encoding=encoding)
			elif extension == 'xlsx':
				curr_df = pd.read_excel(filename)
			else:
				print("Shouldn't have gotten here")
				return

			all_dfs.append(curr_df)

		class_df, cds_demographic_df, *the_other_cds_services = all_dfs

		# if the first row is not the actual column names, read them from the second row.
		# This happens due to the system used in WCC which generates an extra unneeded row at the top
		if len(list(filter(lambda x: x is None or x == "" or "Unnamed:" in x, class_df.columns))) > 0:
			# read the real column names from the second row of the actual file (i.e. first row here
			# since the read columns do not count as a row)
			column_names = list(class_df.iloc[0])

			# discard the row with the real column names
			class_df = class_df.iloc[1:]

			# replace the wrong column names with the correct ones
			class_df.columns = column_names

		# get rid of the last grand total row. NOTE: WE MIGHT WANT TO SAVE THIS TO ADD LATER.
		class_df = class_df.iloc[:-1, :]

		class_df['Date Of Birth'] = pd.to_datetime(class_df['Date Of Birth'], format="%d/%m/%Y")
		class_df['Date Of Birth'] = class_df['Date Of Birth'].dt.strftime("%d/%m/%Y")

		cds_demographic_df['Birthdate (Clients)'] = pd.to_datetime(cds_demographic_df['Birthdate (Clients)'], format="%d/%m/%Y")
		cds_demographic_df['Birthdate (Clients)'] = cds_demographic_df['Birthdate (Clients)'].dt.strftime("%d/%m/%Y")

		merged_df = pd.merge(cds_demographic_df, class_df, how="outer",
												left_on=["First Name (Clients)", "Last Name (Clients)", "Birthdate (Clients)"],
												right_on=["First Name", "Last Name", "Date Of Birth"])
		
		unknown_string = "Not stated/inadequately described"
		
		merged_df = merged_df.fillna("")
		merged_df = merged_df.replace("", unknown_string)
		merged_df = merged_df.replace(regex=r"(?i)^Not Stated$", value=unknown_string)
		merged_df = merged_df.replace(regex=r"(?i)^Unknown$", value=unknown_string)
		merged_df = merged_df.replace(regex=r"(?i)^Not Applicable$", value=unknown_string)

		# save it to add it to the bottom later
		not_matched_cds = merged_df[merged_df['Client ID'] == unknown_string]
		merged_df.drop(not_matched_cds.index, inplace=True)

		not_matched_legal = merged_df[merged_df['Client ID (Clients)'] == unknown_string]
		merged_df.drop(not_matched_legal.index, inplace=True)

		matched_on_second_attempt = []
		# second attempt to match the unmatched ones.
		for idx_cds, client_cds in not_matched_cds.iterrows():
			potential_matches = []
			name_cds, birthdate_cds = client_cds['First Name (Clients)'] + client_cds['Last Name (Clients)'], client_cds['Birthdate (Clients)']

			for idx_legal, client_legal in not_matched_legal.iterrows():
				name_legal, birthdate_legal = client_legal['First Name'] + client_legal['Last Name'], client_legal['Date Of Birth']
				if edit_distance(name_cds.lower(), name_legal.lower()) <= 3 and birthdate_cds == birthdate_legal:
					potential_matches.append(idx_legal)

			# we have a match
			if len(potential_matches) == 1:
				matched_on_second_attempt.append(client_cds.index)

				merged_df = pd.concat([merged_df, not_matched_cds.loc[idx_cds].to_frame().T])
				merged_df.loc[client_cds.index, class_df.columns] = client_legal[class_df.columns]

		for idx_matched in matched_on_second_attempt:
			not_matched_cds = not_matched_cds.drop(index=idx_matched)

		# move 'Client ID' column to second place
		merged_df = merged_df[['Client ID (Clients)', 'Client ID'] + [col for col in merged_df.columns if col != 'Client ID (Clients)' and col != 'Client ID']]
		merged_df = merged_df.rename(columns={'Grand Total' : 'Legal Services Grand Total'})

		inconsistent_ones = pd.DataFrame(columns=merged_df.columns)
		for cds_column, class_column in [('Gender (Clients)', "Gender"),
																		('Main Language Spoken at Home (Clients)', 'Main Language Spoken At Home'),
																		('Employment Status (Clients)', 'Employment Status'),
																		('Country of Birth (Clients)', 'Country Of Birth'),
																		('Longterm Disability (Clients)', 'Disability')]:
			empty_cds = merged_df[merged_df[cds_column].str.lower().str.contains(unknown_string.lower())]
			merged_df.loc[empty_cds.index, cds_column] = merged_df.loc[empty_cds.index, class_column]

			new_inconsistent_ones = merged_df[merged_df[cds_column].str.lower() != merged_df[class_column].str.lower()]
			new_inconsistent_ones = new_inconsistent_ones[new_inconsistent_ones[class_column] != unknown_string]
			
			new_inconsistent_ones.loc[:, new_inconsistent_ones.columns != cds_column] = None
			new_inconsistent_ones.loc[:, cds_column] = 'background-color: red'

			inconsistent_ones = pd.concat([inconsistent_ones, new_inconsistent_ones])

		# Fix the suburb
		empty_cds_suburbs = merged_df[merged_df["Primary Address City (Clients)"].str.lower().str.contains(unknown_string.lower())]
		merged_df.loc[empty_cds_suburbs.index, "Primary Address City (Clients)"] = merged_df.loc[empty_cds_suburbs.index, "Client Suburb"]

		merged_df['Primary Address City (Clients)'] = merged_df['Primary Address City (Clients)'].apply(lambda suburb: match_suburb(suburb))

		inconsistent_suburbs = merged_df[merged_df['Primary Address City (Clients)'].str.lower() != merged_df['Client Suburb'].str.lower()]
		inconsistent_suburbs = inconsistent_suburbs[inconsistent_suburbs['Client Suburb'] != unknown_string]
		
		inconsistent_suburbs.loc[:, inconsistent_suburbs.columns != 'Primary Address City (Clients)'] = None
		inconsistent_suburbs.loc[:, 'Primary Address City (Clients)'] = 'background-color: red'

		# Fix Aboriginal
		empty_cds_aboriginal = merged_df[merged_df["Aboriginal / Torres Strait Islander (Clients)"].str.lower().str.contains(unknown_string.lower())]
		merged_df.loc[empty_cds_aboriginal.index, "Aboriginal / Torres Strait Islander (Clients)"] = merged_df.loc[empty_cds_aboriginal.index, "Aboriginal And Torres Strait Islander Status"]

		ones_to_rename = merged_df.loc[empty_cds_aboriginal.index, "Aboriginal / Torres Strait Islander (Clients)"]
		ones_to_rename[ones_to_rename.str.lower().str.contains("aboriginal")] = "Aboriginal"
		ones_to_rename[ones_to_rename.str.lower().str.contains("torres")] = "Torres Strait Islander"

		merged_df.loc[ones_to_rename.index, "Aboriginal / Torres Strait Islander (Clients)"] = ones_to_rename

		def map_to_simple(x):
			if "aboriginal" in x.lower():
				return "aboriginal"
			elif "torres" in x.lower():
				return "torres"
			elif "no" in x.lower():
				return "no"
			else:
				return x

		inconsistent_aboriginal = merged_df[merged_df["Aboriginal / Torres Strait Islander (Clients)"].map(map_to_simple) != merged_df['Aboriginal And Torres Strait Islander Status'].map(map_to_simple)]
		inconsistent_aboriginal = inconsistent_aboriginal[inconsistent_aboriginal["Aboriginal And Torres Strait Islander Status"] != unknown_string]

		inconsistent_aboriginal.loc[:, inconsistent_aboriginal.columns != 'Aboriginal / Torres Strait Islander (Clients)'] = None
		inconsistent_aboriginal.loc[:, 'Aboriginal / Torres Strait Islander (Clients)'] = 'background-color: red'

		# Fix main source of income
		empty_cds_income = merged_df[merged_df["Main source of income (Clients)"].str.lower().str.contains(unknown_string.lower())]
		merged_df.loc[empty_cds_income.index, "Main source of income (Clients)"] = merged_df.loc[empty_cds_income.index, "Financial Disadvantage Indicator"]

		ones_to_rename = merged_df.loc[empty_cds_income.index, "Main source of income (Clients)"]
		ones_to_rename[ones_to_rename.str.lower().str.contains("centrelink")] = "Government payments / pensions / allowances"
		ones_to_rename[ones_to_rename.str.lower().str.contains("not have means")] = "Nil income"
		ones_to_rename[ones_to_rename.str.lower().str.contains("not applicable")] = unknown_string
		ones_to_rename[ones_to_rename.str.lower().str.contains("unknown")] = unknown_string

		merged_df.loc[ones_to_rename.index, "Main source of income (Clients)"] = ones_to_rename

		def map_to_simple_income(x):
			if "government" in x.lower() or "centrelink" in x.lower():
				return "centrelink"
			elif "nil" in x.lower() or 'not have means' in x.lower():
				return "nil"
			else:
				return x

		inconsistent_income = merged_df[merged_df['Main source of income (Clients)'].map(map_to_simple_income) != merged_df["Financial Disadvantage Indicator"].map(map_to_simple_income)]
		inconsistent_income = inconsistent_income[inconsistent_income['Financial Disadvantage Indicator'] != unknown_string]
		
		inconsistent_income.loc[:, inconsistent_income.columns != 'Main source of income (Clients)'] = None
		inconsistent_income.loc[:, 'Main source of income (Clients)'] = 'background-color: red'
		
		# Fix Family Violence
		empty_cds_violence = merged_df[merged_df["Family Violence (Clients)"].str.lower().str.contains(unknown_string.lower())]
		merged_df.loc[empty_cds_violence.index, "Family Violence (Clients)"] = merged_df.loc[empty_cds_violence.index, "Family Violence Indicator"]

		ones_to_rename = merged_df.loc[empty_cds_violence.index, "Family Violence (Clients)"]
		ones_to_rename[ones_to_rename.str.lower().str.contains("at risk")] = "At Risk"
		ones_to_rename[ones_to_rename.str.lower().str.contains("unknown")] = unknown_string
		ones_to_rename[ones_to_rename.str.lower().str.contains("not applicable")] = unknown_string

		merged_df.loc[ones_to_rename.index, "Family Violence (Clients)"] = ones_to_rename

		def map_to_simple_violence(x):
			if 'risk' in x.lower():
				return "risk"
			else:
				return x

		inconsistent_violence = merged_df[merged_df['Family Violence (Clients)'].map(map_to_simple_violence) != merged_df['Family Violence Indicator'].map(map_to_simple_violence)]
		inconsistent_violence = inconsistent_violence[inconsistent_violence['Family Violence Indicator'] != unknown_string]

		inconsistent_violence.loc[:, inconsistent_violence.columns != 'Family Violence (Clients)'] = None
		inconsistent_violence.loc[:, 'Family Violence (Clients)'] = 'background-color: red'

		# Fix Homeless 
		empty_cds_homeless = merged_df[merged_df["Homeless (Clients)"].str.lower().str.contains(unknown_string.lower())]
		merged_df.loc[empty_cds_homeless.index, "Homeless (Clients)"] = merged_df.loc[empty_cds_homeless.index, "Homelessness Status"]

		ones_to_rename = merged_df.loc[empty_cds_homeless.index, "Homeless (Clients)"]
		ones_to_rename[ones_to_rename.str.lower().str.contains("at risk")] = "At Risk"
		ones_to_rename[ones_to_rename.str.lower().str.contains("unknown")] = unknown_string

		merged_df.loc[ones_to_rename.index, "Homeless (Clients)"] = ones_to_rename

		inconsistent_homeless = merged_df[merged_df['Homeless (Clients)'].map(map_to_simple_violence) != merged_df['Homelessness Status'].map(map_to_simple_violence)]
		inconsistent_homeless = inconsistent_homeless[inconsistent_homeless['Homelessness Status'] != unknown_string]

		inconsistent_homeless.loc[:, inconsistent_homeless.columns != 'Homeless (Clients)'] = None
		inconsistent_homeless.loc[:, 'Homeless (Clients)'] = 'background-color: red'

		# append the ones that didnt match
		merged_df = pd.concat([merged_df, not_matched_cds])

		temp_cols = [col for col in not_matched_cds.columns if 'First Name (' not in col and 'Last Name (' not in col and 'Birthdate' not in col]

		not_matched_cds.loc[:, temp_cols] = None
		not_matched_cds.loc[:, ['First Name (Clients)', 'Last Name (Clients)', 'Birthdate (Clients)']] = 'background-color: red'

		cols_to_remove = ['First Name', 'Last Name', "Date Of Birth", "Gender", "Client Suburb",
									   "Aboriginal And Torres Strait Islander Status", 'Main Language Spoken At Home', 'Employment Status',
										   "Country Of Birth", "Financial Disadvantage Indicator", "Family Violence Indicator", "Disability",
											   "Homelessness Status"]

		merged_df = merged_df.drop(columns=cols_to_remove)
		inconsistent_ones = inconsistent_ones.drop(columns=cols_to_remove)
		inconsistent_suburbs = inconsistent_suburbs.drop(columns=cols_to_remove)
		inconsistent_aboriginal = inconsistent_aboriginal.drop(columns=cols_to_remove)
		inconsistent_income = inconsistent_income.drop(columns=cols_to_remove)
		inconsistent_violence = inconsistent_violence.drop(columns=cols_to_remove)
		inconsistent_homeless = inconsistent_homeless.drop(columns=cols_to_remove)
		not_matched_cds = not_matched_cds.drop(columns=cols_to_remove)
			

		# highlight in red
		def colouring_func(curr_df):
			colour_df = pd.DataFrame(inconsistent_suburbs)

			for curr_df in [inconsistent_aboriginal, inconsistent_income, inconsistent_violence, inconsistent_homeless]:
				colour_df = pd.concat([colour_df, curr_df])

			colour_df = pd.concat([colour_df, not_matched_cds, inconsistent_ones])

			return colour_df
		
		styled_df = merged_df.style.apply(colouring_func, axis=None)

		return styled_df

def match_suburb(to_match):
		suburbs = ['Bundoora',
								'Doreen',
								'Epping North',
								'Epping',
								'Lalor',
								'Mernda',
								'Mill Park',
								'South Morang',
								'Thomastown',
								'Whittlesea',
								'Beveridge',
								'Donnybrook',
								'Eden Park',
								'Humevale',
								'Kinglake West',
								'Wollert',
								'Woodstock',
								'Yan Yean']
		
		if to_match in suburbs:
			return to_match

		scores = [edit_distance(suburb.lower(), to_match.lower()) for suburb in suburbs]

		return suburbs[np.argmin(scores)]


def edit_distance(str1, str2):
	dp = [[0 for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

	for i in range(len(str1) + 1):
		for j in range(len(str2) + 1):
			if i == 0:
				dp[i][j] = j
			elif j == 0:
				dp[i][j] = i
			elif str1[i-1] == str2[j-1]:
				dp[i][j] = dp[i-1][j-1]
			else:
				dp[i][j] = 1 + min(dp[i][j-1],
													dp[i-1][j],
													dp[i-1][j-1])

	return dp[len(str1)][len(str2)]
