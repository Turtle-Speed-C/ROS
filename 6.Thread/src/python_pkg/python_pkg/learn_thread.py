import threading
import requests


class Download:
    def download(self, url, callback):
        print(f"线程：{threading.current_thread().ident} 开始下载：{url}")
        response = requests.get(url)
        response.encoding = "utf-8"
        callback(url, response.text)

    def start_download(self, url, callback):
        thread = threading.Thread(target=self.download, args=(url, callback))
        thread.start()


def download_finish_callback(url, result):
    print(f"{url}下载完成，共{len(result)}字，内容为{result[:5]}")


def main():
    d = Download()

    d.start_download("http://localhost:8000/novel1.txt", download_finish_callback)
    d.start_download("http://localhost:8000/novel2.txt", download_finish_callback)
    d.start_download("http://localhost:8000/novel3.txt", download_finish_callback)

if __name__=="__main__":
    main()

"""
threading.Thread()：创建一个新的线程对象
        threading.Thread(target=None, args=(), kwargs={}, name=None, daemon=None)
        target: 线程要执行的函数（必需参数）
        args: 传递给target函数的参数元组
        kwargs: 传递给target函数的关键字参数字典
        name: 线程名称（可选，用于调试）
        daemon: 是否为守护线程（可选，True表示主线程结束时子线程也结束）
    返回类型: threading.Thread 类的实例对象
    包含的信息:
        线程ID（通过 thread.ident 获取）
        线程名称（通过 thread.name 获取）
        线程状态（通过 thread.is_alive() 检查）
        线程是否为守护线程（通过 thread.daemon 获取）

thread.start()：启动线程，使线程进入就绪状态，等待CPU调度执行。

requests.get()：发送HTTP GET请求，获取指定URL的资源内容。
        requests.get(url, params=None, headers=None, timeout=None, **kwargs)
        url: 要请求的URL地址（必需参数）
        params: URL查询参数，字典或元组列表
        headers: 请求头字典
        timeout: 超时时间（秒），可以是单个数字或元组(connect_timeout, read_timeout)
        verify: 是否验证SSL证书（默认True）
        stream: 是否使用流式下载（默认False）
    返回类型: requests.models.Response 对象
    包含的重要属性和方法:
        response.status_code: HTTP状态码（如200, 404, 500）
        response.headers: 响应头字典
        response.content: 响应内容的原始字节数据
        response.text: 解码后的字符串内容
        response.json(): 将JSON响应解析为Python对象
        response.url: 最终请求的URL（可能经过重定向）
        response.encoding: 响应内容的编码
        response.cookies: 服务器返回的cookies
        response.elapsed: 请求耗时

response.encoding：获取或设置响应内容的编码方式。

response.text：获取响应内容的字符串形式，根据response.encoding进行解码。

result[:5] 表示：从 result 的第 0 个位置开始，取到第 4 个位置（共 5 个元素）
"""
