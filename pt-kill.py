import sys
import getopt
from settings import DATABASES
import psycopg2
import logging


def main(argv):
    logging.basicConfig(filename='slowquery.log', filemode='a',
                        level=logging.DEBUG,
                        format='%(name)s - %(levelname)s - %(message)s')
    database_config = ""
    dry_run = False
    try:
        opts, args = getopt.getopt(argv, "hc:d:", ["config=", "dryrun="])
    except getopt.GetoptError:
        print('pt-kill.py -c <config> -d')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pt-kill.py -c <config> -d')
            sys.exit()
        elif opt == '-c':
            database_config = arg
        elif opt == '-d':
            dry_run = arg
        else:
            print('pt-kill.py -c <config> -d')
            sys.exit()
    connection_params = DATABASES[database_config]
    conn = psycopg2.connect(dbname=connection_params["DBNAME"],
                            user=connection_params["USERNAME"],
                            password=connection_params["PASSWORD"],
                            host=connection_params["DB_HOST"],
                            port=connection_params["DB_PORT"])
    select_running_queries = ('SELECT pid, \n'
                              'now() - query_start AS duration, \n'
                              'query, state, client_addr \n'
                              'FROM pg_stat_activity \n'
                              'WHERE now() - query_start > interval \n'
                              '\'%s second\' \n'
                              'AND state = \'active\';')
    select_running_queries = (select_running_queries %
                              (connection_params["THRESHOLD_IN_SEC"]))
    cursor = conn.cursor()
    cursor.execute(select_running_queries)
    long_running_queries = cursor.fetchall()
    for query in long_running_queries:
        query_details = "PID: %s, DURATION: %s, IP_ADDRESS: %s, QUERY: %s"
        query_details = query_details % (query[0], query[1],
                                         query[4], query[2])
        if not dry_run:
            kill_query = "SELECT pg_cancel_backend(%s)" % query[0]
            cursor.execute(kill_query)
        logging.info(query_details)


if __name__ == "__main__":
    main(sys.argv[1:])
