# SQL queries used in log tool app.

def logs_per_day():
    strSQL = """
    SELECT 
        log_string AS log_string,
        COUNT(1) AS log_count
    FROM log
    GROUP BY 1
    ORDER BY log_count DESC
    """
    return strSQL
