import indexing.crawl
import metadata.fetch
import common.database
import common.statistics
import argcomplete
import argparse
import pprint


def init_parsers():
    parser = argparse.ArgumentParser(prog='nyja')
    subparsers = parser.add_subparsers(help='Sub-commands')

    # nyja crawl
    crawl_parser = subparsers.add_parser(
        'crawl', help='Crawl indexers to retrieve onion links')
    crawl_parser.add_argument(
        'URL', help='The URL of the indexing site to crawl')
    crawl_parser.add_argument('-e', '--export', nargs='?',
                              help='Export the output of the command to /app/<EXPORT>')
    crawl_parser.add_argument('-o', '--output', action='store_true',
                              help='Display onions and don\'t save  to database')
    crawl_parser.set_defaults(func=indexing.crawl.onions)

    # nyja metadata
    metadata_parser = subparsers.add_parser(
        'metadata', help='Crawl onions to retrieve metadata')
    metadata_parser.add_argument(
        'URL', help='The URL of the onion site to crawl metadata', nargs='?')
    metadata_parser.add_argument(
        'FILE', help='The name of the file containing onions site to crawl metadata', nargs='?')
    metadata_parser.add_argument('-i', '--indexers', nargs='?',
                                 help='Specify the indexer that this onion was found on')

    metadata_parser.add_argument('-e', '--export', nargs='?',
                                 help='Export the output of the command to /app/<EXPORT>')
    metadata_parser.add_argument('-o', '--output', action='store_true',
                                 help='Display onions metadata and don\'t save  to database')
    metadata_parser.set_defaults(func=metadata.fetch.all)

    # nyja search : nested formulas
    # 
    search_parser = subparsers.add_parser(
        'search', help='Search websites on the given conditions in a nested formula. You can query the database using expressions but there are a number of rules to follow. The different fields to search are: TITLE, LOGIN, CAPTCHA, CRYPTO, PRODUCTS, HTML, ADDRESSES, INDEXERS, ONLINE. Each field can only by used once. Use ALL to retrieve the whole database. Use ( ) for any operation between two logical operators like && or ||. Use { } for any operation between fields.')
    search_parser.add_argument(
        'NESTED', help='Example : { { TITLE ( Dark || Hack ) && HTML ( Cocaine || Hack ) } && CAPTCHA false }', nargs='+')
    # Date argument to perform search on older versions
    search_parser.add_argument('-d', '--date', nargs=1,
                               help='Specify a date to perform a search in older versions. Please specify the date with the following format : dd/mm/yyyy')
    search_parser.set_defaults(func=common.database.search_nested)
    
    # nyja stats : statitics about the crypto markets
    stats_parser = subparsers.add_parser(
        'stats', help='Some functions providing key information about the crypto markets')
    stats_parser.add_argument(
        'FUNC', help='The statistics function to call', nargs=1, choices=['evo_website', 'evo_website_feature', 'evo_website_avg', 'evo_website_feature_avg', 'online_website', 'online_website_avg', 'history_versions_website', 'history_versions_website_feature', 'history_online_website'])
    stats_parser.add_argument(
        '-w', '--weeks', help='The number of weeks to study', nargs='?')
    stats_parser.add_argument(
        '-t', '--title', help='The title of the website to study', nargs='+')
    stats_parser.add_argument(
        '-f', '--feature', help="The website's feature to study", nargs='?')
    stats_parser.set_defaults(func=common.statistics.stats_router)

    return parser


if __name__ == '__main__':
    parser = init_parsers()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if 'func' in args:
        if 'export' in args :
            if args.export or not args.output:
                args.func(args)
            else:
                pprint.pprint(args.func(args))
        else :
            pprint.pprint(args.func(args))
    else:
        parser.print_help()
