from lib.interface import server
from config.setting import SERVER_PORT
server.run(
    host='0.0.0.0',  # 这里用0.0.0.0，那么其他人只要和本人处于同一个局域网中都可以访问该接口，也可以直接用127.0.0.1访问接口
    port=SERVER_PORT,
    debug=True
)