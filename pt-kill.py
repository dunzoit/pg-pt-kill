import sys
import getopt
from settings import DATABASES
import psycopg2
import logging


def main(argv):
    logging.basicConfig(filename='slowquery.log', filemode='a',
                        level=logging.DEBUG,
                        format='%(name)s - %(levelname)s - %(message)s')
    database_config = "default"
    run_type = "dryrun"
    try:
        opts, args = getopt.getopt(argv, "hc:r:", ["config=", "runtype"])
    except getopt.GetoptError:
        print('pt-kill.py -c <config> -r <kill|dryrun>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pt-kill.py -c <config> -r <kill|dryrun>')
            sys.exit()
        elif opt == '-c':
            database_config = arg
        elif opt == '-r':
            run_type = arg
        else:
            print('pt-kill.py -c <config> -r <kill|dryrun>')
            sys.exit()
    connection_params = DATABASES.get(database_config)
    if not connection_params:
        print('Config not found!! Please provide the right config')
        sys.exit()
    port = connection_params.get("DB_PORT")
    if not port:
        port = 5432
    conn = psycopg2.connect(dbname=connection_params.get("DBNAME"),
                            user=connection_params.get("USERNAME"),
                            password=connection_params.get("PASSWORD"),
                            host=connection_params.get("DB_HOST"),
                            port=port)
    select_running_queries = ('SELECT pid, \n'
                              'now() - query_start AS duration, \n'
                              'query, state, client_addr \n'
                              'FROM pg_stat_activity \n'
                              'WHERE now() - query_start > interval \n'
                              '\'%s second\' \n'
                              'AND state = \'active\';')
    threshold = connection_params.get("THRESHOLD_IN_SEC")
    if not threshold:
        threshold = 10
    select_running_queries = (select_running_queries % threshold)
    cursor = conn.cursor()
    cursor.execute(select_running_queries)
    long_running_queries = cursor.fetchall()
    for query in long_running_queries:
        query_details = "PID: %s, DURATION: %s, IP_ADDRESS: %s, QUERY: %s"
        query_details = query_details % (query[0], query[1],
                                         query[4], query[2])
        if run_type == "kill":
            kill_query = "SELECT pg_cancel_backend(%s)" % query[0]
            cursor.execute(kill_query)
        logging.info(query_details)


if __name__ == "__main__":
    main(sys.argv[1:])
