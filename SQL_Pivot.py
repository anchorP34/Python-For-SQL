def create_pivot_query(id_columns
            , column_focus
            , column_values
            , aggregation_type
            , aggregated_column
            , from_statement
            ):
    """
    id_columns (array) - Values that will be the index values
    column_focus (string) - Column that holds the topics that will be pivoted out
    column_values (array) - Values that will be aggregated in the query
    aggregation_metric (string) - Aggregation type for the column_values
    aggregated_column (string) - Discrete / Continuous variable that will be aggregated
    from_statement (string) - The from statement in the query that holds the referenced columns

    Python Example
    create_pivot_query(['State','City']
            , 'Population_Type'
            , ['Rural','Urban','Suburban']
            , 'SUM'
            , 'Population'
            , 'FROM dbo.Populations')

    ## T-SQL Pivot Example ##

    SELECT *
    FROM (
        SELECT State
        , City
        , Population
        , Population_Type
        FROM dbo.Populations
    ) SRC
    PIVOT
    (
        SUM(Population) FOR Population_Type IN (['Rural','Urban','Suburban'])
    ) AS PIV


    ## Regular SQL Replacement ##

    SELECT State
    , City
    , SUM(CASE WHEN Population_Type = 'Rural' THEN Population ELSE NULL END) AS Rural_SUM
    , SUM(CASE WHEN Population_Type = 'Urban' THEN Population ELSE NULL END) AS Urban_SUM
    , SUM(CASE WHEN Population_Type = 'Suburban' THEN Population ELSE NULL END) AS Suburban_SUM
    FROM dbo.Populations
    GROUP BY State
    , City

    """
    # Print out all of the ID columns in the select statement
    print('SELECT {}'.format("\n, ".join(id for id in id_columns)))

    # Print out all of the values that would have been pivoted out
    for val in column_values:
        if type(val) == str:
            print(", {}(CASE WHEN {} = '{}' THEN {} ELSE NULL END) AS {}_{}".format(aggregation_type
                                                                                , column_focus
                                                                                , val.replace("'","''")
                                                                                , aggregated_column
                                                                                , '"' + val
                                                                                , aggregation_type + '"') 
            )
        # If the value is not a string value
        else:
            print(', {}(CASE WHEN {} = {} THEN {} ELSE NULL END) AS "{}_{}"'.format(aggregation_type
                                                                                , column_focus
                                                                                , val
                                                                                , aggregated_column
                                                                                , val
                                                                                , aggregation_type)
            )

    # Print the From statement
    print(from_statement)

    # Print the group by statement
    print('GROUP BY {}'.format("\n, ".join(id for id in id_columns)))