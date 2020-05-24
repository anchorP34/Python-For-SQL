from datetime import date, datetime, timedelta
import re

def daily_data_pull(start_date_string = None
                    , end_date_string = None
                    , sql_text = None
                    , variable_mapping = {}
                    , print_sql = 'last'
                    ):
    """
        Daily Data Pull:
            This is designed to to create a SQL script for each individual day
            from the start_date to the end_date. This has the idea of doing 
            daily extracts and aggregations to prevent query timeouts

        Inputs:
            start_date_string (string): First date that would like to be included in the daily pull (yyyy-mm-dd)
            end_date_string (string): Last date that would like to be included in the daily pull (yyyy-mm-dd)
            sql_text (string): SQL statement that would like to be run 
            variable_mapping (dictionary): strings that need to be replaced if they are commonly referenced
            print_sql (string): If you would like to print the SQL, put 'all' or if you would just like the last
                                day's SQL to be printed, put 'last'


        Outputs:

        Notes:
            There is 1 different moving variables in the SQL at all times
                current_date -> The current date in the for loop
            These dates can be used in the variable mapping as well for more flexibility 
            in moving different dates around.

            If you want the date to be changed based off the current_date, make sure you
            wrap it in $'s.

            Included in the vairable mappings can be the number reassignments. For example,
            if you put $current_date_plus_3$ and the current_date happens to be '2020-03-10', 
            that will transform the SQL to change that into '2020-03-13'. This gives the ability
            to have different lag dates around your SQL code. Just make sure that there is a $
            in before and after the variable.

            If you do not put a start_date, it will choose 5 days prior to the current date
            If you do not put an end_date, it will choose yesterday


        Examples:


    """

    def date_string(date_value):
        """
            Date String: Converts date / datetime to a string value of YYY-MM-DD
        """

        return date.strftime(date_value, '%Y-%m-%d')

    def date_conversion(current_date, parameter_value_arr):
        """
            Date Conversion:
                This function looks to see what the current date value is and 
                changes the parameter value to a string that represents that new date.
            
            Inputs:
                current_date (datetime): What the current date of the for loop is
                parameter_vaue_arr (array): Array of parameter values that need to be converted

            Outputs:
                parameter_mapping_dict (dictionary): Dictionary of new mappings

            Example:
        """

        # Deduplicate the parameter_value_array
        parameter_value_arr = list(set(parameter_value_arr))

        parameter_mapping_dict = {}

        for param in parameter_value_arr:
            # Split values based on _
            param_split = param.split('_')

            # If it just the current date, then it should be 3 values in the split values
            if len(param_split) == 2 and param == 'current_date':
                parameter_mapping_dict['$current_date$'] = date_string(current_date)

            else:
                # Get the last value of the parameter value
                day_offset = int(param_split[-1])

                if param_split[2] == 'plus':
                    parameter_mapping_dict['$' + param + '$'] = date_string(current_date + timedelta(days = day_offset))
                elif param_split[2] == 'minus':
                    parameter_mapping_dict['$' + param + '$'] = date_string(current_date - timedelta(days = day_offset))
                else:
                    print('Something is wrong with the parameter', param)
                    quit()
            
        return parameter_mapping_dict


    # Check to see if start_date and end_date were input
    if start_date_string == None:
        start_date = date.today() - timedelta(days=5)
    else:
        # Convert string into date object
        start_date =  datetime.strptime(start_date_string, '%Y-%m-%d').date()

    if end_date_string == None:
        end_date = date.today() - timedelta(days=1)
    else:
        # Convert string into date object
        end_date =  datetime.strptime(end_date_string, '%Y-%m-%d').date()
    
    # Set the current_date equal to the start_date for the for loop
    current_date = start_date

    # Clean up the SQL to just have the SQL with the parameter values

    sql_replacements = list(sql_mapping.items())

    replaced_sql = sql_text

    for param, replacement in sql_replacements:
        replaced_sql = replaced_sql.replace(param, replacement)


    # For loop to go through every day between the start date and end date
    while current_date <= end_date:

        # Set up final sql for replacements in for loop
        final_sql = replaced_sql

        # Get all of the parameters that have $ around them
        parameter_replacements = re.findall('\$(.*?)\$', final_sql, re.MULTILINE)
        #print(parameter_replacements)

        parameter_mapping = date_conversion(current_date, parameter_replacements)
        #print(parameter_mapping)

        for param, replacement in list(parameter_mapping.items()):
            final_sql = final_sql.replace(param, replacement)

        print("-- Current Date: ", current_date, '\n')


        ##########################################################
        # Here is where you would execute your SQL command
        ##########################################################

        ################## RUN SQL HERE ##########################

        ##########################################################
        
        ##########################################################

        print('--',current_date, "has finished.\n")

        current_date += timedelta(days=1)

        # Print SQL if it was requested
        if print_sql == 'all':
            print(final_sql)
        if print_sql == 'last' and current_date > end_date:
            print(final_sql)


# Example: 

test_sql = """
    SELECT '$current_date$' as utc_date
    , *
    FROM dbo.whatever_table
    #where_clause#
    
"""

sql_mapping = {
        "#where_clause#" : "WHERE date_index BETWEEN $current_date_minus_4$ AND $current_date_plus_2$"
}

daily_data_pull('2020-03-01','2020-03-03', sql_text=test_sql, variable_mapping=sql_mapping, print_sql='all')