
client = Client('api_key', 'api_secret')
engine = sqlalchemy.create_engine('sqlite:///stream.db')
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket(pair)

pair = 'ETHUSDT'
api_key = '1238789asdfght'
api_secret = '1238789asdfght'
