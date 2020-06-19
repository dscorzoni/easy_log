# SQL queries used in log tool app.

def logs_per_day():
    strSQL = """
    SELECT 
        strftime('%H:%M', created_at) AS ca_day,
        COUNT(1) AS log_count
    FROM log
    GROUP BY 1
    """
    return strSQL