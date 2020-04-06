from Web import web_start, app

print("Web 服务器已开启于 http://127.0.0.1:5000. 按 <Ctrl-C> 关闭")
print("The web server has been started at http://127.0.0.1:5000. Press <Ctrl-C> to close")

try:
    web_start.socket_io.run(app, host='0.0.0.0')
    # app.run(host='0.0.0.0')
except KeyboardInterrupt:
    # web_start.disconnect()
    web_start.socket_io.stop()
