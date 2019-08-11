# Python Function To Create SQL Interval Case Statements
def sql_intervals(start, end, interval_between, column, table):
    """
        Creates T-SQL case statement of intervals from start to end with the number of intervals inbetween
        Also includes the column and table to create a whole select statement

        Example: 
        - Input: sql_intervals(0,101,10, 'Average','dbo.BattingAverages')
        - Output:
        SELECT Average,
        CASE
                WHEN Average > 0 and Average <= 10 THEN '1-10'
                WHEN Average > 10 and Average <= 20 THEN '11-20'
                WHEN Average > 20 and Average <= 30 THEN '21-30'
                WHEN Average > 30 and Average <= 40 THEN '31-40'
                WHEN Average > 40 and Average <= 50 THEN '41-50'
                WHEN Average > 50 and Average <= 60 THEN '51-60'
                WHEN Average > 60 and Average <= 70 THEN '61-70'
                WHEN Average > 70 and Average <= 80 THEN '71-80'
                WHEN Average > 80 and Average <= 90 THEN '81-90'
                WHEN Average > 90 and Average <= 100 THEN '91-100'
        END AS Intervals
        FROM dbo.BattingAverages

    """
    print('SELECT {}, \n\tCASE '.format(column))
    intervals = range(start, end, interval_between)
    for idx, val in enumerate(intervals): # Breaks up values from 0 to 100 in 10 different intervals
        if idx == len(intervals) - 1:
            pass
        else:
            upper_val = intervals[idx + 1]
            print("\t\tWHEN {} > {} and {} <= {} THEN '{}-{}'".format(column, val, column, upper_val,val+1, upper_val))
    print("END AS Intervals")
    print("FROM {}".format(table))



sql_intervals(0,101,10, 'Average','dbo.BattingAverages')
