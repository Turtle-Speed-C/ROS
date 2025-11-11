#include <iostream>
#include <thread>
#include <chrono>                //时间相关的头文件
#include <functional>            //函数包装器
#include <cpp-httplib/httplib.h> //网络下载相关

class Download
{
public:
    void download(const std::string &host, const std::string &path, const std::function<void(const std::string &, const std::string &)> &callback)
    {
        std::cout << "线程" << std::this_thread::get_id() << std::endl;
        httplib::Client client(host);
        auto response = client.Get(path);
        if (response && response->status == 200)
        {
            callback(path, response->body);
        }
    }

    void start_download(const std::string &host, const std::string &path, const std::function<void(const std::string &, const std::string &)> &callback)
    {
        auto download_fun = bind(&Download::download, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3);
        std::thread download_thread(download_fun, host, path, callback);
        download_thread.detach();
    };
};

int main()
{
    // 创建Download对象
    Download download;

    // 定义回调函数（Lambda表达式）
    // 当下载完成时被调用，用于处理下载结果
    // 参数：
    //   - path: 下载的资源路径
    //   - result: 下载的内容（字符串）
    // -> void: 显式指定返回类型为void
    auto download_finish_callback = [](const std::string &path, const std::string &result) -> void
    {
        // 输出下载完成信息
        std::cout << "下载完成：" << path
                  << "共：" << result.length() << "字，" // result.length() 获取字符串长度
                  << "内容为：" << result.substr(0, 16)  // substr(0, 16) 截取前16个字符
                  << std::endl;
    };

    download.start_download("http://localhost:8000", "/novel1.txt", download_finish_callback);
    download.start_download("http://localhost:8000", "/novel2.txt", download_finish_callback);
    download.start_download("http://localhost:8000", "/novel3.txt", download_finish_callback);

    std::this_thread::sleep_for(std::chrono::milliseconds(1000 * 10));
    return 0;
};