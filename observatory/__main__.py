import observatory

parser = observatory.create_commandline_parser()

args = parser.parse_args()

if args.command == 'server':
    import observatory.server
    observatory.server.run_server(args.port, args.seed_nodes)